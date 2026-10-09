import os
import cv2
import skimage.data
import numpy as np
from src.utils import create_synthetic_test_images

def prepare_sample_dataset(data_dir: str = "data"):
    """
    Prepare sample image dataset for CLAHE evaluation:
    1. Extract standard images from skimage.data
    2. Generate synthetic low-contrast, phantom, and noise images
    """
    os.makedirs(data_dir, exist_ok=True)
    print(f"Preparing dataset in folder: {data_dir}")
    
    # 1. Generate synthetic images
    create_synthetic_test_images(data_dir)
    
    # 2. Extract standard skimage benchmark images
    # Moon (Low contrast lunar surface)
    moon = skimage.data.moon()
    cv2.imwrite(os.path.join(data_dir, "skimage_moon.png"), moon)
    
    # Coins (Microscopy / shape segmentation reference)
    coins = skimage.data.coins()
    cv2.imwrite(os.path.join(data_dir, "skimage_coins.png"), coins)
    
    # Retina / Color image
    retina = skimage.data.retina()
    cv2.imwrite(os.path.join(data_dir, "skimage_retina.png"), cv2.cvtColor(retina, cv2.COLOR_RGB2BGR))
    
    # Astronaut / Color RGB image
    astronaut = skimage.data.astronaut()
    cv2.imwrite(os.path.join(data_dir, "skimage_astronaut.png"), cv2.cvtColor(astronaut, cv2.COLOR_RGB2BGR))
    
    print("Dataset preparation complete! Available images:")
    for fname in os.listdir(data_dir):
        if fname.endswith(('.png', '.jpg', '.tif', '.gif')):
            fpath = os.path.join(data_dir, fname)
            img = cv2.imread(fpath)
            shape_str = f"{img.shape[1]}x{img.shape[0]}" if img is not None else "Unknown"
            print(f"  - {fname} ({shape_str})")

if __name__ == "__main__":
    prepare_sample_dataset()
