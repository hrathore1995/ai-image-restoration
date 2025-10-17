import cv2
import numpy as np
import os
from datetime import datetime

def detect_damage_mask(image):
    
    if isinstance(image, str):
        img = cv2.imread(image)
    else:
        img = image.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    os.makedirs("masks", exist_ok=True)
    mask_path = os.path.join("masks", f"mask_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(mask_path, mask)

    return mask_path
