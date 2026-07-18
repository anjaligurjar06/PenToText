from pathlib import Path

import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError("Unable to read the image")

    return image


def calculate_blur_score(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def preprocess_image(image_path: str) -> dict:
    image = load_image(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(
        gray,
        None,
        h=10,
        templateWindowSize=7,
        searchWindowSize=21
    )

    enhanced = cv2.equalizeHist(denoised)

    thresholded = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    blur_score = calculate_blur_score(image)

    return {
        "original": image,
        "grayscale": gray,
        "enhanced": enhanced,
        "thresholded": thresholded,
        "blur_score": blur_score
    }