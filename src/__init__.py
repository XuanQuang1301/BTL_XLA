"""
Package BTL XLA: Contrast Enhancement and CLAHE Implementation
Reference Framework: Fiji / ImageJ
"""

from .contrast_basic import linear_contrast_stretch, percentile_contrast_stretch, global_histogram_equalization
from .clahe_tile import CLAHEGrid, AHEGrid, adaptive_histogram_equalization
from .clahe_sliding import CLAHECửaSổTrượt, local_histogram_equalization
from .metrics import compute_all_metrics
from .utils import load_image, save_image, process_color_image

__all__ = [
    'linear_contrast_stretch',
    'percentile_contrast_stretch',
    'global_histogram_equalization',
    'CLAHEGrid',
    'AHEGrid',
    'adaptive_histogram_equalization',
    'CLAHECửaSổTrượt',
    'local_histogram_equalization',
    'compute_all_metrics',
    'load_image',
    'save_image',
    'process_color_image'
]
