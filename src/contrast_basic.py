import numpy as np

def linear_contrast_stretch(img: np.ndarray) -> np.ndarray:
    """
    Linear Min-Max Contrast Stretching.
    Maps [rmin, rmax] to [0, L-1] (0 to 255 for 8-bit).
    
    Formula:
        s = (r - rmin) / (rmax - rmin) * 255
    """
    r_min = float(np.min(img))
    r_max = float(np.max(img))
    
    if r_max == r_min:
        return img.copy()
        
    stretched = (img.astype(np.float32) - r_min) / (r_max - r_min) * 255.0
    return np.clip(stretched, 0, 255).astype(np.uint8)

def percentile_contrast_stretch(img: np.ndarray, p_low: float = 0.35, p_high: float = 0.35) -> np.ndarray:
    """
    Percentile / Saturated Contrast Stretching (Matching ImageJ Process -> Enhance Contrast).
    p_low: percentage of pixels allowed to saturate at 0 (e.g. 0.35%)
    p_high: percentage of pixels allowed to saturate at 255 (e.g. 0.35%)
    """
    if p_low == 0.0 and p_high == 0.0:
        return linear_contrast_stretch(img)
        
    q_low = np.percentile(img, p_low)
    q_high = np.percentile(img, 100.0 - p_high)
    
    if q_high == q_low:
        return img.copy()
        
    stretched = (img.astype(np.float32) - q_low) / (q_high - q_low) * 255.0
    return np.clip(stretched, 0, 255).astype(np.uint8)

def global_histogram_equalization(img: np.ndarray) -> np.ndarray:
    """
    Global Histogram Equalization (HE) built from scratch.
    
    Steps:
    1. Compute image histogram h[k]
    2. Compute Normalized Cumulative Distribution Function (CDF)
    3. Construct Look-Up Table (LUT): LUT[k] = round((L-1) * (cdf[k] - cdf_min) / (N - cdf_min))
    4. Map input pixels via LUT
    """
    # 1. Compute histogram
    hist, _ = np.histogram(img.flatten(), bins=256, range=[0, 256])
    
    # 2. Compute CDF
    cdf = hist.cumsum()
    
    # Mask zero entries in CDF
    cdf_m = np.ma.masked_equal(cdf, 0)
    
    # 3. Compute LUT
    num_pixels = img.size
    cdf_min = cdf_m.min()
    
    if num_pixels == cdf_min:
        return img.copy()
        
    lut = ((cdf_m - cdf_min) * 255.0 / (num_pixels - cdf_min))
    lut = np.ma.filled(lut, 0).astype(np.uint8)
    
    # 4. Map image through LUT
    return lut[img]
