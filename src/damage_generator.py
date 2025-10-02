"""
Damage Generator for Synthetic Dataset
--------------------------------------

This script takes clean paintings from data/raw/ and generates
multiple damaged versions + corresponding binary masks.

Outputs:
- data/damaged/
- data/masks/
"""

import cv2
import numpy as np
import os
import random

RAW_DIR = "data/raw"
DAMAGED_DIR = "data/damaged"
MASKS_DIR = "data/masks"

# number of variations per image
VARIATIONS = 5


def generate_scratches(image, mask, num_scratches=20):
    h, w = image.shape[:2]
    for _ in range(num_scratches):
        x1, y1 = random.randint(0, w - 1), random.randint(0, h - 1)
        x2, y2 = random.randint(0, w - 1), random.randint(0, h - 1)
        color = (255, 255, 255)
        thickness = random.randint(2, 6)
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)
        cv2.line(mask, (x1, y1), (x2, y2), 255, thickness)
    return image, mask



def generate_holes(image, mask, num_holes=6):
    h, w = image.shape[:2]
    for _ in range(num_holes):
        x1, y1 = random.randint(0, w - 200), random.randint(0, h - 200)
        x2, y2 = x1 + random.randint(80, 200), y1 + random.randint(80, 200)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), -1)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
    return image, mask



def generate_noise(image, mask):
    h, w = image.shape[:2]

    # heavier Gaussian noise
    noise = np.random.normal(0, 50, (h, w, 3)).astype(np.uint8)
    damaged = cv2.addWeighted(image, 0.6, noise, 0.4, 0)

    # multiple faded patches
    for _ in range(3):
        x1, y1 = random.randint(0, w // 2), random.randint(0, h // 2)
        x2, y2 = min(w, x1 + random.randint(80, 200)), min(h, y1 + random.randint(80, 200))
        faded = damaged[y1:y2, x1:x2] // 3
        damaged[y1:y2, x1:x2] = faded
        mask[y1:y2, x1:x2] = 255

    return damaged, mask



def process_images():
    """Main pipeline: generate damaged variations + masks for each raw image."""
    os.makedirs(DAMAGED_DIR, exist_ok=True)
    os.makedirs(MASKS_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(RAW_DIR, filename)
            image = cv2.imread(img_path)

            if image is None:
                print(f"⚠️ Could not read {filename}, skipping...")
                continue

            h, w = image.shape[:2]

            for i in range(VARIATIONS):
                damaged = image.copy()
                mask = np.zeros((h, w), dtype=np.uint8)

                # randomly choose damage types
                damage_types = [generate_scratches, generate_holes, generate_noise]
                selected = random.sample(damage_types, k=random.randint(1, 3))

                for func in selected:
                    damaged, mask = func(damaged, mask)

                # save outputs
                base_name = os.path.splitext(filename)[0]
                damaged_name = f"{base_name}_damaged_{i}.jpg"
                mask_name = f"{base_name}_mask_{i}.png"

                cv2.imwrite(os.path.join(DAMAGED_DIR, damaged_name), damaged)
                cv2.imwrite(os.path.join(MASKS_DIR, mask_name), mask)

                print(f"✅ Saved {damaged_name} and {mask_name}")


if __name__ == "__main__":
    process_images()
