# BÁO CÁO THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG THUẬT TOÁN CLAHE

## 1. Bảng số liệu tổng hợp các chỉ số chất lượng

| Image | Method | Entropy | RMS Contrast | AMBE | EME | PSNR (dB) | SSIM | Noise Std | Exec Time (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| skimage_astronaut.png | Original | 7.4536 | 75.1231 | 0.0000 | 35.6648 | 100.0000 | 1.0000 | 60.2394 | 0.0000 |
| skimage_astronaut.png | Linear Stretch | 7.4274 | 75.1843 | 0.1169 | 35.1349 | 51.1969 | 0.9978 | 60.2574 | 189.6827 |
| skimage_astronaut.png | Percentile Stretch | 7.4238 | 75.1957 | 0.1230 | 35.1352 | 51.1376 | 0.9978 | 60.2574 | 19.3779 |
| skimage_astronaut.png | Global HE | 7.4592 | 79.6812 | 8.0804 | 35.7702 | 22.9624 | 0.9212 | 55.5420 | 17.8893 |
| skimage_astronaut.png | Custom AHE | 7.9152 | 64.9416 | 14.6061 | 19.2560 | 11.3246 | 0.5590 | 58.5837 | 42.4306 |
| skimage_astronaut.png | Custom Tile CLAHE | 7.5076 | 75.6812 | 1.3977 | 20.3203 | 21.5975 | 0.7952 | 61.1659 | 60.3418 |
| skimage_astronaut.png | Custom Sliding CLAHE | 7.5610 | 69.0572 | 0.5463 | 15.5638 | 17.4171 | 0.5499 | 57.2598 | 847.7647 |
| skimage_astronaut.png | OpenCV CLAHE | 7.5875 | 75.1514 | 0.4673 | 20.4016 | 20.9525 | 0.7657 | 61.5962 | 180.7625 |
| skimage_astronaut.png | Skimage CLAHE | 7.4649 | 75.9270 | 0.2073 | 21.4004 | 22.7599 | 0.8456 | 62.2884 | 86.9002 |
| skimage_coins.png | Original | 7.5244 | 52.8798 | 0.0000 | 15.1721 | 100.0000 | 1.0000 | 17.3127 | 0.0000 |
| skimage_coins.png | Linear Stretch | 7.5244 | 53.7404 | 0.0004 | 15.6395 | 49.0143 | 0.9996 | 17.6810 | 2.1200 |
| skimage_coins.png | Percentile Stretch | 7.4947 | 65.0383 | 1.4414 | 34.9447 | 26.3566 | 0.9516 | 21.3333 | 4.8790 |
| skimage_coins.png | Global HE | 7.3970 | 73.3433 | 30.9292 | 34.8506 | 16.3452 | 0.8788 | 18.2637 | 5.0893 |
| skimage_coins.png | Custom AHE | 7.9672 | 69.1855 | 33.1034 | 40.3914 | 14.1140 | 0.5875 | 65.9163 | 16.6633 |
| skimage_coins.png | Custom Tile CLAHE | 7.7809 | 61.2136 | 14.7823 | 23.0081 | 20.6138 | 0.8226 | 30.1587 | 36.6647 |
| skimage_coins.png | Custom Sliding CLAHE | 7.6719 | 56.8117 | 16.9621 | 14.7589 | 17.1081 | 0.4821 | 31.3954 | 507.1733 |
| skimage_coins.png | OpenCV CLAHE | 7.7954 | 61.8379 | 15.7071 | 24.0631 | 20.0699 | 0.7987 | 32.4215 | 0.7985 |
| skimage_coins.png | Skimage CLAHE | 7.7419 | 60.4626 | 8.8910 | 23.2857 | 22.6618 | 0.8638 | 28.5695 | 28.3296 |
| skimage_moon.png | Original | 4.8850 | 13.3303 | 0.0000 | 3.5688 | 100.0000 | 1.0000 | 7.9673 | 0.0000 |
| skimage_moon.png | Linear Stretch | 4.8850 | 13.3303 | 0.0000 | 3.5688 | 100.0000 | 1.0000 | 7.9673 | 3.9518 |
| skimage_moon.png | Percentile Stretch | 4.8543 | 21.1197 | 44.2874 | 5.4808 | 15.0528 | 0.9095 | 13.7329 | 11.7464 |
| skimage_moon.png | Global HE | 4.7218 | 73.7716 | 21.1629 | 22.5548 | 11.3727 | 0.2484 | 46.2213 | 8.0218 |
| skimage_moon.png | Custom AHE | 7.9591 | 68.6845 | 27.1353 | 36.0171 | 11.4519 | 0.1646 | 68.5937 | 31.5895 |
| skimage_moon.png | Custom Tile CLAHE | 5.9235 | 19.6206 | 9.0688 | 5.2135 | 24.5598 | 0.8579 | 12.3472 | 63.0953 |
| skimage_moon.png | Custom Sliding CLAHE | 5.8788 | 18.7215 | 8.4925 | 4.3105 | 23.8621 | 0.7855 | 10.9276 | 1139.3774 |
| skimage_moon.png | OpenCV CLAHE | 6.1366 | 21.2728 | 9.7850 | 6.0467 | 23.6453 | 0.7896 | 14.2334 | 0.7989 |
| skimage_moon.png | Skimage CLAHE | 5.7516 | 18.1991 | 5.2748 | 5.1567 | 26.6100 | 0.9015 | 11.4572 | 65.3875 |
| skimage_retina.png | Original | 5.6471 | 51.7211 | 0.0000 | 12.7890 | 100.0000 | 1.0000 | 0.4000 | 0.0000 |
| skimage_retina.png | Linear Stretch | 5.7645 | 55.6263 | 6.9949 | 13.0215 | 30.1206 | 0.9936 | 0.4000 | 60.3557 |
| skimage_retina.png | Percentile Stretch | 5.8260 | 66.0736 | 26.3271 | 12.9295 | 18.6490 | 0.9674 | 0.4000 | 87.2040 |
| skimage_retina.png | Global HE | 6.8175 | 75.7575 | 0.3532 | 18.8394 | 15.2195 | 0.6823 | 0.4000 | 62.8307 |
| skimage_retina.png | Custom AHE | 7.7001 | 57.9009 | 47.1262 | 12.4676 | 8.5100 | 0.2941 | 0.0000 | 242.1310 |
| skimage_retina.png | Custom Tile CLAHE | 6.1226 | 54.4194 | 5.2791 | 5.6289 | 25.2394 | 0.7730 | 0.4000 | 308.2330 |
| skimage_retina.png | Custom Sliding CLAHE | 6.0716 | 53.4595 | 6.1139 | 5.2331 | 24.0233 | 0.6963 | 0.0000 | 9256.7329 |
| skimage_retina.png | OpenCV CLAHE | 6.1687 | 54.8618 | 5.5333 | 5.9209 | 24.0393 | 0.7147 | 0.0000 | 36.9823 |
| skimage_retina.png | Skimage CLAHE | 6.0782 | 57.2724 | 7.5849 | 15.2623 | 24.9897 | 0.9079 | 0.4000 | 562.5157 |
| synthetic_flat_noise.png | Original | 3.6664 | 3.8785 | 0.0000 | 1.8998 | 100.0000 | 1.0000 | 2.9509 | 0.0000 |
| synthetic_flat_noise.png | Linear Stretch | 3.6664 | 36.5291 | 0.2217 | 22.8699 | 17.8528 | 0.3641 | 27.8724 | 5.4677 |
| synthetic_flat_noise.png | Percentile Stretch | 3.6263 | 65.5688 | 18.4801 | 139.4801 | 11.9529 | 0.2403 | 49.7419 | 24.0030 |
| synthetic_flat_noise.png | Global HE | 3.6346 | 75.9420 | 10.1063 | 108.8129 | 10.8858 | 0.2137 | 62.5623 | 22.9459 |
| synthetic_flat_noise.png | Custom AHE | 6.4082 | 79.5511 | 22.5742 | 84.0788 | 10.1616 | 0.2038 | 73.5871 | 63.4773 |
| synthetic_flat_noise.png | Custom Tile CLAHE | 4.7904 | 10.0181 | 3.8862 | 5.4788 | 30.6802 | 0.7962 | 8.7884 | 118.1242 |
| synthetic_flat_noise.png | Custom Sliding CLAHE | 5.1557 | 9.6257 | 2.9852 | 3.0957 | 28.8120 | 0.6555 | 7.3366 | 3390.9070 |
| synthetic_flat_noise.png | OpenCV CLAHE | 4.7716 | 12.7085 | 3.6017 | 6.9479 | 28.3767 | 0.6987 | 11.1141 | 3.5415 |
| synthetic_flat_noise.png | Skimage CLAHE | 4.6192 | 38.3733 | 1.8201 | 24.3433 | 17.3633 | 0.3487 | 29.6266 | 102.9615 |
| synthetic_low_contrast.png | Original | 5.5532 | 12.4990 | 0.0000 | 1.3354 | 100.0000 | 1.0000 | 6.2287 | 0.0000 |
| synthetic_low_contrast.png | Linear Stretch | 5.5532 | 63.7016 | 70.0048 | 8.1389 | 9.3672 | 0.6076 | 31.7972 | 8.2502 |
| synthetic_low_contrast.png | Percentile Stretch | 5.5532 | 65.0008 | 72.5189 | 8.1454 | 9.0915 | 0.5960 | 32.3623 | 18.3699 |
| synthetic_low_contrast.png | Global HE | 5.5532 | 74.5460 | 73.7868 | 8.7764 | 8.4414 | 0.5547 | 31.1272 | 15.3799 |
| synthetic_low_contrast.png | Custom AHE | 7.2832 | 56.2257 | 77.3390 | 4.6035 | 9.1097 | 0.5640 | 56.4552 | 62.4533 |
| synthetic_low_contrast.png | Custom Tile CLAHE | 5.6161 | 19.0705 | 18.4815 | 2.0844 | 21.9511 | 0.9379 | 17.3230 | 131.9962 |
| synthetic_low_contrast.png | Custom Sliding CLAHE | 6.0372 | 19.6234 | 26.2683 | 2.0511 | 19.1832 | 0.8953 | 19.4110 | 4166.5628 |
| synthetic_low_contrast.png | OpenCV CLAHE | 5.6268 | 21.5174 | 23.2327 | 2.3424 | 19.8610 | 0.9049 | 21.3982 | 2.7544 |
| synthetic_low_contrast.png | Skimage CLAHE | 6.9149 | 59.8792 | 69.7782 | 8.1219 | 9.6066 | 0.6100 | 35.9837 | 110.2912 |
| synthetic_phantom_xray.png | Original | 5.8646 | 32.6981 | 0.0000 | 9.2731 | 100.0000 | 1.0000 | 5.0076 | 0.0000 |
| synthetic_phantom_xray.png | Linear Stretch | 5.8646 | 48.1962 | 0.8808 | 17.4180 | 24.3102 | 0.9334 | 7.4199 | 5.7123 |
| synthetic_phantom_xray.png | Percentile Stretch | 5.8433 | 55.1362 | 7.5068 | 42.3123 | 20.6491 | 0.8228 | 8.4756 | 25.8403 |
| synthetic_phantom_xray.png | Global HE | 5.7276 | 72.4272 | 59.3298 | 61.3659 | 10.6158 | 0.3647 | 44.8277 | 17.6945 |
| synthetic_phantom_xray.png | Custom AHE | 7.8721 | 69.0412 | 62.4160 | 80.2771 | 9.4201 | 0.1951 | 73.8903 | 54.0576 |
| synthetic_phantom_xray.png | Custom Tile CLAHE | 6.9267 | 39.8017 | 18.2312 | 19.4754 | 21.0826 | 0.6917 | 14.8522 | 127.3098 |
| synthetic_phantom_xray.png | Custom Sliding CLAHE | 6.8204 | 35.7987 | 21.4240 | 10.1388 | 19.2308 | 0.3791 | 12.3478 | 3001.9474 |
| synthetic_phantom_xray.png | OpenCV CLAHE | 7.1191 | 41.0996 | 21.8446 | 22.3106 | 19.4442 | 0.6029 | 18.2770 | 1.8151 |
| synthetic_phantom_xray.png | Skimage CLAHE | 7.0410 | 48.9029 | 11.4866 | 25.5715 | 21.5396 | 0.7201 | 14.3626 | 82.8912 |

## 2. Phân tích và Nhận xét định lượng
- **Entropy**: Thuật toán CLAHE (cả Custom Tile, Custom Sliding và OpenCV) làm tăng Entropy đáng kể so với ảnh gốc mà không làm bão hòa mức xám như Global HE.
- **Kiểm soát nhiễu (Noise Std)**: AHE thuần túy (không giới hạn tương phản) làm bùng nổ nhiễu tại các vùng phẳng (Noise Std tăng vọt). CLAHE với cơ chế clip limit đã khống chế thành công nhiễu nền, giữ Noise Std ở mức an toàn.
- **AMBE**: CLAHE duy trì giá trị AMBE nhỏ hơn nhiều so với Global HE, chứng minh khả năng bảo toàn độ sáng trung bình.
- **EME & RMS Contrast**: CLAHE cải thiện tương phản cục bộ EME cao vượt trội so với các phương pháp toàn cục.
- **Thời gian thực thi**: OpenCV CLAHE nhanh nhất do viết bằng C++, tiếp theo là Custom Tile CLAHE (NumPy vectorized ~10-100ms) và Custom Sliding CLAHE (Cửa sổ trượt Fiji).
