# 🎨 PROMPT THIẾT KẾ UI/UX — LA BÀN NGUYỆN VỌNG

> **Cách dùng**: copy toàn bộ phần trong khung `PROMPT` bên dưới, dán vào công cụ sinh UI (v0, Lovable, Claude, Figma Make…). Muốn ra bản HTML tự chạy để demo Mốc 4 thì thêm dòng cuối: *"Xuất ra một file HTML duy nhất, CSS/JS nội tuyến, không tải font/script từ ngoài."*
>
> Nguồn: `docs/REQUIREMENTS.md` v1.1 · Văn phong theo mẫu *UI Description for Alternative Credit Scoring Platform*.

---

# ===== BẮT ĐẦU PROMPT =====

# UI Description — LA BÀN NGUYỆN VỌNG (AI Tư vấn Chọn Ngành & Xếp Nguyện Vọng)

#### STRICTLY OBEY

**BẢNG MÀU** — chỉ dùng đúng các giá trị sau, không tự thêm màu:

| Vai trò | Tên | HEX | Dùng ở đâu |
| :--- | :--- | :--- | :--- |
| Nền tối / chữ chính | Navy Tri Thức | `#0F1E3D` | Header, sidebar, chữ tiêu đề |
| Màu nhấn | Xanh La Bàn | `#2563EB` | Nút hành động chính, link, focus ring |
| Nền trang | Trắng Giấy | `#FFFFFF` / `#F7F9FC` | Nền chính / nền khối phụ |
| Chữ phụ | Xám Ghi Chú | `#5B6472` | Mô tả, timestamp, đơn vị |
| Viền | Xám Viền | `#E3E6EB` | Đường kẻ, viền thẻ |

**MÀU NGHIỆP VỤ — KHOÁ CỨNG, TUYỆT ĐỐI KHÔNG DÙNG CHO MỤC ĐÍCH KHÁC:**

| Nhóm rủi ro | HEX | Icon bắt buộc đi kèm |
| :--- | :--- | :--- |
| 🟢 An toàn | `#157F3D` | ● + chữ "An toàn" |
| 🟡 Vừa tầm | `#B45309` | ◐ + chữ "Vừa tầm" |
| 🔴 Liều | `#B42318` | ▲ + chữ "Liều" |
| ⚫ Ngoài tầm | `#64748B` | ○ + chữ "Ngoài tầm" |

**KHÔNG BAO GIỜ dùng riêng màu để truyền thông tin.** Mọi nhãn rủi ro phải có đủ **màu + icon + chữ tiếng Việt** — người mù màu và bản in đen trắng đều phải đọc được.

**NGÔN NGỮ & CHỮ**: Toàn bộ giao diện bằng **tiếng Việt có dấu**. Font bắt buộc hỗ trợ đầy đủ dấu tiếng Việt: **Be Vietnam Pro** (chính), fallback `Inter, "Segoe UI", system-ui`. Phần log/trace kỹ thuật dùng `JetBrains Mono, Consolas, monospace`. Chữ nội dung ≥ 16px. Người dùng chính là **học sinh 17–18 tuổi đang căng thẳng vì deadline** — chữ to, câu ngắn, không thuật ngữ.

**RÀNG BUỘC SẢN PHẨM (từ FR-13)**: Câu trả lời của agent là **văn bản + bảng markdown thuần, không sinh ảnh, không sinh biểu đồ**. Giao diện được phép có badge/thẻ/thanh trạng thái tĩnh do frontend vẽ, nhưng **không** được thiết kế bất kỳ chart nào lấy dữ liệu từ output của model.

**RÀNG BUỘC KỸ THUẬT**: Bản demo chạy trên **Streamlit**, gọi LLM qua `LLM_PROVIDER=openrouter`, `LLM_MODEL=google/gemini-2.5-flash-lite`. Độ trễ thực tế 2–8 giây/lượt, một phiên đầy đủ 5–7 lần gọi tool. Vì vậy **bắt buộc phải thiết kế cho trạng thái chờ**: streaming chữ, danh sách bước ReAct thu gọn được, nút Dừng. Mọi state nằm trong `st.session_state`.
#####

---

## 0. Sản phẩm này là gì

Một AI Agent (kiến trúc ReAct: `Thought → Action → Observation`) nhận đầu vào là **điểm thi + sở thích/tính cách + ràng buộc cá nhân**, trả về **danh sách ~10 nguyện vọng đã xếp thứ tự, chia 3 nhóm 🔴 Liều / 🟡 Vừa tầm / 🟢 An toàn**, mỗi lựa chọn kèm số liệu và lý do.

**Nguyên tắc thiết kế cốt lõi — mọi màn hình phải phản ánh nguyên tắc này:**

> 🎯 **ƯU TIÊN SỞ THÍCH TRƯỚC — ĐIỂM SỐ CHỈ LÀ BỘ LỌC KHẢ THI.**
> Giao diện **không** được mở đầu bằng ô "Nhập điểm của bạn". Câu hỏi đầu tiên trên màn hình phải là *"Em thích làm gì?"*, ô điểm đứng sau. Nếu bố cục làm ngược lại, học sinh sẽ chọn ngành chỉ vì "vừa đủ đỗ" — đây là nguyên nhân hàng đầu của bỏ học năm nhất.

Hệ thống có **một điểm đăng nhập chung**, nhưng trải nghiệm sau đăng nhập khác hẳn nhau theo vai. Lý do: cùng một ca tư vấn cần ba mức thông tin khác nhau — học sinh cần lời khuyên rõ ràng, cán bộ tư vấn cần lý do để bảo vệ lời khuyên đó, đội kỹ thuật cần trace để chứng minh agent không bịa.

---

## 1. Trang đăng nhập chung

Tất cả người dùng vào qua một trang duy nhất. Thiết kế đơn giản, đáng tin, không hoa mỹ:

- Ô Email / Tên đăng nhập
- Ô Mật khẩu
- Nút **Đăng nhập**
- Link *Quên mật khẩu*
- Link *Điều khoản sử dụng & Chính sách dữ liệu*
- Nút phụ: **Dùng thử không cần tài khoản (chế độ Học sinh)** — học sinh đang vội, bắt tạo tài khoản trước khi cho thử là bước không kiếm nổi chỗ đứng.

**Tài khoản demo (hiển thị sẵn trên trang đăng nhập ở bản demo):**

```
Cán bộ tư vấn:   Username: Tuvan_123    Pass: Tuvan_123
Quản trị/Kiểm định: Username: Admin_T029  Pass: Admin_T029
Học sinh:        vào thẳng bằng nút "Dùng thử"
```

Logic điều hướng sau đăng nhập:

```
Đăng nhập thành công
        ↓
Kiểm tra vai trò
        ↓
role = hoc_sinh / phu_huynh   → Cổng Học sinh      → /hs/tro-chuyen
role = tu_van / giao_vien     → Cổng Tư vấn        → /tuvan/ca-tu-van
role = admin / kiem_dinh      → Cổng Quản trị      → /admin/tong-quan
```

Nguyên tắc: **mọi người đăng nhập cùng một chỗ, nhưng mỗi vai chỉ thấy đúng phần mình được phép thấy.**

---

## 2. Cổng Học sinh / Phụ huynh

### Mục đích

Học sinh dùng giao diện này để trò chuyện, khai thông tin, và nhận **một danh sách nguyện vọng đã xếp thứ tự kèm lý do**. Người dùng này **không** được thấy công thức `fit_score`, trọng số, vòng lặp ReAct, tên tool, hay nội dung system prompt.

### A. Màn hình đầu (trạng thái rỗng — màn hình khó nhất của sản phẩm)

Ô chat trống không gợi ý gì là lỗi UX nặng nhất của loại app này. Màn hình đầu phải có:

- Một câu mở đầu ngắn: *"Chào em. Kể cho anh/chị nghe em thích làm gì — rồi mình mới bàn tới điểm số."*
- **4 nút gợi ý bấm được** (đây là câu thật, hệ thống trả lời tốt):
  - *"Em không biết mình thích gì cả"*
  - *"Em được 24.5 khối A00, ngành CNTT Bách Khoa HN lấy bao nhiêu?"*
  - *"Em muốn học ở Đà Nẵng, học phí dưới 20 triệu"*
  - *"Em muốn làm Data Analyst thì học ngành gì?"*
- Một dòng nói rõ **giới hạn**, chữ nhỏ, không giấu: *"Dữ liệu điểm chuẩn 2023–2025, hiện hỗ trợ tổ hợp A00/A01/D01 và khu vực Hà Nội · TP.HCM · Đà Nẵng. Đây là gợi ý tham khảo, quyết định cuối cùng là của em và gia đình."*

### B. Khung trò chuyện

- Enter gửi, Shift+Enter xuống dòng. Ô nhập tự cao theo nội dung, có trần rồi cuộn.
- Nút gửi luôn hiện, mờ đi khi ô rỗng — **không ẩn hẳn**.
- **Stream chữ ra ngay khi có.** Trong lúc stream, nút gửi đổi thành **Dừng**.
- Trong lúc agent chạy tool, hiện **một dòng trạng thái thân thiện, không lộ tên tool**:
  `⟳ Đang tra điểm chuẩn 3 năm gần nhất…` (KHÔNG hiện `Action: lookup_admission_scores`).
- Học sinh phải **sửa lại được câu hỏi trước và chạy lại từ đó**, không bắt gõ lại từ đầu.

### C. Thẻ thu thập thông tin (Progressive form trong luồng chat)

Thay vì một form dài, hiện **thẻ nhỏ chèn giữa hội thoại** khi agent cần dữ liệu. Mỗi thẻ hỏi đúng một nhóm:

| Trường | Bắt buộc | Kiểu nhập |
| :--- | :---: | :--- |
| Điểm thi (0–30) | ✅ | Ô số + validate ngay tại chỗ |
| Tổ hợp | ✅ | 3 chip chọn: A00 · A01 · D01 |
| Sở thích | ✅ | Ô text tự do |
| Khu vực học | ⬜ | 4 chip: Hà Nội · TP.HCM · Đà Nẵng · Không giới hạn |
| Ngân sách học phí/năm | ⬜ | Ô số, đơn vị "triệu đồng" |
| Môn mạnh nhất | ⬜ | Chip chọn |

Trường bắt buộc thiếu → agent **hỏi lại, không đoán**. Nhập điểm ngoài 0–30 → báo lỗi ngay dưới ô bằng tiếng Việt đời thường (*"Điểm thi phải trong khoảng 0–30. Em kiểm tra lại giúp nhé"*), **không** để agent tự lặp lại tool.

### D. Thẻ trắc nghiệm MBTI rút gọn

Kích hoạt khi học sinh nói *"em không biết mình thích gì"*. Thiết kế thành **4 câu A/B, mỗi câu 2 thẻ lớn bấm được** (không dùng radio button nhỏ), có thanh tiến trình `Câu 2/4`, có nút *Bỏ qua, em tự mô tả*.

Kết quả trả về phải hiển thị kèm câu xác nhận, **không dán nhãn tính cách cứng**:
> *"Theo 4 câu vừa rồi, em có xu hướng thiên về nhóm Nghiên cứu (I) và Nguyên tắc (C). Đây mới là gợi ý ban đầu — em thấy có đúng không?"*

### E. Màn hình kết quả — Danh sách nguyện vọng

Đây là màn hình quan trọng nhất của sản phẩm. Bố cục:

```text
┌──────────────────────────────────────────────────────────┐
│  Danh sách nguyện vọng gợi ý cho em                      │
│  24.5 điểm · A00 · Hà Nội · học phí ≤ 40 triệu    [Sửa]  │
├──────────────────────────────────────────────────────────┤
│  ▲ LIỀU — cần may mắn, chỉ nên đặt ở nguyện vọng đầu     │
│  ┌────────────────────────────────────────────────────┐  │
│  │ NV1  Khoa học Máy tính · ĐH Bách Khoa HN           │  │
│  │      Dự báo 2026: 26.1 ± 0.5   Em: 24.5  (−1.6)    │  │
│  │      Học phí 35 tr/năm · Hà Nội                    │  │
│  │      ▾ Vì sao gợi ý ngành này                      │  │
│  └────────────────────────────────────────────────────┘  │
│  ...                                                      │
│  ◐ VỪA TẦM (4 lựa chọn)                                  │
│  ● AN TOÀN (3 lựa chọn) — đây là lưới an toàn của em     │
├──────────────────────────────────────────────────────────┤
│  [ Tải danh sách về (.txt) ]   [ Hỏi thêm ]  👍 👎       │
└──────────────────────────────────────────────────────────┘
```

Quy tắc bắt buộc trên màn hình này:

1. **Không bao giờ hiển thị một con số giả vờ chính xác.** Luôn là `26.1 ± 0.5`, không phải `26.1`.
2. **Chặn ở tầng sản phẩm**: nếu có `< 2` lựa chọn 🟢 An toàn thì **không được render danh sách** — thay bằng thẻ *"Mình chưa tìm đủ phương án an toàn cho em, để anh/chị tìm thêm hướng khác"* rồi chạy nhánh mở rộng (Cao đẳng / trường nghề / xét học bạ / nới khu vực).
3. Khi hệ thống đã tự nới ràng buộc, phải có **banner nói rõ đã nới gì và vì sao**: *"Mình đã mở rộng sang TP.HCM và Đà Nẵng vì ở Hà Nội chưa đủ lựa chọn an toàn cho mức điểm này."*
4. Mỗi thẻ có mục **"Vì sao gợi ý ngành này"** thu gọn được, viết bằng ngôn ngữ thường: *"Ngành này hợp với xu hướng thích phân tích của em, nhu cầu tuyển dụng 3 năm qua tăng, và mức điểm nằm trong tầm với."*
5. Câu kết luôn nhắc: **quyết định cuối thuộc về học sinh và gia đình.**

### F. Quy tắc giọng điệu (bắt buộc, không phải khuyến nghị)

- ❌ Cấm mọi từ khẳng định chắc chắn: "chắc chắn đỗ", "trượt là cái chắc".
- ❌ Cấm từ phán xét khi điểm thấp: "kém", "thấp quá", "khó lắm".
- ✅ Mọi phản hồi tiêu cực phải kèm **ít nhất 1 lối đi khả thi**.
- ✅ Khi không có dữ liệu, nói thẳng *"phần này mình chưa có dữ liệu"* — **không suy đoán**.

### Học sinh KHÔNG được thấy

Công thức `fit_score` và trọng số · công thức dự báo `P̂₂₀₂₆` · biên `b` dưới dạng công thức · tên tool · chuỗi `Thought / Action / Observation` · system prompt · số vòng lặp · tên model, token, chi phí · log hệ thống · cấu hình quản trị.

---

## 3. Cổng Cán bộ Tư vấn / Giáo viên Hướng nghiệp

### Mục đích

Người dùng nội bộ tư vấn cho nhiều học sinh trong ngày mùa cao điểm (một buổi có thể 30–50 ca). Mục tiêu của giao diện: **rút ngắn thời gian mỗi ca và đưa ra lý do đủ vững để bảo vệ lời khuyên trước phụ huynh.** Nhóm này thấy được điểm số và chỉ báo của mô hình, nhưng **không** sửa được cấu hình mô hình.

### A. Màn hình tra cứu / tạo ca tư vấn

Tìm theo: Mã ca · Tên học sinh (viết tắt) · Trường THPT · Ngày tư vấn.
Có **ô nhập nhanh** cho tình huống thực tế nhất — cán bộ nhập 4 trường rồi nhận gợi ý ngay:

```
Điểm: 22.0    Tổ hợp: A01    Khu vực: Đà Nẵng    Sở thích: "thích máy móc"
                          → [ Chấm nhanh ]
```

### B. Thẻ tóm tắt ca

Sau khi mở một ca, hiện thẻ tổng quan: mã ca · điểm · tổ hợp · mã RIASEC · khu vực · ngân sách · số lựa chọn theo từng nhóm rủi ro · trạng thái ca · thời điểm cập nhật cuối.

```
Ca #T029-0142 · 22.0 điểm · A01 · Đà Nẵng · RIASEC: R,I
Kết quả: ● 3 An toàn  ◐ 4 Vừa tầm  ▲ 3 Liều     Trạng thái: Đã có danh sách
Cảnh báo: đã tự nới khu vực (không đủ lựa chọn An toàn tại Đà Nẵng)
```

### C. Bảng kết quả mô hình

Nhóm này thấy thêm so với học sinh:

| Chỉ số hiển thị | Ví dụ |
| :--- | :--- |
| `fit_score` từng ngành (0–100) | Cơ khí: 78 · CNTT: 71 |
| `interest_match` | 82/100 |
| `job_outlook_score` + nhãn bền vững | 4.6 — Bền vững cao |
| Dự báo `P̂₂₀₂₆` và biên `b` | 23.25 ± 1.03 |
| `Δ = điểm HS − P̂` | +1.25 |
| Nhóm rủi ro | ● An toàn |
| Độ phủ dữ liệu | Đủ / Thiếu học phí / Thiếu chỉ tiêu |

### D. Giải thích theo tiêu chí (không phải theo model)

Hiện hai cột **Yếu tố thuận lợi** / **Yếu tố rủi ro**, viết ở mức nghiệp vụ:

```
Yếu tố thuận lợi:
 - Sở thích khớp 2/2 mã Holland của ngành
 - Ngành có nhu cầu tuyển dụng tăng 3 năm liên tiếp
 - Điểm vượt ngưỡng dự báo 1.25 điểm

Yếu tố rủi ro:
 - Điểm chuẩn ngành này dao động mạnh giữa các năm (σ = 1.03)
 - Học sinh chưa khai ngân sách học phí
 - Chỉ còn đúng 2 lựa chọn nhóm An toàn
```

### E. Luồng vận hành Xanh / Vàng / Đỏ

| Luồng | Khi nào | Khuyến nghị hiển thị |
| :--- | :--- | :--- |
| 🟢 Xanh | ≥3 lựa chọn An toàn, dữ liệu đủ | *Có thể chốt danh sách, chỉ cần rà lại với phụ huynh* |
| 🟡 Vàng | Đủ 2 An toàn nhưng thiếu dữ liệu hoặc biên `b` rộng | *Cần hỏi thêm: ngân sách / môn mạnh — trước khi chốt* |
| 🔴 Đỏ | Hệ thống đã nới ràng buộc mà vẫn < 2 An toàn | *Chuyển hướng tư vấn Cao đẳng / trường nghề / xét học bạ. Cần cán bộ ngồi trực tiếp với học sinh.* |

### F. Bảng việc cần làm

- Số trường thông tin còn thiếu và là trường nào
- Hành động kế tiếp được gợi ý
- Ca này có cần chuyển lên chuyên viên cao hơn không
- Thời gian xử lý ca (để đo hiệu quả so với tư vấn thủ công)

### Cán bộ tư vấn KHÔNG được thấy

Toàn văn system prompt · trọng số `fit_score` ở dạng **sửa được** · cấu hình `MAX_ITERATIONS` · trace `Thought/Action/Observation` thô · log hệ thống · chuyển đổi provider/model · quyền sửa dữ liệu điểm chuẩn.
→ Họ **xem được kết quả và lý do, nhưng không đổi được cách mô hình chấm.**

---

## 4. Cổng Quản trị & Kiểm định mô hình

### Mục đích

Dành cho đội phát triển và người chấm bài (cross-audit). Đây là nơi **chứng minh agent không bịa** — mỗi con số trong câu trả lời phải truy ngược được về một Observation cụ thể. Nhóm này thấy toàn bộ.

### A. Bảng theo dõi tổng quan

Số phiên đã chạy · tỷ lệ phiên hoàn thành · phân bố Xanh/Vàng/Đỏ · số lần chạm `MAX_ITERATIONS` · số lần lặp trùng action · số lần gọi tool không tồn tại · số lần tool trả lỗi · số vòng lặp trung bình mỗi phiên · độ trễ trung bình mỗi lượt · tỷ lệ kích hoạt nhánh mở rộng.

```
Phiên đã chạy: 48        Trung bình 4.2 vòng/phiên
Chạm trần lặp: 3 (6.3%)  Lặp trùng action: 2
Tool lỗi: 7 (chủ yếu: điểm ngoài 0–30)
Độ trễ TB: 3.4s/lượt · Model: google/gemini-2.5-flash-lite qua OpenRouter
```

### B. Xem trace đầy đủ một phiên

Với mỗi phiên: câu hỏi gốc · **toàn bộ chuỗi `Thought → Action → Action Input → Observation`** · câu trả lời cuối · guardrail nào đã kích hoạt · thời gian từng bước · tên model + provider + số token.

Trace hiển thị dạng **danh sách bước, mặc định thu gọn một dòng, bấm mới mở chi tiết** — người xem tổng quan chỉ cần biết chạy tới đâu, người debug mới cần input/output đầy đủ:

```text
✓ Bước 1 · mbti_quick_assess("BABA")            (0.9s)
✓ Bước 2 · find_majors_by_interest("I,C")       (1,4s · 5 ngành)
⚠ Bước 3 · filter_universities(khu_vuc="Đà Nẵng") (1,1s · chỉ 1 lựa chọn An toàn)
✓ Bước 4 · filter_universities(khu_vuc="")      (1,2s · nhánh D kích hoạt)
  → Trả lời cuối
```

Dùng `monospace` cho khối trace. Có nút **Sao chép trace** và **Xuất ra `docs/trace_eval.md`**.

### C. Đối chứng Chatbot vs ReAct Agent

Màn hình chia đôi, cùng một câu hỏi chạy hai đường:

| Cột trái — Chatbot thuần | Cột phải — ReAct Agent |
| :--- | :--- |
| Câu trả lời | Câu trả lời |
| **Không có Observation** | Trace tool đầy đủ |
| Highlight ĐỎ mọi con số không truy được về nguồn | Highlight XANH mọi con số có Observation |

Đây là màn hình dùng để trình bày lúc bảo vệ bài — thiết kế nó đủ to để chiếu lên máy chiếu đọc được từ hàng cuối.

### D. Bảng chạy bộ test case

Đọc từ `config/test_cases.json`, hiện bảng: mã case · loại (Đơn giản / 1 tool / Multi-tool / Edge case) · kỳ vọng · kết quả thực tế · số tool đã gọi · Đạt/Không đạt · nút *Chạy lại case này*. Có nút **Chạy tất cả**.

### E. Bảng guardrail

Liệt kê G-01…G-13, mỗi dòng: mã · rủi ro · số lần kích hoạt · phiên gần nhất · nút xem trace. Guardrail chưa từng kích hoạt lần nào thì đánh dấu **"chưa được kiểm chứng"** — chưa chạy không đồng nghĩa với an toàn.

### F. Cấu hình (chỉ đọc trong bản demo)

Trọng số `fit_score` (0.45 / 0.30 / 0.25) · trọng số dự báo (0.5 / 0.3 / 0.2) · `MAX_ITERATIONS = 8` · biên `b` tối thiểu 0.5 · ngưỡng chặn "≥ 2 lựa chọn An toàn" · `LLM_PROVIDER` · `LLM_MODEL`.

Mọi thay đổi cấu hình phải đi qua **xác nhận hai bước** và ghi vào nhật ký kèm người thực hiện, thời điểm, giá trị cũ → giá trị mới.

### G. Ma trận phân quyền

| Chức năng | Học sinh | Cán bộ tư vấn | Quản trị |
| :--- | :---: | :---: | :---: |
| Trò chuyện với agent | Có | Có | Có |
| Xem danh sách nguyện vọng | Có | Có | Có |
| Xem lý do bằng ngôn ngữ thường | Có | Có | Có |
| Xem `fit_score`, `Δ`, biên `b` | Không | Có | Có |
| Xem trace Thought/Action/Observation | Không | Không | Có |
| Xem system prompt | Không | Không | Có |
| Xem log & guardrail | Không | Không | Có |
| Sửa cấu hình trọng số | Không | Không | Có (2 bước) |
| Chạy bộ test case | Không | Không | Có |

---

## 5. Trạng thái bắt buộc thiết kế cho mọi thành phần

Một thành phần chưa xong cho tới khi cả 5 trạng thái đều có câu trả lời:

| Trạng thái | Yêu cầu cụ thể cho sản phẩm này |
| :--- | :--- |
| **Rỗng** | Chat trống → 4 câu gợi ý bấm được + dòng nói rõ giới hạn dữ liệu |
| **Đang tải** | < 1s: không hiện gì · 1–3s: chỉ báo đơn giản · 3–10s: nói đang làm gì (*"Đang tra điểm chuẩn 3 năm…"*) · > 10s: danh sách bước + nút **Huỷ** |
| **Có dữ liệu** | Thử với danh sách 10 nguyện vọng, và với tên trường dài 60 ký tự |
| **Lỗi** | 3 loại: (1) nhập sai → chỉ rõ ô nào, sửa thế nào · (2) không có kết quả sau lọc → gợi ý nới điều kiện · (3) lỗi API/hết quota → *"Hệ thống đang bận, em thử lại sau 30 giây"*, **không đổ stack trace** |
| **Chạm trần lặp** | Agent chạy hết 8 vòng → hiện phần kết quả đã thu được + câu xin lỗi lịch sự + nút *Hỏi lại theo cách khác*. **Không** hiện màn hình trắng. |

---

## 6. Design token

- **Khoảng cách**: đúng một thang `4 / 8 / 12 / 16 / 24 / 32 / 48`, không có số lẻ ngẫu hứng.
- **Cỡ chữ**: `13 / 16 / 20 / 26 / 34`. Chữ nội dung 16px, chữ trên màn chiếu ≥ 20px.
- **Bo góc**: 8px (thẻ nhỏ) và 16px (thẻ lớn). **Đổ bóng**: 2 mức, không hơn.
- **Kiểm tra bắt buộc**: tương phản chữ/nền ≥ 4.5:1 · vùng bấm ≥ 44×44px · focus ring nhìn thấy rõ khi đi bằng bàn phím · toàn bộ luồng chat đi được bằng Tab.

---

## 7. Sơ đồ điều hướng

```
/dang-nhap
  ├── role = hoc_sinh   → /hs/tro-chuyen
  │                       /hs/thong-tin
  │                       /hs/trac-nghiem
  │                       /hs/ket-qua
  │
  ├── role = tu_van     → /tuvan/ca-tu-van
  │                       /tuvan/ca/:ma_ca
  │                       /tuvan/cham-nhanh
  │                       /tuvan/viec-can-lam
  │
  └── role = admin      → /admin/tong-quan
                          /admin/trace/:ma_phien
                          /admin/doi-chung
                          /admin/test-cases
                          /admin/guardrail
                          /admin/cau-hinh
                          /admin/phan-quyen
```

---

## 8. Cấu trúc UI khuyến nghị

```
Chung
├── Đăng nhập
├── Quên mật khẩu
├── Hồ sơ người dùng
└── Thông báo

Cổng Học sinh
├── Trò chuyện (màn hình chính)
├── Thẻ thu thập thông tin
├── Trắc nghiệm MBTI rút gọn
├── Danh sách nguyện vọng
└── Tải kết quả

Cổng Tư vấn
├── Danh sách ca
├── Chấm nhanh
├── Chi tiết ca
├── Bảng kết quả mô hình
├── Giải thích theo tiêu chí
├── Luồng Xanh/Vàng/Đỏ
└── Việc cần làm

Cổng Quản trị & Kiểm định
├── Tổng quan
├── Trace phiên đầy đủ
├── Đối chứng Chatbot vs Agent
├── Bộ test case
├── Bảng guardrail
├── Cấu hình
└── Phân quyền
```

---

## 9. Cần giao lại những gì

1. **User flow** của cả 3 vai, gồm cả đường lỗi (nhập sai, không đủ lựa chọn An toàn, API rớt, chạm trần lặp) — không chỉ đường hạnh phúc.
2. **Wireframe dạng ASCII/markdown** cho từng màn hình chính trước khi dựng pixel.
3. **Spec bàn giao**: từng thành phần kèm đủ 5 trạng thái, bảng token, quy tắc responsive, checklist tiếp cận.
4. **Bản prototype HTML một file**, CSS/JS nội tuyến, không tải font/script từ ngoài, chạy được cả light và dark, không tràn ngang trên màn hình 360px.

Với mỗi màn hình còn nhiều phương án, đưa **2 phương án bố cục kèm một câu đánh đổi**, rồi **nói rõ chọn phương án nào và vì sao** — không đưa lựa chọn rồi để người đọc tự quyết.

# ===== KẾT THÚC PROMPT =====

---

## Ghi chú cho nhóm T029

| Vai trong tài liệu mẫu (ngân hàng) | Ánh xạ sang sản phẩm này |
| :--- | :--- |
| Company / Customer | Học sinh / Phụ huynh |
| RM / Credit Officer / Approver | Cán bộ tư vấn / Giáo viên hướng nghiệp |
| Bank Admin / Audit | Quản trị & Kiểm định mô hình (đội dev + người chấm chéo) |
| Credit score 0–1000 | `fit_score` 0–100 |
| Risk tier A/B/C/D | Nhóm 🟢 An toàn / 🟡 Vừa tầm / 🔴 Liều / ⚫ Ngoài tầm |
| SHAP explanation | Trace `Thought → Action → Observation` |
| Rule engine config | Trọng số `fit_score`, `MAX_ITERATIONS`, ngưỡng chặn ≥2 An toàn |
| Green/Yellow/Red flow | Giữ nguyên, đổi tiêu chí phân loại |

**Ba chỗ cần chốt trước khi chạy prompt:**

1. **Bảng màu** ở khối STRICTLY OBEY là do tôi đề xuất (sản phẩm chưa có brand). Đổi được — nhưng 4 màu nghiệp vụ 🟢🟡🔴⚫ nên giữ nguyên vì đã gắn với ngữ nghĩa trong `REQUIREMENTS.md`.
2. **Cổng Tư vấn là phần mở rộng ngoài MVP.** `REQUIREMENTS.md` §2.2 chỉ định phạm vi là chatbot text thuần một vai. Nếu chỉ cần demo đúng phạm vi Mốc 3, cắt mục 3 và giữ mục 2 + 4.
3. **FR-13 (không sinh ảnh/biểu đồ)** trong prompt được diễn giải là: agent không sinh chart, nhưng frontend được vẽ badge/thẻ tĩnh. Nếu nhóm muốn siết chặt hơn nữa thì bỏ luôn phần badge màu ở mục 2.E — tuy vậy sẽ mất khả năng đọc lướt của học sinh.
