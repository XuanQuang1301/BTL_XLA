import numpy as np

def compute_entropy(img: np.ndarray) -> float:
    """Compute Shannon Entropy of gray level distribution."""
    hist, _ = np.histogram(img.flatten(), bins=256, range=[0, 256])
    prob = hist / hist.sum()
    prob = prob[prob > 0]
    return float(-np.sum(prob * np.log2(prob)))

def compute_rms_contrast(img: np.ndarray) -> float:
    """Compute Root Mean Square (RMS) Contrast (standard deviation)."""
    return float(np.std(img.astype(np.float64)))

def compute_ambe(img_orig: np.ndarray, img_enhanced: np.ndarray) -> float:
    """Compute Absolute Mean Brightness Error (AMBE). Lower is better."""
    mean_orig = float(np.mean(img_orig))
    mean_enhanced = float(np.mean(img_enhanced))
    return float(abs(mean_enhanced - mean_orig))

def compute_eme(img: np.ndarray, block_size: int = 8, epsilon: float = 1e-4) -> float:
    """
    Vectorized Compute Measure of Enhancement (EME) by Agaian et al. (2001).
    Splits image into non-overlapping blocks of size block_size x block_size.
    Formula:
        EME = (1 / (k1 * k2)) * sum(20 * ln(I_max / (I_min + epsilon)))
    """
    h, w = img.shape[:2]
    k1 = h // block_size
    k2 = w // block_size
    
    if k1 == 0 or k2 == 0:
        return 0.0
        
    cropped = img[: k1 * block_size, : k2 * block_size].astype(np.float64)
    blocks = cropped.reshape(k1, block_size, k2, block_size).transpose(0, 2, 1, 3)
    
    i_min = blocks.min(axis=(2, 3))
    i_max = blocks.max(axis=(2, 3))
    
    ratio = (i_max + epsilon) / (i_min + epsilon)
    valid = i_max > 0
    eme_vals = np.where(valid, 20.0 * np.log(ratio), 0.0)
    
    return float(np.mean(eme_vals))

def compute_psnr(img_orig: np.ndarray, img_enhanced: np.ndarray) -> float:
    """Compute Peak Signal-to-Noise Ratio (PSNR)."""
    if np.array_equal(img_orig, img_enhanced):
        return 100.0  # Cap infinity at 100 dB for comparison tables
    mse = np.mean((img_orig.astype(np.float64) - img_enhanced.astype(np.float64)) ** 2)
    if mse == 0:
        return 100.0
    return float(10.0 * np.log10(255.0 ** 2 / mse))

def compute_ssim(img_orig: np.ndarray, img_enhanced: np.ndarray) -> float:
    """Compute Structural Similarity Index (SSIM) using skimage."""
    if np.array_equal(img_orig, img_enhanced):
        return 1.0
    from skimage.metrics import structural_similarity as ssim_func
    # If 3D color, convert to 2D gray for fast robust SSIM calculation
    if img_orig.ndim == 3:
        import cv2
        g1 = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)
        g2 = cv2.cvtColor(img_enhanced, cv2.COLOR_RGB2GRAY)
        return float(ssim_func(g1, g2, data_range=255))
    return float(ssim_func(img_orig, img_enhanced, data_range=255))

def compute_flat_region_noise(img: np.ndarray, roi: tuple = None) -> float:
    """
    Compute standard deviation in a flat ROI (Background region)
    to estimate noise amplification.
    roi: (ymin, ymax, xmin, xmax) or None (auto-select top-left 50x50 block).
    """
    if roi is None:
        h, w = img.shape[:2]
        roi_img = img[: min(50, h), : min(50, w)]
    else:
        ymin, ymax, xmin, xmax = roi
        roi_img = img[ymin:ymax, xmin:xmax]
        
    return float(np.std(roi_img.astype(np.float64)))

def compute_all_metrics(img_orig: np.ndarray, img_enhanced: np.ndarray, exec_time_ms: float = 0.0) -> dict:
    """
    Calculate full set of 7 quantitative metrics.
    """
    if img_orig.ndim == 3:
        import cv2
        gray_orig = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)
        gray_enh = cv2.cvtColor(img_enhanced, cv2.COLOR_RGB2GRAY)
    else:
        gray_orig = img_orig
        gray_enh = img_enhanced
        
    return {
        'Entropy': compute_entropy(gray_enh),
        'RMS Contrast': compute_rms_contrast(gray_enh),
        'AMBE': compute_ambe(gray_orig, gray_enh),
        'EME': compute_eme(gray_enh),
        'PSNR (dB)': compute_psnr(img_orig, img_enhanced),
        'SSIM': compute_ssim(img_orig, img_enhanced),
        'Noise Std': compute_flat_region_noise(gray_enh),
        'Exec Time (ms)': exec_time_ms
    }
