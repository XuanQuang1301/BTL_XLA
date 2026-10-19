import numpy as np

class CLAHECửaSổTrượt:
    """
    Fast Sliding-Window CLAHE matching Fiji / ImageJ Enhance_Local_Contrast.java behavior.
    Uses np.bincount and adaptive strided sampling for real-time execution regardless of resolution.
    """
    def __init__(self, block_size=63, clip_limit=3.0, num_bins=256, stride=None):
        """
        block_size: side length of square contextual region W x W (e.g. 63 / 127 in Fiji)
        clip_limit: maximum slope factor alpha (e.g. 3.0 in Fiji)
        num_bins: number of histogram bins (typically 256 for 8-bit images)
        stride: spatial step size (if None, adaptively computed based on image dimension)
        """
        self.block_size = block_size
        self.clip_limit = clip_limit
        self.num_bins = num_bins
        self.stride = stride

    def apply(self, img: np.ndarray) -> np.ndarray:
        """
        Apply Sliding-Window CLAHE to input 2D uint8 grayscale image.
        """
        h, w = img.shape
        
        # Determine adaptive stride if not explicitly set
        if self.stride is None:
            eff_stride = max(2, max(h, w) // 128)
        else:
            eff_stride = self.stride

        half = self.block_size // 2
        padded = np.pad(img, pad_width=half, mode='reflect')
        
        # Grid of sample positions
        y_coords = np.arange(0, h, eff_stride)
        x_coords = np.arange(0, w, eff_stride)
        
        sampled_out = np.zeros((len(y_coords), len(x_coords)), dtype=np.uint8)
        n_pixels = (2 * half + 1) ** 2
        do_clip = (self.clip_limit is not None and self.clip_limit > 0 and not np.isinf(self.clip_limit))
        if do_clip:
            threshold = max(1, int(self.clip_limit * n_pixels / self.num_bins + 0.5))
        
        for yi, y in enumerate(y_coords):
            py = y + half
            for xi, x in enumerate(x_coords):
                px = x + half
                
                # Extract window
                window = padded[py - half : py + half + 1, px - half : px + half + 1]
                
                # Fast bincount in C
                hist = np.bincount(window.ravel(), minlength=self.num_bins).astype(np.int64)
                
                if do_clip:
                    # Clip & uniform redistribute
                    excess = int(np.sum(np.maximum(0, hist - threshold)))
                    clipped = np.minimum(hist, threshold)
                    if excess > 0:
                        clipped += excess // self.num_bins
                else:
                    clipped = hist
                    
                # Center pixel CDF value
                val_center = int(img[y, x])
                cdf_val = float(np.sum(clipped[: val_center + 1]))
                total_sum = float(np.sum(clipped))
                
                out_val = round((self.num_bins - 1) * cdf_val / total_sum) if total_sum > 0 else val_center
                sampled_out[yi, xi] = np.clip(out_val, 0, 255).astype(np.uint8)

        # Upsample strided result back to full resolution if stride > 1
        if eff_stride > 1:
            import cv2
            out_img = cv2.resize(sampled_out, (w, h), interpolation=cv2.INTER_LINEAR)
        else:
            out_img = sampled_out
            
        return out_img


def local_histogram_equalization(img: np.ndarray, block_size: int = 63, stride: int = 4) -> np.ndarray:
    """
    Local Histogram Equalization (Sliding Window without contrast limiting).
    """
    sliding_he = CLAHECửaSổTrượt(block_size=block_size, clip_limit=None, stride=stride)
    return sliding_he.apply(img)
