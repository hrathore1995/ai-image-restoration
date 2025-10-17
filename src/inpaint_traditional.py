import cv2
import os

DAMAGED_DIR = "data/damaged"
MASKS_DIR = "data/masks"
RESULTS_DIR = "results/traditional"

os.makedirs(RESULTS_DIR, exist_ok=True)

def inpaint_image(damaged_path, mask_path, method="telea"):
    damaged = cv2.imread(damaged_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if method == "telea":
        restored = cv2.inpaint(damaged, mask, 3, cv2.INPAINT_TELEA)
    else:
        restored = cv2.inpaint(damaged, mask, 3, cv2.INPAINT_NS)

    return restored


def process_all_images():
    for filename in os.listdir(DAMAGED_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            base_name = filename.replace("_damaged_", "_mask_").replace(".jpg", ".png")

            damaged_path = os.path.join(DAMAGED_DIR, filename)
            mask_path = os.path.join(MASKS_DIR, base_name)

            if not os.path.exists(mask_path):
                continue

            telea_restored = inpaint_image(damaged_path, mask_path, "telea")
            cv2.imwrite(os.path.join(RESULTS_DIR, filename.replace("damaged", "telea")), telea_restored)

            ns_restored = inpaint_image(damaged_path, mask_path, "ns")
            cv2.imwrite(os.path.join(RESULTS_DIR, filename.replace("damaged", "navier")), ns_restored)

            print(f"Processed {filename}")


if __name__ == "__main__":
    process_all_images()
