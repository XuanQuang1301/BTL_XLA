# BÀI TẬP LỚN XỬ LÝ ẢNH SỐ: TĂNG CƯỜNG ĐỘ TƯƠNG PHẢN CỤC BỘ BẰNG CLAHE

Học phần: Xử lý ảnh số (PTIT)  
Chủ đề: Nghiên cứu, cài đặt, thực nghiệm và đánh giá thuật toán CLAHE (Contrast Limited Adaptive Histogram Equalization) với Fiji/ImageJ làm nền tảng tham chiếu.  
Công cụ tham chiếu: Plugin Fiji/ImageJ Process -> Enhance Local Contrast (CLAHE) (Tác giả: Stephan Saalfeld).

---

## 1. Tổng quan Thuật toán và Nền tảng Tham chiếu Fiji

CLAHE (Contrast Limited Adaptive Histogram Equalization) là phương pháp tăng cường độ tương phản cục bộ mạnh mẽ, khắc phục các nhược điểm của Cân bằng Histogram toàn cục (Global HE) và AHE thông thường:
1. **Thích nghi cục bộ (Adaptive)**: Tính toán histogram trên từng vùng ngữ cảnh cục bộ (Contextual region) thay vì toàn bộ bức ảnh.
2. **Giới hạn tương phản (Contrast Limiting)**: Cắt chiều cao histogram tại ngưỡng clip limit và phân phối đều phần dư để chặn độ dốc của hàm biến đổi, hạn chế khuếch đại nhiễu ở các vùng nền đồng nhất.
3. **Nội suy song tuyến tính (Bilinear Interpolation)**: Loại bỏ hiệu ứng đường biên khối (blocking artifacts) giữa các ô liền kề.

---

## 2. Cấu trúc Thư mục Dự án

```text
BTL_XLA/
├── README.md                 # Tài liệu hướng dẫn dự án
├── requirements.txt          # Danh sách thư viện Python phụ thuộc
├── docs/                     # Quyển báo cáo và tài liệu lý thuyết
├── data/                     # Thư mục chứa dữ liệu ảnh kiểm thử
│   ├── synthetic_low_contrast.png
│   ├── synthetic_phantom_xray.png
│   ├── synthetic_flat_noise.png
│   ├── skimage_moon.png
│   ├── skimage_coins.png
│   ├── skimage_retina.png
│   └── skimage_astronaut.png
├── src/                      # Bộ mã nguồn Python cài đặt thuật toán
│   ├── __init__.py
│   ├── contrast_basic.py     # Min-Max, Percentile Saturation, Global HE
│   ├── clahe_tile.py         # CLAHE Tile-Grid + Bilinear Interpolation (Zuiderveld) + AHE
│   ├── clahe_sliding.py      # CLAHE Sliding Window (Cửa sổ trượt kiểu Fiji) + Local HE
│   ├── metrics.py            # 7 chỉ số kiểm thử định lượng (Entropy, RMS, AMBE, EME, PSNR, SSIM, Noise)
│   └── utils.py              # Helper load/save ảnh, chuyển màu LAB/HSV, vẽ đồ thị
├── tests/                    # Bộ kiểm thử tự động (Unit Tests)
│   └── test_algorithms.py    # 18 test cases kiểm thử các thuật toán và trường hợp biên
├── scripts/
│   └── download_samples.py   # Script khởi tạo/tải bộ ảnh kiểm thử
├── run_benchmark.py          # Script chạy kiểm thử tự động toàn bộ dự án
└── results/                  # Thư mục chứa kết quả thực nghiệm
    ├── processed_images/     # Ảnh đầu ra của các phương pháp
    ├── plots/                # Biểu đồ so sánh Side-by-side và Histogram
    ├── benchmark_results.csv # Bảng dữ liệu thô dạng CSV
    └── benchmark_summary.md  # Bảng tổng hợp báo cáo dạng Markdown
```

---

## 3. Hướng dẫn Cài đặt Môi trường

### 3.1. Yêu cầu Hệ thống
- **Python**: Phiên bản Python 3.8 trở lên.

### 3.2. Các bước cài đặt

**Bước 1: Mở Terminal / PowerShell tại thư mục dự án**

```bash
cd BTL_XLA
```

**Bước 2: (Tùy chọn) Tạo và kích hoạt môi trường ảo**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Bước 3: Cài đặt các thư viện phụ thuộc**

```bash
pip install -r requirements.txt
```

---

## 4. Hướng dẫn Chạy Chương trình

### 4.1. Cách 1: Chạy bộ Kiểm thử tự động (Unit Tests)
Để kiểm tra tính đúng đắn và sự toàn vẹn của tất cả các hàm thuật toán (18 test cases):

```bash
python -m unittest discover tests
```

### 4.2. Cách 2: Chạy toàn bộ Benchmark định lượng tự động (Khuyên dùng)
Để chạy toàn bộ quy trình kiểm thử từ khởi tạo dữ liệu, xử lý ảnh, tính toán 7 chỉ số định lượng đến xuất bảng báo cáo:

```bash
python run_benchmark.py
```

**Các bước hệ thống tự động thực thi**:
1. Tự động kiểm tra và tạo bộ ảnh thử nghiệm đa dạng trong thư mục `data/`.
2. Áp dụng 8 phương pháp tăng cường tương phản lên tất cả ảnh:
   - *Original Image*: Ảnh gốc.
   - *Linear Contrast Stretch*: Kéo giãn tuyến tính Min-Max.
   - *Percentile Stretch*: Kéo giãn 0.35% bão hòa (tương tự ImageJ Process -> Enhance Contrast).
   - *Global Histogram Equalization*: Cân bằng histogram toàn cục.
   - *Custom AHE*: Thuật toán Adaptive Histogram Equalization không cắt ngưỡng.
   - *Custom Tile CLAHE*: Thuật toán CLAHE Tile-Grid + Nội suy song tuyến tính cài đặt từ đầu.
   - *Custom Sliding CLAHE*: Thuật toán CLAHE Cửa sổ trượt cài đặt từ đầu (kiểu Fiji).
   - *OpenCV CLAHE*: Thuật toán CLAHE tối ưu của thư viện OpenCV (`cv2.createCLAHE`).
   - *Scikit-Image CLAHE*: Thuật toán CLAHE của thư viện Scikit-Image (`equalize_adapthist`).
3. Tính toán 7 chỉ số định lượng (Entropy, RMS Contrast, AMBE, EME, PSNR, SSIM, Noise Std) và đo thời gian thực thi (ms).
4. Xuất kết quả vào thư mục `results/`.

---

### 4.3. Cách 3: Tải/Khởi tạo riêng bộ ảnh thử nghiệm

```bash
python scripts/download_samples.py
```

---

### 4.4. Cách 4: Chạy trực tiếp từ môi trường IDE (VS Code / PyCharm)
1. Mở thư mục dự án trong VS Code hoặc PyCharm.
2. Chọn Trình thông dịch Python (Python Interpreter) đã cài đặt `requirements.txt`.
3. Mở file `run_benchmark.py` và nhấn nút **Run File**.

---

### 4.5. Cách 5: Tích hợp thư viện vào Code Python cá nhân

```python
import cv2
from src.contrast_basic import linear_contrast_stretch, global_histogram_equalization
from src.clahe_tile import CLAHEGrid, adaptive_histogram_equalization
from src.clahe_sliding import CLAHECửaSổTrượt, local_histogram_equalization
from src.metrics import compute_all_metrics
from src.utils import process_color_image

# 1. Đọc ảnh mức xám
img = cv2.imread("data/skimage_moon.png", cv2.IMREAD_GRAYSCALE)

# 2. Áp dụng Custom CLAHE Grid Tile
clahe_tile = CLAHEGrid(tile_grid_size=(8, 8), clip_limit=3.0)
img_enhanced = clahe_tile.apply(img)

# 3. Tính toán bộ 7 chỉ số định lượng
metrics = compute_all_metrics(img, img_enhanced, exec_time_ms=12.5)
print("Kết quả chỉ số định lượng:", metrics)

# 4. Xử lý ảnh màu RGB (dùng không gian màu LAB để tránh lệch màu)
img_color = cv2.imread("data/skimage_retina.png")
img_color_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
img_color_enhanced = process_color_image(img_color_rgb, clahe_tile.apply)
```

---

### 4.6. Cách 6: Kiểm chứng đối chứng thủ công trên phần mềm Fiji/ImageJ
Để so sánh kết quả giữa Python Code và phần mềm Fiji:
1. Mở phần mềm Fiji/ImageJ.
2. Chọn `File -> Open`, chọn một ảnh trong thư mục `data/` (ví dụ: `skimage_moon.png`).
3. Vào menu: `Process -> Enhance Local Contrast (CLAHE)`.
4. Nhập các tham số:
   - `blocksize`: 127
   - `histogram bins`: 256
   - `maximum slope`: 3
5. Nhấn `OK` và so sánh kết quả hình ảnh cũng như Histogram với file ảnh tương ứng trong `results/processed_images/`.

---

## 5. Hệ thống 7 Chỉ số Kiểm thử Định lượng (`metrics.py`)

| Chỉ số | Ý nghĩa và Công thức toán học | Tiêu chuẩn đánh giá |
| :--- | :--- | :--- |
| **Entropy ($H$)** | $H = -\sum p_r(r_k) \log_2 p_r(r_k)$ (Đo độ phong phú thông tin mức xám). | **Cao hơn** thể hiện thông tin chi tiết được khôi phục tốt hơn. |
| **RMS Contrast ($\sigma$)** | $\sigma = \sqrt{\frac{1}{MN}\sum (f(x,y) - \bar{f})^2}$ (Độ lệch chuẩn mức xám). | **Tăng vừa phải** thể hiện tương phản được nâng cao. |
| **AMBE** | $\text{AMBE} = \|\bar{I}_{out} - \bar{I}_{in}\|$ (Sai số giữ độ sáng trung bình). | **Càng nhỏ càng tốt** (tránh làm thay đổi độ sáng gốc). |
| **EME** | $\text{EME} = \frac{1}{k_1 k_2} \sum 20 \ln \frac{I_{max}}{I_{min} + \epsilon}$ (Tương phản cục bộ theo khối). | **Cao hơn** thể hiện tương phản chi tiết cục bộ bộc lộ rõ. |
| **PSNR (dB)** | Peak Signal-to-Noise Ratio so với ảnh gốc. | **Cao hơn** thể hiện độ trung thực cấu trúc tốt hơn. |
| **SSIM** | Structural Similarity Index (Độ tương đồng cấu trúc). | **Gần 1** thể hiện cấu trúc tự nhiên được bảo toàn. |
| **Noise Std** | Độ lệch chuẩn tại vùng phẳng/nền (Flat background ROI). | **Nhỏ hơn** chứng minh khả năng hạn chế khuếch đại nhiễu của CLAHE. |

---

## 6. Đọc Kết quả Thực nghiệm (`results/`)

Sau khi chạy xong lệnh `python run_benchmark.py`, các file kết quả sẽ được tạo tại thư mục `results/`:
1. **`results/benchmark_summary.md`**: Bảng tổng hợp số liệu hiển thị dưới dạng Markdown để trích xuất vào báo cáo Word (~30 trang).
2. **`results/benchmark_results.csv`**: Dữ liệu thô CSV chứa thông số thí nghiệm của tất cả các ảnh và phương pháp.
3. **`results/plots/`**: Các file ảnh biểu đồ so sánh Side-by-side kèm Histogram cho từng ảnh thử nghiệm (dạng `comparison_<tên_ảnh>.png`).
4. **`results/processed_images/`**: Toàn bộ ảnh đầu ra sau xử lý của từng phương pháp.

---

## 7. Kết luận cho Báo cáo Nhóm
- Thuật toán **CLAHE tự cài đặt (Custom Tile CLAHE)** cho kết quả tương đương **OpenCV CLAHE** và khớp với hành vi của **Plugin Fiji Enhance Local Contrast**.
- CLAHE vượt trội hoàn toàn so với Global HE nhờ khả năng **giữ độ sáng trung bình (AMBE thấp)**, **bảo toàn cấu trúc (SSIM cao)** và **không bị khuếch đại nhiễu hạt ở vùng phẳng (Noise Std được kiểm soát)**.
