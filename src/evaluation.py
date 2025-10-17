import cv2
import os
import pandas as pd
import torch
import lpips
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ProcessPoolExecutor, as_completed

RAW_DIR = "data/raw"
DAMAGED_DIR = "data/damaged"
TRAD_RESULTS = "results/traditional"
DEEP_RESULTS = "results/deep"
METRICS_OUT = "results/metrics_all.csv"

TARGET_SIZE = (512, 512)

lpips_model = lpips.LPIPS(net='alex').to("cpu") 

def evaluate_one(raw_path, restored_path):
    """Compute PSNR, SSIM, and LPIPS between raw and restored images."""
    raw = cv2.imread(raw_path)
    restored = cv2.imread(restored_path)

    if raw is None or restored is None:
        return None, None, None

    raw = cv2.resize(raw, TARGET_SIZE)
    restored = cv2.resize(restored, TARGET_SIZE)

    psnr_val = psnr(raw, restored, data_range=255)
    ssim_val, _ = ssim(raw, restored, channel_axis=-1, full=True)

    raw_tensor = torch.from_numpy(raw).permute(2,0,1).unsqueeze(0).float() / 127.5 - 1.0
    restored_tensor = torch.from_numpy(restored).permute(2,0,1).unsqueeze(0).float() / 127.5 - 1.0
    lpips_val = lpips_model(raw_tensor, restored_tensor).item()

    return psnr_val, ssim_val, lpips_val


def evaluate_file(filename):
    if "_damaged_" not in filename:
        return None

    base_name = filename.split("_damaged_")[0]

    raw_candidates = [f for f in os.listdir(RAW_DIR) if f.startswith(base_name)]
    if not raw_candidates:
        return None
    raw_file = os.path.join(RAW_DIR, raw_candidates[0])

    telea_file = os.path.join(TRAD_RESULTS, filename.replace("damaged", "telea"))
    navier_file = os.path.join(TRAD_RESULTS, filename.replace("damaged", "navier"))
    sdxl_file = os.path.join(DEEP_RESULTS, filename.replace("damaged", "sdxl"))

    telea_psnr, telea_ssim, telea_lpips = evaluate_one(raw_file, telea_file)
    navier_psnr, navier_ssim, navier_lpips = evaluate_one(raw_file, navier_file)
    sdxl_psnr, sdxl_ssim, sdxl_lpips = evaluate_one(raw_file, sdxl_file)

    return {
        "image": filename,
        "telea_psnr": telea_psnr,
        "telea_ssim": telea_ssim,
        "telea_lpips": telea_lpips,
        "navier_psnr": navier_psnr,
        "navier_ssim": navier_ssim,
        "navier_lpips": navier_lpips,
        "sdxl_psnr": sdxl_psnr,
        "sdxl_ssim": sdxl_ssim,
        "sdxl_lpips": sdxl_lpips
    }


def run_evaluation():
    damaged_files = [f for f in os.listdir(DAMAGED_DIR) if "_damaged_" in f]

    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(evaluate_file, f): f for f in damaged_files}
        for future in as_completed(futures):
            res = future.result()
            if res:
                results.append(res)
                print(f"Evaluated {res['image']}")

    df = pd.DataFrame(results)
    os.makedirs("results", exist_ok=True)
    df.to_csv(METRICS_OUT, index=False)
    print(f"\nMetrics saved to {METRICS_OUT}")


if __name__ == "__main__":
    run_evaluation()
