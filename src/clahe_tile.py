import numpy as np

class CLAHEGrid:
    """
    Fully Vectorized Grid-Tile CLAHE with Bilinear Interpolation (Zuiderveld reference).
    Executes in milliseconds via NumPy matrix operations.
    """
    def __init__(self, tile_grid_size=(8, 8), clip_limit=3.0, num_bins=256, iterative_clip=True):
        """
        tile_grid_size: (tiles_y, tiles_x) e.g. (8, 8)
        clip_limit: maximum slope factor alpha (e.g., 3.0 in Fiji)
        num_bins: number of histogram bins (typically 256 for 8-bit images)
        iterative_clip: if True, redistributes repeatedly until convergence (Fiji behavior);
                        if False, single pass redistribution (OpenCV behavior).
        """
        self.tile_grid_size = tile_grid_size
        self.clip_limit = clip_limit
        self.num_bins = num_bins
        self.iterative_clip = iterative_clip

    def _clip_and_redistribute(self, hist: np.ndarray, n_pixels: int) -> np.ndarray:
        """
        Clip histogram and redistribute clipped excess pixels.
        clip_threshold = max(1, int(clip_limit * n_pixels / num_bins))
        """
        threshold = max(1, int(self.clip_limit * n_pixels / self.num_bins))
        clipped_hist = hist.copy()
        
        excess = np.sum(np.maximum(0, hist - threshold))
        clipped_hist = np.minimum(clipped_hist, threshold)
        
        if self.iterative_clip:
            # Iterative redistribution (Fiji / ImageJ behavior)
            while excess > 0:
                step = max(1, excess // self.num_bins)
                for k in range(self.num_bins):
                    if clipped_hist[k] < threshold:
                        add = min(threshold - clipped_hist[k], step)
                        clipped_hist[k] += add
                        excess -= add
                        if excess <= 0:
                            break
                if excess > 0 and np.all(clipped_hist >= threshold):
                    clipped_hist += excess // self.num_bins
                    excess = 0
        else:
            # Single-pass uniform redistribution (OpenCV behavior)
            bonus = excess // self.num_bins
            clipped_hist += bonus
            
        return clipped_hist

    def apply(self, img: np.ndarray) -> np.ndarray:
        """
        Apply Tile-Grid CLAHE to input 2D grayscale uint8 image using NumPy vectorization.
        """
        h, w = img.shape
        ty, tx = self.tile_grid_size
        
        tile_h = float(h) / ty
        tile_w = float(w) / tx
        
        # 1. Compute LUT for each tile
        luts = np.zeros((ty, tx, self.num_bins), dtype=np.float32)
        
        for i in range(ty):
            y_start = int(i * tile_h)
            y_end = int((i + 1) * tile_h) if i < ty - 1 else h
            for j in range(tx):
                x_start = int(j * tile_w)
                x_end = int((j + 1) * tile_w) if j < tx - 1 else w
                
                tile = img[y_start:y_end, x_start:x_end]
                n_pixels = tile.size
                
                # Fast histogram
                hist = np.bincount(tile.ravel(), minlength=self.num_bins)
                
                # Clip & redistribute
                clipped = self._clip_and_redistribute(hist, n_pixels)
                
                # CDF
                cdf = clipped.cumsum()
                
                # Create LUT for this tile
                luts[i, j] = (cdf / cdf[-1]) * (self.num_bins - 1)
                
        # 2. Vectorized Bilinear Interpolation over image grid
        Y, X = np.ogrid[:h, :w]
        
        # Continuous tile indices
        i_float = (Y + 0.5) / tile_h - 0.5
        j_float = (X + 0.5) / tile_w - 0.5
        
        # Bounding integer indices
        i1 = np.clip(np.floor(i_float).astype(int), 0, ty - 1)
        i2 = np.clip(i1 + 1, 0, ty - 1)
        a = np.clip(i_float - i1, 0.0, 1.0)
        
        j1 = np.clip(np.floor(j_float).astype(int), 0, tx - 1)
        j2 = np.clip(j1 + 1, 0, tx - 1)
        b = np.clip(j_float - j1, 0.0, 1.0)
        
        # Matrix lookup across 4 surrounding LUTs
        lut11 = luts[i1, j1, img]
        lut12 = luts[i1, j2, img]
        lut21 = luts[i2, j1, img]
        lut22 = luts[i2, j2, img]
        
        # Matrix Bilinear Interpolation equation
        interp_img = (1 - a) * ((1 - b) * lut11 + b * lut12) + a * ((1 - b) * lut21 + b * lut22)
        out_img = np.clip(np.round(interp_img), 0, 255).astype(np.uint8)
        
        return out_img
