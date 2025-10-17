import torch
from diffusers import StableDiffusionInpaintPipeline
import PIL.Image
import os

DAMAGED_DIR = "data/damaged"
MASKS_DIR = "data/masks"
RESULTS_DIR = "results/deep"

os.makedirs(RESULTS_DIR, exist_ok=True)

def run_inpainting():
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        torch_dtype=torch.float16
    )

    if torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    pipe = pipe.to(device)

    for filename in os.listdir(DAMAGED_DIR):
        if "_damaged_" not in filename:
            continue

        base_name = filename.replace("_damaged_", "_mask_").rsplit(".", 1)[0] + ".png"
        mask_path = os.path.join(MASKS_DIR, base_name)
        damaged_path = os.path.join(DAMAGED_DIR, filename)

        if not os.path.exists(mask_path):
            continue

        damaged = PIL.Image.open(damaged_path).convert("RGB")
        mask = PIL.Image.open(mask_path).convert("RGB")

        result = pipe(prompt="Restore this artwork realistically",
                      image=damaged, mask_image=mask).images[0]

        out_name = filename.replace("damaged", "sdxl")
        result.save(os.path.join(RESULTS_DIR, out_name))

        print(f"Restored {filename} with Stable Diffusion")


if __name__ == "__main__":
    run_inpainting()
