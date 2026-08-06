"""
prep_photo.py

Preprocesses an input portrait photograph for ASCII art conversion:
1. Removes background using rembg (with automatic fallback).
2. Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) via OpenCV.
3. Converts the image to grayscale.
4. Composites onto a solid white background.
5. Saves the output to source-prepped.png.
"""

import os
import sys
import argparse
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from PIL import Image

try:
    # pyrefly: ignore [missing-import]
    import cv2
except ImportError:
    cv2 = None

try:
    # pyrefly: ignore [missing-import]
    from rembg import remove
except ImportError:
    remove = None


class PhotoPreprocessor:
    """Preprocesses images for ASCII artwork generation."""

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    def remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background using rembg with fallback if rembg fails or offline."""
        if remove is not None:
            try:
                print("[+] Removing background with rembg...")
                return remove(image)
            except Exception as e:
                print(f"[!] rembg background removal skipped or failed ({e}). Using original photo.")
        else:
            print("[!] rembg not available. Skipping background removal.")
        return image

    def apply_clahe(self, gray_np: np.ndarray) -> np.ndarray:
        """Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)."""
        if cv2 is not None:
            print("[+] Applying CLAHE contrast enhancement with OpenCV...")
            clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            return clahe.apply(gray_np)
        else:
            print("[!] OpenCV not available. Normalizing grayscale values.")
            min_val, max_val = float(gray_np.min()), float(gray_np.max())
            if max_val > min_val:
                return ((gray_np - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)
            return gray_np

    def process(self) -> str:
        """Run the full photo preparation pipeline."""
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        print(f"[+] Loading photo from {self.input_path}...")
        img = Image.open(self.input_path).convert("RGBA")

        # 1. Remove background
        img_no_bg = self.remove_background(img)

        # 2. Extract alpha mask and composite onto white background
        bg = Image.new("RGBA", img_no_bg.size, (255, 255, 255, 255))
        composite = Image.alpha_composite(bg, img_no_bg).convert("RGB")

        # 3. Convert to Grayscale numpy array
        gray_img = composite.convert("L")
        gray_np = np.array(gray_img)

        # 4. Apply CLAHE
        enhanced_np = self.apply_clahe(gray_np)

        # Save result
        output_dir = os.path.dirname(self.output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        result_img = Image.fromarray(enhanced_np)
        result_img.save(self.output_path, "PNG")
        print(f"[OK] Successfully prepped photo -> {self.output_path}")
        return self.output_path


def main():
    parser = argparse.ArgumentParser(description="Preprocess photo for ASCII conversion.")
    parser.add_argument("--input", default="data/input_photo.png", help="Path to input photo")
    parser.add_argument("--output", default="data/source-prepped.png", help="Path to output prepped photo")
    args = parser.parse_args()

    preprocessor = PhotoPreprocessor(args.input, args.output)
    preprocessor.process()


if __name__ == "__main__":
    main()
