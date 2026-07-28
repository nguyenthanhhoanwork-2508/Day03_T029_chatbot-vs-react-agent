# 🧾 SPEC BÀN GIAO — LA BÀN NGUYỆN VỌNG

> **Bàn giao 3/4** (theo `docs/PROMPT_THIET_KE_UI_UX.md` §9.3)
> Dành cho **Role 4 (Integrator)** dựng `src/app.py` trên Streamlit.
> Đọc kèm: [UI_FLOW.md](UI_FLOW.md) · [UI_WIREFRAME.md](UI_WIREFRAME.md) · [prototype/la-ban-nguyen-vong.html](prototype/la-ban-nguyen-vong.html)
>
> Spec tốt là spec mà dev không phải hỏi lại câu nào. Chỗ nào cố ý không làm thì ghi ở [§9 Ngoài phạm vi](#9-ngoài-phạm-vi) — để phân biệt "chưa nghĩ tới" với "đã nghĩ và quyết định không làm".

---

## 1. Token

### 1.1. Màu nền tảng

| Vai trò | Tên | Sáng | Tối | Tương phản trên nền của nó |
| :--- | :--- | :--- | :--- | :---: |
| Nền trang | Nền | `#FFFFFF` | `#101827` | — |
| Nền khối phụ | Nền phụ | `#F7F9FC` | `#18202F` | — |
| Chữ chính | Navy Tri Thức | `#0F1E3D` | `#E8ECF3` | 16.8 : 1 · 13.9 : 1 |
| Chữ phụ | Xám Ghi Chú | `#5B6472` | `#9AA5B8` | **5.98 : 1** · 7.4 : 1 |
| Viền | Xám Viền | `#E3E6EB` | `#2A3446` | — |
| Màu nhấn | Xanh La Bàn | `#2563EB` | `#60A5FA` | **5.17 : 1** · 8.1 : 1 |
| Nền màu nhấn nhạt | | `#EFF4FE` | `#1B2942` | — |

> Nền tối là **`#101827` (navy sẫm), không phải đen tuyệt đối** — đen tuyệt đối làm viền bị chói. Màu nhấn ở chế độ tối giảm bão hoà (`#2563EB` → `#60A5FA`) vì màu rực trên nền tối gây mỏi mắt.

### 1.2. Màu nghiệp vụ — khoá cứng

**Tuyệt đối không dùng cho mục đích khác.** Không có màu "xanh lá cho thành công" nào khác trong sản phẩm này — xanh lá chỉ có nghĩa **An toàn**.

| Nhóm | Sáng | Tối | Icon | Chữ | Tương phản (sáng) |
| :--- | :--- | :--- | :---: | :--- | :---: |
| An toàn | `#157F3D` | `#4ADE80` | `●` | "An toàn" | **5.08 : 1** |
| Vừa tầm | `#B45309` | `#FBBF24` | `◐` | "Vừa tầm" | **5.02 : 1** |
| Liều | `#B42318` | `#F87171` | `▲` | "Liều" | **6.57 : 1** |
| Ngoài tầm | `#64748B` | `#94A3B8` | `○` | "Ngoài tầm" | **4.76 : 1** |

Ba yếu tố **màu + icon + chữ tiếng Việt** luôn đi cùng nhau, không tách. Kiểm nhanh: chụp màn hình rồi chuyển sang đen trắng — nếu vẫn phân biệt được nhóm rủi ro thì đạt.

Màu luồng vận hành (cổng Tư vấn) **dùng lại đúng 3 giá trị này**: 🟢 Xanh = `#157F3D`, 🟡 Vàng = `#B45309`, 🔴 Đỏ = `#B42318`. Không sinh thêm bảng màu thứ hai.

### 1.3. Chữ

```
Font  UI      Be Vietnam Pro → Inter → "Segoe UI" → system-ui → sans-serif
Font  trace   JetBrains Mono → Consolas → "Courier New" → monospace
Cỡ            13 / 16 / 20 / 26 / 34        (nội dung 16 · màn chiếu ≥ 20)
Đậm           400 thường · 500 nhấn · 600 tiêu đề
Dòng          1.55 nội dung · 1.25 tiêu đề
```

> ⚠️ **Prototype HTML dùng font hệ thống, không tải Be Vietnam Pro.** Ràng buộc "không tải tài nguyên từ ngoài" thắng. Trên Windows `Segoe UI` có đủ dấu tiếng Việt. Nếu bản chính thức muốn Be Vietnam Pro thì phải **tự host**, không dùng Google Fonts CDN.
>
> Riêng màn hình **Đối chứng (§14 wireframe)** dùng cỡ nền **20px** thay vì 16px — nó được chiếu lên máy chiếu và phải đọc được từ hàng ghế cuối.

### 1.4. Khoảng cách, bo góc, đổ bóng

```
Khoảng cách   4 · 8 · 12 · 16 · 24 · 32 · 48     ← đúng một thang, không có số lẻ
Bo góc        8px  thẻ nhỏ / nút / ô nhập
              16px thẻ lớn / thẻ nguyện vọng
              999px huy hiệu rủi ro, chip
Đổ bóng       nhẹ  0 1px 2px rgba(15,30,61,.06)
              nổi  0 4px 16px rgba(15,30,61,.10)
```

Đúng 2 mức bóng, không hơn. Chế độ tối: **bỏ bóng, thay bằng viền `#2A3446`** — bóng đen trên nền tối không nhìn thấy gì.

---

## 2. Thành phần cốt lõi — đủ 5 trạng thái

Một thành phần chưa xong cho tới khi cả 5 trạng thái đều có câu trả lời. Đây là bước bị bỏ nhiều nhất và tạo ra nhiều bug UX nhất.

### 2.1. Ô nhập chat + nút Gửi/Dừng

| | |
| :--- | :--- |
| **Vai trò** | Đường vào duy nhất của cổng HS |
| **Dữ liệu** | `noi_dung` — string — bắt buộc |
| **Rỗng** | Placeholder *"Nhắn cho anh/chị…"*. Nút gửi **mờ (opacity .4), vẫn hiện** — không ẩn hẳn. |
| **Đang tải** | Ô nhập vẫn gõ được (soạn câu tiếp theo). Nút gửi → `[⏹ Dừng]`, nền đỏ `#B42318`. |
| **Có dữ liệu** | Ô tự cao theo nội dung, trần **6 dòng** rồi cuộn trong ô. Nút gửi sáng đầy. |
| **Lỗi** | Gửi thất bại → dòng đỏ **dưới ô**, giữ nguyên chữ HS đã gõ. Tuyệt đối không xoá nội dung ô. |
| **Không quyền** | Không áp dụng — cổng HS không có trạng thái hết hạn. |
| **Bàn phím** | `Enter` gửi · `Shift+Enter` xuống dòng · `Esc` khi đang chạy = Dừng · `↑` khi ô rỗng = nạp lại câu vừa gửi |
| **Tiếp cận** | `<label>` ẩn bằng `.sr-only`, không dùng placeholder thay label |

### 2.2. Danh sách bước ReAct (phía HS)

| | |
| :--- | :--- |
| **Vai trò** | Biến hộp đen 8 giây thành thứ nhìn thấy được |
| **Dữ liệu** | `[{nhan_than_thien, trang_thai: cho\|dang\|xong\|loi, giay, ghi_chu}]` |
| **Rỗng** | Không render gì cả. Không hiện khung rỗng. |
| **Đang tải** | `<1s` không hiện gì · `1–3s` một dòng `⟳ Đang xử lý…` · `3–10s` danh sách bước có nhãn cụ thể · `>10s` thêm nút **Huỷ** nổi bật |
| **Có dữ liệu** | Xong → **tự thu gọn thành một dòng** `▸ Đã tra 3 nguồn dữ liệu (4,6s)`, bấm mở lại được |
| **Lỗi** | Bước lỗi: icon `✗` + nền đỏ nhạt + **nói hệ thống làm gì tiếp** (*"đang thử cách khác"* / *"đã bỏ qua bước này"*) |
| **Không quyền** | HS **không bao giờ** thấy tên tool, `Thought`, `Action Input`, số vòng lặp |

**Ánh xạ nhãn — bắt buộc, đây là bảng dịch mà Role 4 phải dùng:**

| Tool thật | Chữ hiện cho HS |
| :--- | :--- |
| `mbti_quick_assess` | Đang xem xu hướng của em |
| `find_majors_by_interest` | Đang tìm nhóm ngành hợp với em |
| `lookup_admission_scores` | Đang tra điểm chuẩn 3 năm gần nhất |
| `filter_universities` | Đang lọc trường theo điều kiện của em |
| `get_job_market_stats` | Đang xem nhu cầu tuyển dụng của ngành |
| `lookup_career_requirements` | Đang tra nghề này cần học gì |

### 2.3. Thẻ nhập điểm từng môn

| | |
| :--- | :--- |
| **Dữ liệu** | `diem_mon: {toan, ly, hoa, sinh, van, su, dia, anh}` — float — **chỉ môn đã thi**, mỗi môn `[0, 10]` |
| **Rỗng** | 6 ô mặc định hiện (Toán·Lý·Hoá·Sinh·Văn·Anh) + link `▸ Thêm môn Sử · Địa`. Nút `[[Tiếp tục]]` **mờ** cho tới khi đủ 3 môn ghép được ít nhất 1 tổ hợp. |
| **Đang tải** | Không áp dụng — `tinh_to_hop` là hàm cục bộ, chạy tức thì |
| **Có dữ liệu** | Sau `[[Tiếp tục]]`: hiện `Tổ hợp tốt nhất của em là **A00 — 24.5 điểm**` + `▸ Xem tổ hợp khác`. Thẻ đã gửi **khoá lại**, còn nút `[Sửa]`. |
| **Lỗi** | Môn ngoài `[0,10]` → viền ô đỏ + icon `▲` + chữ dưới đúng ô đó. Tổ hợp ra ngoài `[0,30]` → lỗi ở **dòng tổng**, không ở ô môn. **Không gọi tool.** Nút Tiếp tục mờ. |
| **Không quyền** | Không áp dụng |
| **Bàn phím** | `Tab` đi theo thứ tự đọc trái→phải trên→dưới · `Enter` trong ô cuối = `[[Tiếp tục]]` |
| **Mobile** | `inputmode="decimal"` · 2 ô/hàng thay vì 3 |

> ⚠️ **HS không tự chọn tổ hợp.** Xem [UI_FLOW.md §0b-1](UI_FLOW.md#0b-bốn-chỗ-tài-liệu-đá-nhau--đã-chốt). Hệ thống tính, hệ thống nói rõ đã chọn tổ hợp nào, HS đổi được sang tổ hợp khả dụng khác.

### 2.4. Thẻ nguyện vọng

| | |
| :--- | :--- |
| **Dữ liệu** | `{stt, ten_nganh, ten_truong, du_bao_2026, bien_b, diem_hs, delta, nhom_rui_ro, hoc_phi_nam, khu_vuc, chi_tieu, ly_do}` |
| **Rỗng** | Không có thẻ rỗng. `0` kết quả → chuyển sang [màn hình chặn §7 wireframe](UI_WIREFRAME.md), không phải một thẻ trống. |
| **Đang tải** | Khung xám nhấp nháy nhẹ **cùng chiều cao thẻ thật** (~168px) — tránh nhảy bố cục khi dữ liệu về |
| **Có dữ liệu** | Xem [§6 wireframe](UI_WIREFRAME.md). Khối *"Vì sao gợi ý ngành này"* mặc định **thu gọn**. |
| **Lỗi** | Thiếu một trường (vd. chưa có học phí) → dòng đó ghi *"chưa có dữ liệu"*, **không ẩn dòng, không điền 0** |
| **Không quyền** | HS **không** thấy `fit_score`, `interest_match`, `σ`, tên tool. Cán bộ thấy thêm bảng §2.6. |

**Ba ràng buộc hiển thị không được vi phạm:**

1. `du_bao_2026` **luôn** in kèm biên: `26.1 ± 0.5`. Không có đường nào in ra `26.1` trơ trọi. Nếu `bien_b` thiếu → in `chưa đủ dữ liệu để dự báo`, không in số.
2. `ten_truong` **xuống dòng, không cắt bằng `…`**. Thử với `"Trường Đại học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh"` (54 ký tự) trước khi coi là xong.
3. Huy hiệu rủi ro đủ **màu + icon + chữ**.

### 2.5. Banner nới ràng buộc (nhánh D)

| | |
| :--- | :--- |
| **Vai trò** | Nói rõ hệ thống đã tự đổi điều kiện của HS — bắt buộc, không phải nice-to-have |
| **Dữ liệu** | `{loai: "khu_vuc"\|"hoc_phi"\|"nganh"\|"bac_hoc", cu, moi, ly_do}` |
| **Rỗng** | `da_noi_rang_buoc == None` → không render |
| **Có dữ liệu** | Nền `#EFF4FE`, viền trái 3px `#2563EB`, icon `ⓘ`. Nêu **đã nới gì và vì sao**, không phải "đã điều chỉnh điều kiện" |
| **Lỗi** | Không áp dụng |

Câu mẫu đúng: *"Mình đã mở rộng sang TP.HCM và Đà Nẵng vì ở Hà Nội chưa đủ lựa chọn an toàn cho mức điểm này."*
Câu mẫu sai: *"Đã điều chỉnh bộ lọc."*

### 2.6. Bảng kết quả mô hình (cổng Tư vấn)

| | |
| :--- | :--- |
| **Rỗng** | Ca chưa chạy → *"Ca này chưa có kết quả. [Chạy chấm điểm]"* |
| **Đang tải** | Dòng trạng thái `⟳ đang chạy…` ngay trong bảng danh sách ca, không chặn cả trang |
| **Có dữ liệu** | Thử với **20 dòng** và tên trường 60 ký tự. Bảng **cuộn ngang trong hộp riêng** — trang không bao giờ cuộn ngang. |
| **Lỗi** | Độ phủ dữ liệu thiếu → nhãn `⚠ Thiếu học phí` **trên đúng dòng đó**, không gom về đầu trang |
| **Không quyền** | Cán bộ **không** thấy: system prompt, trọng số ở dạng sửa được, `MAX_ITERATIONS`, trace thô, log, chuyển provider/model |
| **Mobile** | < 640px: mỗi dòng thành **một thẻ** với nhãn trường bên trái, giá trị bên phải |

### 2.7. Khối trace (cổng Quản trị)

| | |
| :--- | :--- |
| **Rỗng** | *"Phiên này chưa có bước nào được ghi lại."* + gợi ý kiểm `st.session_state["trace"]` |
| **Đang tải** | Append **từng bước trong lúc chạy**, không gom cuối. Bước đang chạy có `⟳` quay. |
| **Có dữ liệu** | Mặc định **thu gọn một dòng/bước**. `monospace`. `Observation` dài > 400 ký tự → cắt kèm nút `▸ xem đầy đủ` |
| **Lỗi** | Bước lỗi nền vàng nhạt + icon `⚠` + ghi rõ guardrail nào bắt được |
| **Không quyền** | Chỉ vai `admin`. Vai khác vào URL này → *"Phần này dành cho quản trị."* + nút quay lại — không phải màn hình trắng |

> Gom trace ở cuối vòng lặp là lỗi hay gặp nhất: khi chạm `MAX_ITERATIONS` hoặc API rớt giữa chừng thì mất sạch trace, **đúng lúc cần nó nhất**.

---

## 3. Viết chữ trong giao diện

Chữ trong UI là một phần thiết kế, không phải phần điền sau. Người đọc là HS 17–18 tuổi đang căng thẳng.

### 3.1. Cấm — không phải khuyến nghị

| Loại | Ví dụ cấm | Thay bằng |
| :--- | :--- | :--- |
| Khẳng định chắc chắn (G-01) | "chắc chắn đỗ", "trượt là cái chắc" | "gần như chắc chắn đỗ **theo dữ liệu 3 năm**", "cần may mắn" |
| Phán xét khi điểm thấp (G-03) | "điểm em hơi thấp", "ngành này khó lắm" | "mức điểm này hợp với nhóm trường sau" |
| Nhãn tính cách cứng (G-11) | "Em là người hướng nội" | "em **có xu hướng** thiên về nhóm Nghiên cứu" |
| Ngôn ngữ log | "Error 502", "MAX_ITERATIONS reached", "null" | "Hệ thống đang bận, em thử lại sau 30 giây" |
| Nhãn nút mơ hồ | "OK", "Gửi", "Tiếp tục" ở chỗ có hậu quả | "Tải danh sách về (.txt)", "Chạy lại từ câu này" |

### 3.2. Bắt buộc

- Mọi phản hồi tiêu cực kèm **≥1 lối đi khả thi** (G-03).
- Không có dữ liệu → nói thẳng *"phần này mình chưa có dữ liệu"*, **không suy đoán** (G-02).
- Câu kết của mọi danh sách nhắc **quyết định cuối thuộc về em và gia đình** (G-04).
- Nhất quán từ vựng: gọi là **"nguyện vọng"** thì đừng chỗ khác gọi "lựa chọn xét tuyển"; **"khu vực"** chứ không lúc "địa điểm" lúc "thành phố".

---

## 4. Responsive

Thiết kế mobile trước rồi mở rộng — mobile ép chọn cái gì thật sự quan trọng.

| Khoảng | Nguyên tắc | Cụ thể cho sản phẩm này |
| :--- | :--- | :--- |
| **< 640px** | Một cột. Hành động chính trong tầm ngón cái. Bảng → danh sách thẻ. | 4 gợi ý xếp **dọc** · thẻ điểm 2 ô/hàng · thẻ NV xếp dọc `Dự báo` rồi `Em có` · sidebar hồ sơ → ngăn kéo sau ☰, mặc định đóng · ô nhập **dính đáy** |
| **640–1024px** | Hai cột được. | Gợi ý về lưới 2×2 · sidebar hồ sơ hiện · màn Đối chứng **vẫn xếp chồng dọc** (chatbot trên, agent dưới) |
| **> 1024px** | Giới hạn bề rộng vùng đọc 65–75 ký tự. | Cột chat `max-width: 760px` căn giữa · màn Đối chứng chia đôi thật · bảng mô hình hiện đủ cột |

Bảng, khối trace, bảng đối chứng — **cuộn ngang trong hộp riêng của nó**. Trang không bao giờ cuộn ngang. Kiểm ở 360px trước khi coi là xong.

---

## 5. Checklist tiếp cận

Ba mục đầu là bắt buộc — thiếu chúng thì một phần người dùng thật sự không dùng được sản phẩm.

- [x] **Tương phản ≥ 4.5:1** — đã tính cho toàn bộ token ở [§1.1](#11-màu-nền-tảng)/[§1.2](#12-màu-nghiệp-vụ--khoá-cứng), thấp nhất là `#64748B` ở **4.76:1**
- [x] **Vùng bấm ≥ 44×44px** — thẻ MBTI để ~120px cao; nút icon `[✎]`, `👍`, `👎` phải có padding đủ dù icon vẽ nhỏ hơn
- [x] **Không dùng riêng màu để truyền thông tin** — mọi nhãn rủi ro có màu + icon + chữ; ô đỏ/xanh màn Đối chứng kèm nhãn `← Bước 2` / `← không nguồn`
- [ ] Toàn bộ luồng chat đi được bằng `Tab` theo thứ tự đọc; `Enter` kích hoạt; `Esc` đóng lớp phủ và dừng stream
- [ ] Focus ring nhìn rõ: `outline: 2px solid #2563EB; outline-offset: 2px`. **Không** `outline: none` mà không thay bằng gì
- [ ] Nút chỉ có icon có `aria-label` — `[✎]` → `aria-label="Sửa câu hỏi này"`
- [ ] Mọi ô nhập có `<label>` gắn thật; placeholder **không** thay label (placeholder biến mất ngay khi gõ)
- [ ] Lỗi form gắn vào đúng trường qua `aria-describedby`, không gom một dòng đỏ đầu trang
- [ ] Vùng stream có `aria-live="polite"` để trình đọc màn hình đọc được chữ chạy dần
- [ ] Đọc được khi phóng to 200%
- [ ] Tôn trọng `prefers-reduced-motion` — tắt hiệu ứng con trỏ nhấp nháy và spinner quay

---

## 6. Kiểm với dữ liệu xấu nhất

Thiết kế cho dữ liệu đẹp là lỗi lặp lại nhiều nhất. Bảy ca phải thử trước khi coi là xong:

| # | Ca | Chỗ dễ vỡ |
| :---: | :--- | :--- |
| 1 | `"Trường Đại học Sư phạm Kỹ thuật Thành phố Hồ Chí Minh"` (54 ký tự) | Tiêu đề thẻ NV, cột `Ngành` bảng mô hình, dropdown chấm nhanh |
| 2 | Danh sách nguyện vọng **rỗng** sau khi lọc | Phải rơi vào màn hình chặn §7, không phải thẻ trống |
| 3 | Đúng **2** lựa chọn An toàn (sát ngưỡng G-10) | Danh sách vẫn render, nhưng phải hiện được là mỏng |
| 4 | Bảng ca **50 dòng**, bảng test **19 case** | Cuộn dọc trong hộp; đầu bảng dính (`sticky`) |
| 5 | Câu hỏi HS **dài 800 ký tự** | Bong bóng chat, ô nhập trần 6 dòng, nút `[✎]` không bị đẩy ra ngoài |
| 6 | Câu hỏi **một chữ** — `"hi"` | Agent phải hỏi lại tử tế, không chạy vòng ReAct rỗng |
| 7 | `Observation` JSON **dài 3.000 ký tự** | Khối trace cắt kèm `▸ xem đầy đủ`, không phá bố cục |

Thêm hai ca vận hành: **ngắt mạng giữa lúc stream** và **API hết quota ngay lúc trình bày** — có phương án dự phòng chưa?

---

## 7. Ánh xạ sang Streamlit — bàn giao Role 4

Streamlit dựng demo rất nhanh, đổi lại vài giới hạn phải biết trước khi hứa với người xem.

| Thành phần trong spec | Streamlit | Ghi chú |
| :--- | :--- | :--- |
| Cổng chọn vai | `st.sidebar.radio` | Không làm form đăng nhập thật; xem [UI_FLOW §0b-2](UI_FLOW.md) |
| Khung chat | `st.chat_message` + `st.chat_input` | Đúng quy ước, đỡ tự dựng. `st.chat_input` **đã có** Enter gửi sẵn |
| Stream chữ | `st.write_stream(generator)` | Cho hiệu ứng chữ chạy mà không tự xử lý |
| Danh sách bước ReAct | `st.status("Đang tìm cho em…", expanded=True)` → `.update(state="complete")` | Tự thu gọn khi xong — đúng thứ §2.2 cần |
| Thẻ nhập điểm / MBTI | `st.form` trong `st.chat_message("assistant")` | `st.form` gom nhiều ô vào **một lần rerun**, tránh chạy lại script sau mỗi ký tự |
| Sidebar hồ sơ | `st.sidebar` đọc `st.session_state["ho_so"]` | **Chỉ đọc** — không đặt widget có state riêng ở đây |
| Thẻ nguyện vọng | `st.container(border=True)` + `st.expander("Vì sao gợi ý ngành này")` | |
| Bảng mô hình / test case | `st.dataframe` | `column_config` để cố định độ rộng; **không** `st.table` (không cuộn được) |
| Khối trace | `st.code(..., language=None)` trong `st.expander` | |
| Màn Đối chứng | `st.columns(2)` | Cỡ chữ 20px qua `st.markdown` + CSS nội tuyến |
| Nút Dừng | `st.button` + cờ `st.session_state["yeu_cau_dung"]`, generator kiểm mỗi vòng | Streamlit không có huỷ thật — generator phải tự thoát |

### Bốn cái bẫy đã biết

1. **Mỗi tương tác chạy lại toàn bộ script.** Mọi state phải nằm trong `st.session_state`, nếu không nó biến mất sau mỗi lần bấm.
2. **`@st.cache_data` cho việc nặng** (nạp `test_cases.json`, dựng bảng dữ liệu mock). Thiếu cache là lý do phổ biến nhất khiến demo Streamlit chậm bất thường.
3. **`dang_chay` phải reset trong `finally`** — một lần lỗi API mà quên reset là khoá nút Gửi vĩnh viễn tới lúc restart, ngay giữa buổi trình bày.
4. **Nút gợi ý ở màn hình rỗng**: ghi câu vào `session_state` rồi `st.rerun()`, **không** gọi agent trong callback.

> **Giới hạn cần nói trước, không để lộ ra lúc gần nộp**: Streamlit khó tuỳ biến sâu, khó làm layout phức tạp, kém trên mobile. Bố cục 2 cột của màn Đối chứng và sidebar hồ sơ sẽ **không** đẹp bằng prototype HTML. Prototype là **bản trình bày ý đồ**, Streamlit là **bản chạy thật** — nói rõ điều này ngay từ đầu buổi demo.

---

## 8. Checklist trước khi demo

Demo hỏng thường không hỏng ở phần AI mà ở mấy chỗ này:

- [ ] 4 nút gợi ý màn hình rỗng **thật sự cho kết quả tốt** — bấm thử cả 4, không chỉ cái đầu
- [ ] Có câu trả lời cho câu ngoài phạm vi (*"em muốn học ở Cần Thơ"*) thay vì bịa
- [ ] Stream chạy được, nút Dừng dừng thật
- [ ] Chạy TC05a (điểm 45/30) — xem agent hỏi lại **một lần** rồi dừng, không lặp
- [ ] Chạy TC06 (16.5 điểm) — xem nhánh D **tự** kích hoạt và banner nói rõ đã nới gì
- [ ] Thử ngắt mạng giữa lúc đang trả lời
- [ ] Thử câu hỏi rất dài và câu hỏi một chữ
- [ ] Kiểm trên máy chiếu: màn Đối chứng đọc được từ hàng ghế cuối
- [ ] Có phương án dự phòng khi OpenRouter hết quota — **trace đã lưu sẵn của một phiên chạy đúng** để chiếu thay

---

## 9. Ngoài phạm vi

Cố ý không làm ở bản này, để Role 4 không tự suy diễn thêm:

| Không làm | Vì sao |
| :--- | :--- |
| Hệ thống tài khoản thật, quên mật khẩu, lưu lịch sử giữa các phiên | `REQUIREMENTS.md` §2.2 đã loại. Cổng vào là **màn hình chọn vai**, không phải auth |
| Biểu đồ, chart, infographic lấy dữ liệu từ output của model | FR-13. Frontend được vẽ **huy hiệu/thẻ/thanh tĩnh**, không vẽ chart |
| Đăng ký nguyện vọng thật lên hệ thống của Bộ | Agent chỉ tư vấn, không hành động thay người dùng |
| Trắc nghiệm MBTI đầy đủ 93 câu / Holland bản dài | Chỉ bộ rút gọn 4 câu |
| Khu vực ngoài Hà Nội · TP.HCM · Đà Nẵng | `REQUIREMENTS.md` §2.3, enum đóng |
| Sửa cấu hình trọng số trong bản demo | Màn hình Cấu hình **chỉ đọc**. Nếu làm được thì phải kèm xác nhận 2 bước + nhật ký cũ→mới |
| Đa ngôn ngữ | Chỉ tiếng Việt có dấu |
| Chế độ tối cho **cổng Tư vấn và Quản trị** | Chỉ cổng HS có light + dark. Hai cổng nội bộ dùng sáng, ưu tiên thời gian cho phần đi thi |
