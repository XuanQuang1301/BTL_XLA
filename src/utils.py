import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(filepath: str, grayscale: bool = True) -> np.ndarray:
    """
    Load an image from disk.
    If grayscale is True, returns uint8 2D array (H, W).
    Otherwise returns uint8 3D array (H, W, 3) in RGB order.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Image not found at path: {filepath}")
    
    if grayscale:
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Failed to read image as grayscale: {filepath}")
        return img
    else:
        img_bgr = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img_bgr is None:
            raise ValueError(f"Failed to read image as color: {filepath}")
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

def save_image(img: np.ndarray, filepath: str) -> None:
    """Save an image to disk."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    if img.ndim == 2:
        cv2.imwrite(filepath, img)
    else:
        cv2.imwrite(filepath, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

def process_color_image(img_rgb: np.ndarray, enhance_func) -> np.ndarray:
    """
    Apply a grayscale enhancement function to a color RGB image
    by transforming to CIE L*a*b* space, enhancing L*, and reconstructing RGB.
    This prevents color shifts (Hue shift).
    """
    # Convert RGB to LAB
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    
    # Enhance L channel
    l_enhanced = enhance_func(l_channel)
    
    # Recombine and convert back to RGB
    enhanced_lab = cv2.merge((l_enhanced, a_channel, b_channel))
    enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
    return enhanced_rgb

def create_synthetic_test_images(output_dir: str):
    """
    Generate synthetic test images representing common CLAHE evaluation scenarios:
    1. Low contrast gradient image
    2. Artificial medical chest X-ray like phantom
    3. Flat uniform background with noise
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Low contrast dark image (simulating under-exposed scene)
    h, w = 512, 512
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    xx, yy = np.meshgrid(x, y)
    pattern = np.sin(4 * np.pi * xx) * np.cos(4 * np.pi * yy)
    # Compress dynamic range to low contrast [30, 80]
    low_contrast = (pattern - pattern.min()) / (pattern.max() - pattern.min()) * 50 + 30
    low_contrast = low_contrast.astype(np.uint8)
    cv2.imwrite(os.path.join(output_dir, "synthetic_low_contrast.png"), low_contrast)
    
    # 2. Simulated Medical Phantom (X-Ray phantom with dark and bright spots)
    phantom = np.full((h, w), 50, dtype=np.uint8)
    # Add circular bone structures
    cv2.circle(phantom, (256, 256), 180, 120, -1)
    cv2.circle(phantom, (256, 256), 120, 80, -1)
    cv2.circle(phantom, (180, 200), 40, 180, -1) # lesion high contrast
    cv2.circle(phantom, (320, 300), 50, 40, -1) # lesion low contrast
    # Add subtle low-contrast text detail
    cv2.putText(phantom, "PATIENT_XRAY_PHANTOM", (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.9, 95, 2)
    # Add mild Gaussian noise
    noise = np.random.normal(0, 5, phantom.shape)
    phantom_noisy = np.clip(phantom + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(output_dir, "synthetic_phantom_xray.png"), phantom_noisy)

    # 3. Flat background with low contrast noise (to test noise amplification)
    flat_noise = np.full((h, w), 128, dtype=np.float32)
    flat_noise += np.random.normal(0, 3, (h, w))
    cv2.rectangle(flat_noise, (150, 150), (350, 350), 135, -1) # faint box
    flat_noise = np.clip(flat_noise, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(output_dir, "synthetic_flat_noise.png"), flat_noise)

    print(f"Synthetic test images created in: {output_dir}")

def plot_comparison(img_dict: dict, title: str, save_path: str = None):
    """
    Plot side-by-side comparison of original and processed images along with their histograms.
    img_dict: dictionary of {'Method Name': image_array}
    """
    num_methods = len(img_dict)
    fig, axes = plt.subplots(2, num_methods, figsize=(4 * num_methods, 7))
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    if num_methods == 1:
        axes = np.expand_dims(axes, axis=1)
        
    for i, (name, img) in enumerate(img_dict.items()):
        # Plot image
        if img.ndim == 2:
            axes[0, i].imshow(img, cmap='gray', vmin=0, vmax=255)
        else:
            axes[0, i].imshow(img)
        axes[0, i].set_title(name, fontsize=11, fontweight='semibold')
        axes[0, i].axis('off')
        
        # Plot histogram
        if img.ndim == 2:
            hist, _ = np.histogram(img.flatten(), bins=256, range=[0, 256])
            axes[1, i].plot(hist, color='black', linewidth=1)
            axes[1, i].set_xlim([0, 256])
            axes[1, i].set_title("Histogram", fontsize=9)
            axes[1, i].grid(True, linestyle='--', alpha=0.5)
        else:
            for color, col_name in zip(['r', 'g', 'b'], ['Red', 'Green', 'Blue']):
                hist, _ = np.histogram(img[:, :, 'rgb'.index(color)].flatten(), bins=256, range=[0, 256])
                axes[1, i].plot(hist, color=color, alpha=0.7, label=col_name)
            axes[1, i].set_xlim([0, 256])
            axes[1, i].set_title("RGB Histogram", fontsize=9)
            axes[1, i].grid(True, linestyle='--', alpha=0.5)
            
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
