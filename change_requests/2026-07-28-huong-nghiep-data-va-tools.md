# 📄 CR-001 — Bộ dữ liệu & Tool cho Agent Hướng nghiệp

| | |
| :-- | :-- |
| **Ngày** | 2026-07-28 |
| **Đề tài** | Chatbot Định hướng Sự nghiệp — gợi ý ngành/trường cho học sinh tốt nghiệp cấp 3 |
| **Phạm vi** | 2 bộ dữ liệu JSON + 8 tool tra cứu + 61 test |
| **Trạng thái** | ✅ Hoàn tất — 61/61 test pass |

---

## 1. Bối cảnh & Mục tiêu

Bài lab cần một ReAct Agent tra cứu được số liệu thật thay vì trả lời từ kiến thức tĩnh của LLM. Đề tài chọn: **hướng nghiệp** — học sinh cung cấp điểm thi, khối thi, vùng muốn học; agent tra **điểm chuẩn đại học** và đối chiếu với **xu hướng tuyển dụng** để gợi ý ngành/trường.

Hai câu hỏi agent phải trả lời được:
1. *"Em 27 điểm khối A01, muốn học IT ở miền Nam thì đỗ trường nào?"* → dữ liệu tuyển sinh
2. *"Học ngành đó ra có việc không?"* → dữ liệu xu hướng tuyển dụng

> ⚠️ **Toàn bộ dữ liệu là MÔ PHỎNG phục vụ học tập.** Tên trường có thật nhưng điểm chuẩn, chỉ tiêu, học phí và số liệu tuyển dụng đều là số giả lập — không dùng để quyết định nguyện vọng thật. Disclaimer được ghi trong `meta` của cả hai file và có test bắt buộc kiểm tra.

### Các file đã tạo/sửa

| File | Vai trò |
| :-- | :-- |
| `data/job_market_vn.json` | 🆕 Xu hướng tuyển dụng VN 2024–2025 (30 dòng) |
| `data/university_admissions_vn.json` | 🆕 Tuyển sinh đại học VN 2024–2025 (53 ngành) |
| `src/tools.py` | ✏️ 8 tool tra cứu + bộ nhận diện tham số tiếng Việt |
| `tests/test_tools.py` | 🆕 61 test (schema + hành vi tool + báo cáo registry) |

---

## 2. Data Schema

### 2.1. `data/job_market_vn.json` — Xu hướng tuyển dụng

Cấu trúc lồng 3 tầng: **năm → nhóm ngành → vùng miền**.

```
meta
years[]                     ← 2 năm: 2024, 2025
  └─ industries[]           ← 5 nhóm ngành
       └─ regions[]         ← 3 vùng miền  → 2 × 5 × 3 = 30 dòng
```

| Trường | Kiểu | Ý nghĩa |
| :-- | :-- | :-- |
| `job_postings` | int | Số tin tuyển dụng trong năm |
| `growth_pct` | float | % thay đổi so với **năm liền trước** (đã tính sẵn) |
| `trend` | str | Nhãn xu hướng suy ra từ `growth_pct` |

**Nhóm ngành:** IT - Phần mềm · Quản trị - Nhân sự · Kinh tế - Tài chính - Ngân hàng · Marketing - Truyền thông · Sản xuất - Cơ khí
**Vùng miền:** Miền Bắc · Miền Trung · Miền Nam

**Ngưỡng nhãn `trend`** (ghi trong `meta.trend_labels`):

| `growth_pct` | `trend` |
| :-- | :-- |
| ≥ 10% | tăng mạnh |
| 3% ~ 10% | tăng |
| −3% ~ 3% | ổn định |
| −10% ~ −3% | giảm |
| < −10% | giảm mạnh |

**Ví dụ một dòng:**

```json
{ "region": "Miền Nam", "job_postings": 25400, "growth_pct": 13.4, "trend": "tăng mạnh" }
```

**Quy ước quan trọng — trend tính sẵn (pre-calculated):** `growth_pct` không phải số ngẫu nhiên mà **suy ra từ `job_postings` của hai năm**. Agent chỉ đọc, không phải tự tính. Có test khoá lại ràng buộc này.

---

### 2.2. `data/university_admissions_vn.json` — Tuyển sinh đại học

Cấu trúc lồng 3 tầng: **vùng miền → trường → ngành**.

```
meta
dimensions                  ← khối thi, loại trường, phương thức xét tuyển
regions[]                   ← 3 vùng
  └─ universities[]         ← 12 trường
       └─ majors[]          ← 53 ngành (3–5 ngành/trường)
```

**Cấp trường:**

| Trường | Kiểu | Ý nghĩa |
| :-- | :-- | :-- |
| `university_code` | str | Mã trường (BKA, NEU, UIT…), duy nhất toàn dataset |
| `university_name`, `city`, `type` | str | Tên đầy đủ, thành phố, loại hình |
| `admission_methods` | list | Phương thức xét tuyển (phải thuộc `dimensions`) |
| `tuition_million_vnd_per_year` | int | Học phí (triệu VNĐ/năm) — dùng để lọc theo ngân sách |

**Cấp ngành:**

| Trường | Kiểu | Ý nghĩa |
| :-- | :-- | :-- |
| `major_name`, `major_code` | str | Tên & mã ngành (mã duy nhất trong cùng trường) |
| `exam_blocks` | list | Tổ hợp xét tuyển (A00, A01, B00, C00, D01, D07) |
| `benchmark_2024` / `benchmark_2025` | float | Điểm chuẩn, thang 30 |
| `benchmark_change` | float | `benchmark_2025 − benchmark_2024` (tính sẵn) |
| `benchmark_trend` | str | tăng / ổn định / giảm |
| `competition_level` | str | rất cao / cao / trung bình / dễ thở |
| `quota_2025` | int | Chỉ tiêu |
| `note` | str | Gợi ý ngắn: ngành này hợp với ai |

**Ngưỡng suy ra (ghi trong `meta`):**

| `benchmark_change` | `benchmark_trend` | | `benchmark_2025` | `competition_level` |
| :-- | :-- | :-- | :-- | :-- |
| ≥ +0.3 | tăng | | ≥ 27 | rất cao |
| −0.3 ~ +0.3 | ổn định | | 24 ~ 27 | cao |
| ≤ −0.3 | giảm | | 20 ~ 24 | trung bình |
| | | | < 20 | dễ thở |

**12 trường:**

| Vùng | Trường |
| :-- | :-- |
| Miền Bắc (5) | BKA · NEU · UET · BAV · TMU |
| Miền Trung (3) | DDK · DDQ · DHT |
| Miền Nam (4) | QSB · UIT · UEH · TCT |

**Nguyên tắc phủ điểm:** mỗi vùng đều có ngành **dưới 21 điểm** và ngành **từ 26 điểm trở lên** → học sinh ở bất kỳ mức điểm nào cũng nhận được gợi ý, không rơi vào kết quả rỗng. Dải điểm toàn dataset: **16.8 → 28.8**; học phí: **13 → 60 triệu/năm**.

---

### 2.3. Nối 2 bộ dữ liệu

Hai file độc lập về mặt lưu trữ (không có khóa ngoại). Việc nối thực hiện **ở tầng tool**: hàm `_major_group()` gom 53 ngành đào tạo về đúng 5 nhóm ngành của bộ dữ liệu tuyển dụng.

| Nhóm ngành | Số ngành đào tạo |
| :-- | --: |
| Sản xuất - Cơ khí | 13 |
| IT - Phần mềm | 12 |
| Kinh tế - Tài chính - Ngân hàng | 11 |
| Quản trị - Nhân sự | 6 |
| Ngành khác | 6 |
| Marketing - Truyền thông | 5 |

`Ngành khác` gồm 6 ngành không thuộc 5 nhóm trên: Sư phạm Toán học, Ngôn ngữ Anh, Công nghệ sinh học, Kỹ thuật môi trường, Nông học, Nuôi trồng thủy sản.

---

## 3. Tools List & Description

8 tool đăng ký trong `AVAILABLE_TOOLS` (`src/tools.py`). Mọi tool **trả về `str`** để ReAct loop ghép thẳng vào Observation, và **báo lỗi bằng chuỗi mở đầu `LỖI:`** kèm danh sách giá trị hợp lệ thay vì raise exception — giúp agent tự sửa tham số ở vòng lặp sau.

### 3.1. Nhóm A — Xu hướng tuyển dụng

| # | Tool | Chữ ký | Mô tả |
| :-: | :-- | :-- | :-- |
| 1 | `get_job_market_trend` | `(industry, region, year=2025)` | Xu hướng tuyển dụng của **1 ngành tại 1 vùng** trong một năm |
| 2 | `compare_regions_by_industry` | `(industry, year=2025)` | So sánh **1 ngành trên cả 3 vùng**, xếp hạng theo tăng trưởng |
| 3 | `get_top_industries_by_region` | `(region, year=2025)` | Xếp hạng **5 nhóm ngành tại 1 vùng** theo tăng trưởng |
| 4 | `list_job_market_options` | `()` | Liệt kê năm / nhóm ngành / vùng hợp lệ |

### 3.2. Nhóm B — Tuyển sinh đại học

| # | Tool | Chữ ký | Mô tả |
| :-: | :-- | :-- | :-- |
| 5 | `get_admission_by_university` | `(university, year=2025)` | Điểm chuẩn & xu hướng **tất cả ngành của 1 trường** |
| 6 | `get_admission_by_region` | `(region, year=2025)` | Mặt bằng điểm & xu hướng **tất cả trường trong 1 vùng** |
| 7 | `get_admission_by_major_group` | `(major_group, region="", year=2025)` | Điểm chuẩn **1 nhóm ngành** toàn quốc hoặc lọc theo vùng |
| 8 | `list_admission_options` | `()` | Liệt kê năm / nhóm ngành / 12 trường theo vùng |

### 3.3. Nhận diện tham số tiếng Việt

Hàm `_norm()` bỏ dấu + chữ thường, `_match()` so khớp theo từ khoá với **alias dài được ưu tiên** để tránh nhầm chuỗi con.

| Người dùng gõ | Nhận diện thành |
| :-- | :-- |
| `it`, `cntt`, `phần mềm`, `lập trình`, `software` | IT - Phần mềm |
| `hn`, `hà nội`, `phía bắc`, `bắc ninh` | Miền Bắc |
| `hcm`, `sài gòn`, `bình dương`, `cần thơ` | Miền Nam |
| `bkhn`, `bách khoa hà nội` | Trường BKA |
| `bách khoa đà nẵng` / `bách khoa TP.HCM` | Trường DDK / QSB |

**Xử lý nhập nhằng:** `"bách khoa"` khớp 3 trường → trả lỗi liệt kê cả BKA, DDK, QSB để agent hỏi lại người dùng thay vì đoán bừa.

### 3.4. Ví dụ output

```
> get_admission_by_university("UIT", 2025)

Trường Đại học Công nghệ Thông tin - ĐHQG TP.HCM (UIT) - TP.HCM, Miền Nam
Loại hình: Công lập tự chủ | Học phí: 35 triệu/năm
Phương thức xét tuyển: Điểm thi THPT, Đánh giá năng lực, Xét tuyển thẳng
Điểm chuẩn 2025 (5 ngành, từ 26.1 đến 28.8 điểm):
1. Trí tuệ nhân tạo: 28.8 điểm (+0.5 📈 tăng) | khối A00/A01 | cạnh tranh rất cao | chỉ tiêu 100 | nhóm ngành: IT - Phần mềm
...
=> Xu hướng điểm chuẩn chung của trường: TĂNG (+0.32 điểm/ngành so với 2024)
```

```
> get_job_market_trend("IT", "TP.HCM", 2025)

Xu hướng tuyển dụng IT - Phần mềm tại Miền Nam năm 2025:
- Số tin tuyển dụng: 25.400 tin
- Thay đổi so với năm 2024: +13.4% 📈
- Đánh giá xu hướng: TĂNG MẠNH
```

---

## 4. Test Cases

File: `tests/test_tools.py` — dùng `unittest` (thư viện chuẩn), **không cần cài thêm dependency**.

```bash
.venv/Scripts/python.exe tests/test_tools.py          # in báo cáo tool + chạy test
.venv/Scripts/python.exe -m unittest discover tests   # chỉ chạy test
```

Khi chạy trực tiếp, `print_tool_report()` đọc `AVAILABLE_TOOLS` bằng `inspect` và in bảng tool + chữ ký + mô tả tham số — **báo cáo sinh từ code nên không bao giờ lệch với thực tế**.

### 4.1. `TestToolRegistry` — 7 test

Kiểm tra chất lượng khai báo tool, vì agent chỉ dùng đúng tool khi description đủ rõ.

| Test | Nội dung |
| :-- | :-- |
| `test_dang_ky_du_8_tool` | Registry đúng 8 tool như thiết kế |
| `test_moi_tool_deu_callable` | Mọi giá trị trong registry gọi được |
| `test_key_registry_trung_ten_ham` | Key trùng `__name__` — tránh agent gọi đúng tên nhưng chạy nhầm hàm |
| `test_moi_tool_co_docstring_du_dai` | Docstring ≥ 60 ký tự |
| `test_docstring_mo_ta_gia_tri_tra_ve` | Docstring có mục `Returns:` |
| `test_tool_co_tham_so_phai_mo_ta_args` | Có `Args:` và **mô tả đủ từng tham số** |
| `test_moi_tool_tra_ve_chuoi` | Mọi tool trả `str` (yêu cầu của ReAct loop) |

### 4.2. `TestJobMarketSchema` — 6 test

| Test | Nội dung |
| :-- | :-- |
| `test_co_dung_30_row` | Đúng 30 dòng dữ liệu |
| `test_cau_truc_nam_nganh_vung` | 2 năm × 5 ngành × 3 vùng |
| `test_moi_row_du_truong_bat_buoc` | Đủ `job_postings` / `growth_pct` / `trend`, số tin > 0 |
| `test_growth_pct_2025_khop_so_lieu_2_nam` | ⭐ `growth_pct` khớp tuyệt đối với `job_postings` hai năm |
| `test_nhan_trend_khop_nguong` | Nhãn `trend` khớp ngưỡng % |
| `test_meta_ghi_ro_disclaimer_du_lieu_mo_phong` | Có disclaimer + `row_count` khớp số đếm |

### 4.3. `TestAdmissionsSchema` — 12 test

| Test | Nội dung |
| :-- | :-- |
| `test_quy_mo_3_vung_12_truong_53_nganh` | Đúng quy mô thiết kế |
| `test_meta_khop_so_dem_thuc_te` | `meta.university_count` / `major_row_count` khớp dữ liệu |
| `test_diem_chuan_nam_trong_thang_30` | Mọi điểm nằm trong [15.0, 30.0] |
| `test_benchmark_change_khop_hieu_2_nam` | ⭐ `benchmark_change` = hiệu 2 năm |
| `test_benchmark_trend_khop_nguong` | Nhãn trend khớp ngưỡng ±0.3 |
| `test_competition_level_khop_diem_2025` | Mức cạnh tranh khớp ngưỡng điểm |
| `test_khoi_thi_ton_tai_trong_dimensions` | Mọi khối thi hợp lệ |
| `test_loai_truong_va_phuong_thuc_xet_tuyen_hop_le` | Loại trường & phương thức thuộc `dimensions` |
| `test_ma_truong_khong_trung` | 12 mã trường duy nhất |
| `test_ma_nganh_khong_trung_trong_cung_truong` | Mã ngành duy nhất trong mỗi trường |
| `test_moi_vung_phu_du_dai_diem` | ⭐ Mỗi vùng có ngành < 21 và ≥ 26 điểm |
| `test_meta_ghi_ro_disclaimer_du_lieu_mo_phong` | Có disclaimer dữ liệu mô phỏng |

### 4.4. `TestJobMarketTools` — 14 test

**🟢 Đơn giản (3):** `test_tra_cuu_dung_so_lieu` · `test_nam_2024_so_sanh_voi_2023` · `test_year_mac_dinh_la_2025`

**🟡 Nhận diện tham số (3):** `test_alias_nganh` · `test_alias_vung_mien` · `test_alias_dai_duoc_uu_tien` *(chống nhầm `"miền nam"` do chứa chuỗi con của alias khác)*

**🟡 Multi-step (3):** `test_so_sanh_3_vung_sap_xep_giam_dan` · `test_xep_hang_du_5_nganh_trong_1_vung` · `test_list_options_liet_ke_du_gia_tri`

**🔴 Edge case / Guardrail (5):**

| Test | Đầu vào bẫy | Kỳ vọng |
| :-- | :-- | :-- |
| `test_nganh_khong_ton_tai` | `"Thời trang"` | `LỖI:` + liệt kê 5 nhóm ngành |
| `test_vung_khong_ton_tai` | `"Atlantis"` | `LỖI:` + liệt kê 3 vùng |
| `test_nam_ngoai_dai_du_lieu` | `2030` | `LỖI:` + "2024, 2025" |
| `test_nam_khong_phai_so` | `"ngày 32/13/2026"` | `LỖI:` không crash |
| `test_tham_so_rong` | `""` | `LỖI:` |

### 4.5. `TestAdmissionTools` — 18 test

**🟢 Theo trường (3):** `test_tra_cuu_theo_truong` · `test_nganh_trong_truong_sap_xep_diem_giam_dan` · `test_alias_truong`

**🟢 Theo vùng (2):** `test_tra_cuu_theo_vung` · `test_truong_trong_vung_sap_xep_theo_diem_cao_nhat`

**🟢 Theo nhóm ngành (4):** `test_tra_cuu_theo_nhom_nganh_toan_quoc` · `test_loc_nhom_nganh_theo_vung` · `test_nhan_dien_nhom_nganh_theo_tu_khoa_nguoi_dung` · `test_nhom_nganh_khac`

**🟡 Xử lý năm cũ (3):** ⭐ `benchmark_change` và `competition_level` được tính theo năm 2025 — không được gán cho năm 2024.

| Test | Nội dung |
| :-- | :-- |
| `test_nam_2024_khong_hien_chi_so_cua_2025` | Tra 2024 → **không** hiện "cạnh tranh"/"Xu hướng chung" |
| `test_nam_2025_hien_day_du_chi_so` | Tra 2025 → hiện đầy đủ, có "so với 2024" |
| `test_bao_cao_vung_nam_2024_khong_co_dong_bien_dong` | Báo cáo vùng năm 2024 không có dòng "Biến động" |

**🔴 Edge case / Guardrail (6):**

| Test | Đầu vào bẫy | Kỳ vọng |
| :-- | :-- | :-- |
| `test_ten_truong_nhap_nhang` | `"bách khoa"` | `LỖI:` + liệt kê BKA, DDK, QSB |
| `test_truong_khong_ton_tai` | `"Đại học Harvard"` | `LỖI:` + gợi ý gọi `list_admission_options` |
| `test_nhom_nganh_khong_ton_tai` | `"Thời trang"` | `LỖI:` |
| `test_vung_khong_ton_tai` | `"Atlantis"` | `LỖI:` (cả 2 tool) |
| `test_nam_ngoai_dai_du_lieu` | `2030` | `LỖI:` (cả 3 tool) |
| `test_list_options_liet_ke_du_12_truong` | — | Liệt kê đủ 12 mã trường |

### 4.6. `TestCrossDataset` — 4 test

| Test | Nội dung |
| :-- | :-- |
| `test_nhom_nganh_tuyen_sinh_trung_ten_nhom_nganh_tuyen_dung` | Nhóm ngành tuyển sinh ⊆ nhóm ngành tuyển dụng ∪ {Ngành khác} |
| `test_moi_nhom_nganh_chinh_deu_co_nganh_dao_tao` | Cả 5 nhóm ngành đều có ngành đào tạo tương ứng |
| `test_gom_nhom_nganh_dung` | Kiểm tra mapping 10 ngành cụ thể |
| `test_kich_ban_huong_nghiep_day_du` | ⭐ Kịch bản đầu-cuối: học sinh 27 điểm A01 → tra điểm chuẩn IT miền Nam → tra xu hướng tuyển dụng IT miền Nam |

---

## 5. Test Report

```
$ .venv/Scripts/python.exe -m unittest discover tests

.............................................................
----------------------------------------------------------------------
Ran 61 tests in 0.044s

OK
```

| Nhóm test | Số test | Kết quả |
| :-- | --: | :-- |
| `TestToolRegistry` | 7 | ✅ pass |
| `TestJobMarketSchema` | 6 | ✅ pass |
| `TestAdmissionsSchema` | 12 | ✅ pass |
| `TestJobMarketTools` | 14 | ✅ pass |
| `TestAdmissionTools` | 18 | ✅ pass |
| `TestCrossDataset` | 4 | ✅ pass |
| **Tổng** | **61** | **✅ 61 pass / 0 fail** |

### Bug phát hiện & đã sửa trong quá trình test

| # | Bug | Nguyên nhân | Cách sửa |
| :-: | :-- | :-- | :-- |
| 1 | `get_admission_by_major_group("IT")` trả `LỖI: không nhận diện được nhóm ngành` | Dict nhóm ngành chỉ chứa tên ngành đào tạo, không có từ khoá người dùng gõ | Dùng lại `_INDUSTRY_ALIASES` (tên 5 nhóm ngành trùng nhau giữa 2 dataset) để parse input |
| 2 | Tra `year=2024` vẫn hiện `competition_level` và "xu hướng chung" | Hai chỉ số này tính theo điểm 2025, gán nhầm cho năm 2024 → **số liệu sai** | Chỉ hiển thị khi `year` là năm mới nhất; đã khoá bằng 3 test |
| 3 | Docstring tiếng Việt vỡ font khi chạy test | `unittest` in ra `stderr` chưa set UTF-8 trên Windows Console | Reconfigure cả `stdout` và `stderr` sang UTF-8 |

---

## 6. Việc còn lại (ngoài phạm vi CR này)

| # | Việc | Lý do |
| :-: | :-- | :-- |
| 1 | `src/app.py:22` vẫn `import get_weather, search_flights` | Hai tool demo cũ đã bị xoá khỏi `tools.py` → chạy app sẽ `ImportError` |
| 2 | `src/prompts.py` — `REACT_SYSTEM_PROMPT` còn mô tả `get_weather` / `search_flights` | Cần thay bằng 8 tool mới để agent biết gọi gì |
| 3 | `config/test_cases.json` còn 5 test case chủ đề thời tiết/vé máy bay | Cần viết lại theo đề tài hướng nghiệp |
| 4 | Chưa có tool `recommend_universities(điểm, khối, vùng, ngân sách)` | Tool gợi ý tổng hợp — sẽ làm ở CR sau |
