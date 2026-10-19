import unittest
import numpy as np
import cv2

from src.contrast_basic import linear_contrast_stretch, percentile_contrast_stretch, global_histogram_equalization
from src.clahe_tile import CLAHEGrid, AHEGrid, adaptive_histogram_equalization
from src.clahe_sliding import CLAHECửaSổTrượt, local_histogram_equalization
from src.metrics import (
    compute_entropy, compute_rms_contrast, compute_ambe,
    compute_eme, compute_psnr, compute_ssim, compute_flat_region_noise,
    compute_all_metrics
)
from src.utils import process_color_image


class TestContrastStretching(unittest.TestCase):
    def test_linear_contrast_stretch_normal(self):
        # Range [50, 150] should stretch to [0, 255]
        img = np.array([[50, 100], [100, 150]], dtype=np.uint8)
        stretched = linear_contrast_stretch(img)
        self.assertEqual(stretched.dtype, np.uint8)
        self.assertEqual(stretched.min(), 0)
        self.assertEqual(stretched.max(), 255)

    def test_linear_contrast_stretch_flat_image(self):
        # Completely flat image should return copy without crashing
        img = np.full((10, 10), 128, dtype=np.uint8)
        stretched = linear_contrast_stretch(img)
        np.testing.assert_array_equal(stretched, img)

    def test_percentile_contrast_stretch(self):
        img = np.arange(256, dtype=np.uint8).reshape((16, 16))
        stretched = percentile_contrast_stretch(img, p_low=1.0, p_high=1.0)
        self.assertEqual(stretched.dtype, np.uint8)
        self.assertEqual(stretched.shape, img.shape)


class TestHistogramEqualization(unittest.TestCase):
    def test_global_he(self):
        img = np.random.randint(50, 100, size=(64, 64), dtype=np.uint8)
        he = global_histogram_equalization(img)
        self.assertEqual(he.dtype, np.uint8)
        self.assertEqual(he.shape, img.shape)
        # Global HE expands dynamic range, std dev should increase
        self.assertGreater(np.std(he), np.std(img))

    def test_global_he_flat(self):
        img = np.full((32, 32), 100, dtype=np.uint8)
        he = global_histogram_equalization(img)
        self.assertEqual(he.dtype, np.uint8)
        self.assertEqual(he.shape, img.shape)


class TestAHEAndCLAHE(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.test_img = np.random.randint(40, 120, size=(128, 128), dtype=np.uint8)

    def test_clahe_grid_dimensions_and_type(self):
        clahe = CLAHEGrid(tile_grid_size=(8, 8), clip_limit=3.0)
        out = clahe.apply(self.test_img)
        self.assertEqual(out.dtype, np.uint8)
        self.assertEqual(out.shape, self.test_img.shape)
        self.assertTrue(0 <= out.min() <= out.max() <= 255)

    def test_clahe_non_square_image(self):
        rect_img = np.random.randint(30, 150, size=(100, 160), dtype=np.uint8)
        clahe = CLAHEGrid(tile_grid_size=(4, 8), clip_limit=2.5)
        out = clahe.apply(rect_img)
        self.assertEqual(out.shape, (100, 160))
        self.assertEqual(out.dtype, np.uint8)

    def test_ahe_grid(self):
        # AHE has no clip limit (clip_limit=None)
        ahe = AHEGrid(tile_grid_size=(4, 4))
        out = ahe.apply(self.test_img)
        self.assertEqual(out.dtype, np.uint8)
        self.assertEqual(out.shape, self.test_img.shape)

    def test_adaptive_histogram_equalization_helper(self):
        out = adaptive_histogram_equalization(self.test_img, tile_grid_size=(4, 4))
        self.assertEqual(out.dtype, np.uint8)
        self.assertEqual(out.shape, self.test_img.shape)

    def test_clahe_sliding_window(self):
        clahe_sw = CLAHECửaSổTrượt(block_size=31, clip_limit=3.0, stride=4)
        out = clahe_sw.apply(self.test_img)
        self.assertEqual(out.dtype, np.uint8)
        self.assertEqual(out.shape, self.test_img.shape)

    def test_local_histogram_equalization_helper(self):
        out = local_histogram_equalization(self.test_img, block_size=31, stride=4)
        self.assertEqual(out.dtype, np.uint8)
        self.assertEqual(out.shape, self.test_img.shape)

    def test_contrast_limiting_effect_on_noise(self):
        # A uniform region with slight noise: CLAHE should produce less noise than pure AHE
        noisy_flat = np.full((64, 64), 100, dtype=np.float32) + np.random.normal(0, 2, (64, 64))
        noisy_flat = np.clip(noisy_flat, 0, 255).astype(np.uint8)
        
        ahe_out = adaptive_histogram_equalization(noisy_flat, tile_grid_size=(4, 4))
        clahe_out = CLAHEGrid(tile_grid_size=(4, 4), clip_limit=1.5).apply(noisy_flat)
        
        noise_ahe = compute_flat_region_noise(ahe_out)
        noise_clahe = compute_flat_region_noise(clahe_out)
        # CLAHE with clip_limit=1.5 must suppress noise amplification compared to unclipped AHE
        self.assertLessEqual(noise_clahe, noise_ahe)


class TestColorProcessing(unittest.TestCase):
    def test_color_enhancement_preserves_channels(self):
        color_img = np.zeros((64, 64, 3), dtype=np.uint8)
        color_img[:, :, 0] = 50   # R
        color_img[:, :, 1] = 100  # G
        color_img[:, :, 2] = 150  # B
        
        clahe = CLAHEGrid(tile_grid_size=(4, 4), clip_limit=2.0)
        enhanced_color = process_color_image(color_img, clahe.apply)
        
        self.assertEqual(enhanced_color.dtype, np.uint8)
        self.assertEqual(enhanced_color.shape, color_img.shape)


class TestQuantitativeMetrics(unittest.TestCase):
    def setUp(self):
        self.img1 = np.full((64, 64), 100, dtype=np.uint8)
        self.img2 = np.full((64, 64), 120, dtype=np.uint8)

    def test_psnr_identical(self):
        psnr = compute_psnr(self.img1, self.img1)
        self.assertEqual(psnr, 100.0)

    def test_ssim_identical(self):
        ssim = compute_ssim(self.img1, self.img1)
        self.assertAlmostEqual(ssim, 1.0, places=4)

    def test_ambe(self):
        ambe = compute_ambe(self.img1, self.img2)
        self.assertAlmostEqual(ambe, 20.0, places=4)

    def test_entropy(self):
        # Completely uniform image has 0 entropy
        entropy = compute_entropy(self.img1)
        self.assertAlmostEqual(entropy, 0.0, places=4)

    def test_compute_all_metrics(self):
        metrics = compute_all_metrics(self.img1, self.img2, exec_time_ms=10.0)
        expected_keys = {'Entropy', 'RMS Contrast', 'AMBE', 'EME', 'PSNR (dB)', 'SSIM', 'Noise Std', 'Exec Time (ms)'}
        self.assertEqual(set(metrics.keys()), expected_keys)


if __name__ == '__main__':
    unittest.main()
