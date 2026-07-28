# 📐 WIREFRAME — LA BÀN NGUYỆN VỌNG

> **Bàn giao 2/4** (theo `docs/PROMPT_THIET_KE_UI_UX.md` §9.2)
> Khung bằng chữ trước khi bằng pixel. Sửa một khung ASCII mất 30 giây, sửa một trang đã code mất 30 phút — và sẽ phải sửa vài lần.
>
> Đọc kèm: [UI_FLOW.md](UI_FLOW.md) · [UI_SPEC.md](UI_SPEC.md)

**Quy ước ký hiệu**

| | |
| :--- | :--- |
| `[ Nhãn ]` | nút | 
| `[[ Nhãn ]]` | **hành động chính** — mỗi màn hình đúng một cái |
| `( ) / (•)` | chip chọn một | 
| `[ ] / [✓]` | chip chọn nhiều |
| `▾ / ▸` | khối mở/thu gọn được |
| `···` | vùng cuộn |

---

## 1. Cổng vào

Nút to nhất **không phải** nút Đăng nhập.

```text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                        🧭  LA BÀN NGUYỆN VỌNG                │
│              Chọn ngành trước, tính điểm sau                 │
│                                                              │
│      ┌────────────────────────────────────────────────┐      │
│      │                                                │      │
│      │   [[  Dùng thử ngay — không cần tài khoản  ]]  │      │
│      │                                                │      │
│      │   ────────────  hoặc đăng nhập  ────────────   │      │
│      │                                                │      │
│      │   Tên đăng nhập                                │      │
│      │   ┌──────────────────────────────────────┐     │      │
│      │   │                                      │     │      │
│      │   └──────────────────────────────────────┘     │      │
│      │   Mật khẩu                                     │      │
│      │   ┌──────────────────────────────────────┐     │      │
│      │   │                                  👁  │     │      │
│      │   └──────────────────────────────────────┘     │      │
│      │                                                │      │
│      │   [ Đăng nhập ]                                │      │
│      │                                                │      │
│      │   ▸ Tài khoản demo                             │      │
│      │     Cán bộ tư vấn   Tuvan_123 / Tuvan_123      │      │
│      │     Quản trị        Admin_T029 / Admin_T029    │      │
│      └────────────────────────────────────────────────┘      │
│                                                              │
│   ⓘ Bản demo học thuật. Không tạo tài khoản thật, không lưu  │
│     dữ liệu sau khi đóng trình duyệt.                        │
│     Điều khoản sử dụng · Chính sách dữ liệu                  │
└──────────────────────────────────────────────────────────────┘
```

**Ba quyết định trên màn này**

1. `[[Dùng thử ngay]]` đứng **trên** ô đăng nhập, không phải dưới. HS là 95% người dùng và HS không có tài khoản — bắt họ đọc qua form đăng nhập trước là bắt đa số phục vụ thiểu số.
2. Đăng nhập sai → lỗi gắn dưới ô Mật khẩu, chữ *"Tên đăng nhập hoặc mật khẩu chưa đúng"* — **không** nói ô nào sai. Đây là bản demo, nhưng thói quen tốt thì tập từ bản demo.
3. Dòng ⓘ nói thẳng đây là demo. `REQUIREMENTS.md` §2.2 đã loại tài khoản khỏi phạm vi; giấu điều đó đi sẽ khiến người chấm tưởng có hệ thống thật rồi hỏi những câu ta không trả lời được.

---

## 2. Học sinh — màn hình rỗng

Màn hình khó nhất của sản phẩm. Ô chat trống không gợi ý gì là lỗi UX nặng nhất của loại app này.

### Phương án A — Gợi ý dạng lưới 2×2, ô nhập ở dưới ⭐ **CHỌN**

```text
┌──────────────────────────────────────────────────────────────┐
│ 🧭 La Bàn Nguyện Vọng            Chế độ dùng thử   ☾  [Thoát] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                                                              │
│         Chào em 👋                                           │
│         Kể cho anh/chị nghe em thích làm gì —                │
│         rồi mình mới bàn tới điểm số.                        │
│                                                              │
│    ┌───────────────────────────┐ ┌──────────────────────────┐│
│    │ Em không biết mình        │ │ Em được 24.5 khối A00,   ││
│    │ thích gì cả               │ │ ngành CNTT Bách Khoa HN  ││
│    │                        →  │ │ lấy bao nhiêu?        →  ││
│    └───────────────────────────┘ └──────────────────────────┘│
│    ┌───────────────────────────┐ ┌──────────────────────────┐│
│    │ Em muốn học ở Đà Nẵng,    │ │ Em muốn làm Data Analyst ││
│    │ học phí dưới 20 triệu     │ │ thì học ngành gì?        ││
│    │                        →  │ │                       →  ││
│    └───────────────────────────┘ └──────────────────────────┘│
│                                                              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────┐ ┌──────┐ │
│  │ Nhắn cho anh/chị…                              │ │  ➤   │ │
│  └────────────────────────────────────────────────┘ └──────┘ │
│  Dữ liệu điểm chuẩn 2023–2025 · tổ hợp A00 A01 B00 C00 D01   │
│  D07 · khu vực Hà Nội · TP.HCM · Đà Nẵng. Đây là gợi ý tham  │
│  khảo, quyết định cuối cùng là của em và gia đình.           │
└──────────────────────────────────────────────────────────────┘
```

### Phương án B — Onboarding 3 bước có thanh tiến trình

```text
┌──────────────────────────────────────────────────────────────┐
│  Bước 1/3 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│         Em thích làm việc với gì nhất?                       │
│                                                              │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│    │ 🔧       │ │ 🔬       │ │ 🎨       │ │ 👥       │       │
│    │ Máy móc  │ │ Phân tích│ │ Sáng tạo │ │ Con người│       │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                              │
│         [ Em chưa rõ, cho em trò chuyện thay ]               │
└──────────────────────────────────────────────────────────────┘
```

### Đánh đổi và lý do chọn A

| | **A — lưới gợi ý + chat** | **B — onboarding 3 bước** |
| :--- | :--- | :--- |
| Ưu | Vào thẳng luồng chat thật; 4 câu gợi ý dạy được phạm vi hệ thống; **khớp trực tiếp với TC01–TC18** nên demo chạy đúng câu đã test | Tỷ lệ hoàn thành cao hơn; ít bỏ dở giữa chừng |
| Nhược | HS vẫn phải gõ nếu 4 câu không đúng ý mình | Đóng khung HS vào 4 lựa chọn cứng — **phản lại chính nguyên tắc §1.4**; và nó biến sản phẩm thành form, mất luôn phần chứng minh ReAct |

**Chọn A.** Sản phẩm này đi thi ở chỗ *agent suy luận nhiều bước*, không ở chỗ *form đẹp*. Onboarding dạng B thu hẹp đầu vào tới mức vòng ReAct chẳng còn gì để quyết — đúng thứ mà bảng Agentic Fit §8 đang phải bảo vệ. 4 nút gợi ý của A **là câu thật trong `test_cases.json`**, nên lúc demo bấm vào chắc chắn ra kết quả tốt.

> Lấy từ B đúng một thứ: **thanh tiến trình**, nhưng dùng cho thẻ MBTI (`Câu 2/4`) chứ không dùng cho cả luồng.

---

## 3. Học sinh — thẻ thu thập thông tin

### Phương án A — Thẻ chèn giữa hội thoại ⭐ **CHỌN (kết hợp)**

```text
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 💬 Em thích phân tích, giải mấy bài toán khó           │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  🧭 Hay đấy — nhóm ngành phân tích khá rộng. Giờ cho          │
│     anh/chị xin điểm để lọc ra trường vừa tầm nhé.           │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Điểm từng môn em đã thi                               │  │
│  │  Chỉ điền môn em có thi — hệ thống tự ghép tổ hợp,     │  │
│  │  em không phải tự cộng.                                │  │
│  │                                                        │  │
│  │  Toán  ┌──────┐   Lý   ┌──────┐   Hoá  ┌──────┐        │  │
│  │        │ 8.5  │        │ 8.0  │        │ 8.0  │        │  │
│  │        └──────┘        └──────┘        └──────┘        │  │
│  │  Sinh  ┌──────┐   Văn  ┌──────┐   Anh  ┌──────┐        │  │
│  │        │      │        │      │        │ 7.5  │        │  │
│  │        └──────┘        └──────┘        └──────┘        │  │
│  │        ▸ Thêm môn Sử · Địa                             │  │
│  │                                                        │  │
│  │                                    [[ Tiếp tục ]]      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  🧭 Tổ hợp tốt nhất của em là **A00 — 24.5 điểm**             │
│     (Toán 8.5 + Lý 8.0 + Hoá 8.0)                            │
│     ▸ Xem 2 tổ hợp khác  ·  A01: 24.0  ·  D07: 24.0          │
```

Trạng thái lỗi của cùng thẻ đó (G-13):

```text
│  │  Toán  ┌──────┐   Lý   ┌──────┐   Hoá  ┌──────┐        │  │
│  │        │ 8.5  │        │ 15   │        │ 8.0  │        │  │
│  │        └──────┘        └━━━━━━┘        └──────┘        │  │
│  │                        ▲ Điểm mỗi môn trong khoảng     │  │
│  │                          0–10. Em kiểm tra lại nhé.    │  │
│  │                                                        │  │
│  │                                    [  Tiếp tục  ]  ← mờ│  │
```

### Phương án B — Sidebar "Hồ sơ của em"

```text
┌──────────────────┬───────────────────────────────────────────┐
│ HỒ SƠ CỦA EM     │  (khung chat chiếm toàn bộ bên phải)      │
│                  │                                           │
│ Điểm từng môn    │                                           │
│  Toán  [ 8.5 ]   │                                           │
│  Lý    [ 8.0 ]   │                                           │
│  Hoá   [ 8.0 ]   │                                           │
│                  │                                           │
│ Khu vực          │                                           │
│  [✓] Hà Nội      │                                           │
│  [ ] TP.HCM      │                                           │
│  [ ] Đà Nẵng     │                                           │
│                  │                                           │
│ Học phí ≤ [ 40 ] │                                           │
│         triệu/năm│                                           │
│                  │                                           │
│ [ Cập nhật ]     │                                           │
└──────────────────┴───────────────────────────────────────────┘
```

### Đánh đổi và lý do chọn **A + phần đọc-được của B**

| | **A — thẻ trong chat** | **B — sidebar form** |
| :--- | :--- | :--- |
| Ưu | Hỏi đúng lúc cần, đúng một nhóm; giữ được cảm giác trò chuyện; **agent chủ động hỏi** là bằng chứng cho Dynamic Decision | Sửa lại dễ; luôn nhìn thấy mình đã khai gì; hợp với Streamlit hơn hẳn |
| Nhược | Muốn sửa điều kiện phải cuộn ngược lên tìm thẻ cũ | Là một form dài trá hình — quay lại đúng cái UX mà §2.C muốn tránh; và nó **hỏi hết mọi thứ trước khi biết có cần không** |

**Chọn A cho phần nhập, lấy của B phần hiển thị.** Cụ thể:

- **Thẻ trong chat** = nơi *nhập* — xuất hiện đúng lúc agent cần, mỗi thẻ một nhóm.
- **Sidebar = bảng tóm tắt chỉ đọc**, tự cập nhật khi HS điền xong. Có đúng một nút `[Sửa]` — bấm vào thì **chèn lại thẻ tương ứng xuống cuối hội thoại**, không mở form riêng.

Cách này giải được nhược điểm chí mạng của A (không biết mình đã khai gì, muốn sửa phải cuộn) mà không rơi vào form dài của B. Trên Streamlit nó cũng rẻ: sidebar là `st.sidebar` đọc thẳng `st.session_state["ho_so"]`, không cần widget có state riêng.

```text
┌──────────────────┐
│ HỒ SƠ CỦA EM     │   ← chỉ đọc, tự điền dần
│                  │
│ Điểm   24.5 (A00)│
│ Sở thích  I, C   │
│ Khu vực  Hà Nội  │
│ Học phí  ≤ 40 tr │
│                  │
│ [ Sửa ]          │
├──────────────────┤
│ Còn thiếu:       │
│ · môn mạnh nhất  │
└──────────────────┘
```

---

## 4. Học sinh — thẻ MBTI rút gọn

Kích hoạt khi HS nói *"em không biết mình thích gì"*. **Hai thẻ lớn bấm được**, không phải radio button nhỏ.

```text
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Câu 2/4     ━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░░░░░░░░░░  │  │
│  │                                                        │  │
│  │  Em thấy mình giống bên nào hơn?                       │  │
│  │                                                        │  │
│  │  ┌──────────────────────┐  ┌──────────────────────┐    │  │
│  │  │  A                   │  │  B                   │    │  │
│  │  │  Em thích việc cụ    │  │  Em thích nghĩ ý     │    │  │
│  │  │  thể, có hướng dẫn   │  │  tưởng mới, hình     │    │  │
│  │  │  rõ ràng             │  │  dung tương lai      │    │  │
│  │  │                      │  │                      │    │  │
│  │  └──────────────────────┘  └──────────────────────┘    │  │
│  │                                                        │  │
│  │  [ ← Quay lại ]              [ Bỏ qua, em tự mô tả ]   │  │
│  └────────────────────────────────────────────────────────┘  │
```

Kết quả — **không dán nhãn tính cách cứng** (G-11):

```text
│  🧭 Theo 4 câu vừa rồi, em có xu hướng thiên về nhóm          │
│     **Nghiên cứu (I)** và **Nguyên tắc (C)**.                 │
│     Đây mới là gợi ý ban đầu thôi — em thấy có đúng không?   │
│                                                              │
│     [ Đúng rồi ]   [ Chưa đúng lắm, để em tự nói ]           │
```

> Vùng bấm mỗi thẻ A/B ≥ 44×44px là mức sàn; ở đây nên để **cả thẻ** bấm được (~120px cao). HS đang căng thẳng, thao tác trên điện thoại — thẻ to giảm bấm nhầm hơn bất kỳ tối ưu nào khác.

---

## 5. Học sinh — đang chạy (streaming + danh sách bước)

Độ trễ thực tế 2–8s/lượt, một phiên đầy đủ 5–7 lần gọi tool. Vòng chờ dài tới mức nó **là** một phần trải nghiệm.

```text
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 💬 Em không biết mình thích gì cả. Em 22 điểm A01,     │  │
│  │    muốn học ở Đà Nẵng.                            [✎]  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  🧭 ▾ Đang tìm cho em…                            (4,6s)     │
│     ✓ Tìm nhóm ngành hợp với xu hướng của em      (1,4s)     │
│     ✓ Tra điểm chuẩn 3 năm gần nhất               (1,1s)     │
│     ⟳ Đối chiếu với mức điểm 22.0 của em…                    │
│                                                              │
│     Với 22 điểm khối A01 và mong muốn học tại Đà             │
│     Nẵng, anh/chị tìm được mấy hướng sau cho em▮             │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────┐ ┌──────┐ │
│  │                                                │ │ ⏹ Dừng│ │
│  └────────────────────────────────────────────────┘ └──────┘ │
└──────────────────────────────────────────────────────────────┘
```

**Bốn quy tắc trên màn này**

1. **Chữ thân thiện, không lộ tên tool.** `⟳ Đang tra điểm chuẩn 3 năm gần nhất…` — **không** `Action: lookup_admission_scores`. Tên tool chỉ hiện ở cổng Quản trị.
2. Danh sách bước **mặc định mở** trong lúc chạy, **tự thu gọn thành một dòng** khi xong: `▸ Đã tra 3 nguồn dữ liệu (4,6s)`. Người dùng bình thường chỉ cần biết đang chạy tới đâu.
3. Nút gửi → **Dừng** trong suốt lúc stream. HS thường nhận ra mình hỏi sai ngay từ câu mở đầu.
4. Icon `[✎]` trên bong bóng của HS: **sửa câu hỏi cũ và chạy lại từ đó**, không bắt gõ lại từ đầu.

Ngưỡng thời gian: `<1s` không hiện gì · `1–3s` chỉ báo đơn giản · `3–10s` nói đang làm gì · `>10s` danh sách bước đầy đủ + nút Dừng nổi bật hơn.

---

## 6. Học sinh — danh sách nguyện vọng ⭐ màn hình quan trọng nhất

### Phương án A — Nhóm theo rủi ro, NV đánh số bên trong

```text
│  ▲ LIỀU (3)                                                  │
│    NV1 …   NV2 …   NV3 …                                     │
│  ◐ VỪA TẦM (4)                                               │
│    NV4 …   NV5 …   NV6 …   NV7 …                             │
│  ● AN TOÀN (3)                                               │
│    NV8 …   NV9 …   NV10 …                                    │
```

### Phương án B — Danh sách phẳng NV1→NV10, huy hiệu rủi ro trên từng dòng

```text
│  NV1  ▲ Liều       Khoa học Máy tính · BKHN                  │
│  NV2  ▲ Liều       …                                         │
│  …                                                           │
│  NV10 ● An toàn    …                                         │
```

### Đánh đổi và lý do chọn A

| | **A — nhóm theo rủi ro** | **B — danh sách phẳng** |
| :--- | :--- | :--- |
| Ưu | **Dạy được chiến lược**: nhìn một cái là thấy "mình có 3 lưới an toàn"; đúng cấu trúc §B6; guardrail G-10 (≥2 An toàn) trở nên nhìn thấy được | Khớp 1-1 với ô nhập trên hệ thống của Bộ; chép sang đỡ nhầm |
| Nhược | Muốn chép sang hệ thống Bộ phải nhảy giữa 3 khối | Mất hoàn toàn thông điệp chiến lược; HS dễ chỉ đọc 3 dòng đầu rồi bỏ — mà 3 dòng đầu chính là 3 lựa chọn **Liều** |

**Chọn A**, và bù nhược điểm bằng ba thứ:

1. **Số NV vẫn chạy liên tục 1→10 xuyên qua các nhóm**, không đánh số lại trong từng nhóm.
2. Nút `[Tải danh sách về (.txt)]` xuất ra **đúng thứ tự phẳng 1→10** để chép sang hệ thống Bộ.
3. Tiêu đề nhóm **giải thích ý nghĩa**, không chỉ dán nhãn: *"AN TOÀN — đây là lưới an toàn của em"*.

Nhược điểm của B không sửa được: một HS đang lo sẽ đọc 3 dòng đầu rồi dừng, và 3 dòng đầu là nhóm Liều. Đó là rủi ro sản phẩm, không phải rủi ro thẩm mỹ.

### Khung đầy đủ

```text
┌──────────────────────────────────────────────────────────────┐
│  Danh sách nguyện vọng gợi ý cho em                          │
│  24.5 điểm · A00 · Hà Nội · học phí ≤ 40 triệu       [ Sửa ] │
├──────────────────────────────────────────────────────────────┤
│  ⓘ Mình đã mở rộng sang TP.HCM và Đà Nẵng vì ở Hà Nội        │
│    chưa đủ lựa chọn an toàn cho mức điểm này.                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ▲ LIỀU — cần may mắn, chỉ nên đặt ở nguyện vọng đầu         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ NV1   Khoa học Máy tính                        ▲ Liều  │  │
│  │       ĐH Bách Khoa Hà Nội                              │  │
│  │                                                        │  │
│  │       Dự báo 2026   26.1 ± 0.5     Em có   24.5        │  │
│  │       ─────────────────────────────────────────        │  │
│  │       Chênh lệch  −1.6 điểm                            │  │
│  │                                                        │  │
│  │       Học phí 35 tr/năm · Hà Nội · chỉ tiêu 680        │  │
│  │                                                        │  │
│  │       ▸ Vì sao gợi ý ngành này                         │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ NV2   Kỹ thuật Điều khiển & Tự động hoá        ▲ Liều  │  │
│  │       ĐH Bách Khoa Hà Nội                    …         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ◐ VỪA TẦM — cân bằng, khả năng đỗ trung bình      (4)       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ NV4   Công nghệ Kỹ thuật Cơ điện tử         ◐ Vừa tầm  │  │
│  │       Trường ĐH Sư phạm Kỹ thuật TP. Hồ Chí            │  │
│  │       Minh                                             │  │
│  │       Dự báo 2026   23.9 ± 1.0     Em có   24.5        │  │
│  │       …                                                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ● AN TOÀN — đây là lưới an toàn của em            (3)       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ NV8   Sư phạm Toán học                       ● An toàn │  │
│  │       …                                                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Đây là gợi ý tham khảo. Quyết định cuối cùng là của em      │
│  và gia đình.                                                │
│                                                              │
│  [[ Tải danh sách về (.txt) ]]  [ Hỏi thêm ]      👍   👎    │
└──────────────────────────────────────────────────────────────┘
```

Khối **"Vì sao gợi ý ngành này"** khi mở ra:

```text
│  │       ▾ Vì sao gợi ý ngành này                         │  │
│  │         Ngành này hợp với xu hướng thích phân tích     │  │
│  │         của em. Nhu cầu tuyển dụng 3 năm qua tăng      │  │
│  │         đều, và mức lương khởi điểm thuộc nhóm cao.    │  │
│  │         Điểm của em còn cách ngưỡng dự báo 1.6 điểm    │  │
│  │         nên đây là lựa chọn cần may mắn — hợp để đặt   │  │
│  │         ở nguyện vọng đầu, không nên là chỗ dựa duy    │  │
│  │         nhất.                                          │  │
```

**Năm quy tắc bắt buộc trên màn này**

1. **Không bao giờ hiện một con số giả vờ chính xác.** Luôn `26.1 ± 0.5`, không bao giờ `26.1` trơ trọi. Biên `b` là cách mã hoá độ bất định vào kết quả — bỏ nó đi là nói dối bằng typography.
2. Mỗi huy hiệu rủi ro có đủ **màu + icon + chữ tiếng Việt** (`▲ Liều`). Bản in đen trắng và người mù màu đều phải đọc được.
3. **Tên trường 60 ký tự phải xuống dòng, không cắt bằng `…`** — xem NV4 ở trên. HS cần biết chính xác trường nào.
4. Banner nới ràng buộc nói rõ **đã nới gì và vì sao**, không phải một dòng "đã điều chỉnh điều kiện tìm kiếm".
5. Câu kết luôn nhắc: **quyết định cuối thuộc về em và gia đình** (G-04).

---

## 7. Học sinh — chặn khi thiếu lưới an toàn (G-10)

Đây là màn hình mà **không render danh sách** mới là hành vi đúng.

```text
┌──────────────────────────────────────────────────────────────┐
│  🧭 Mình chưa tìm đủ phương án an toàn cho em                 │
│                                                              │
│  Với 16.5 điểm khối A00 và mong muốn học ở Hà Nội với        │
│  học phí dưới 20 triệu, mình mới tìm được 1 lựa chọn         │
│  chắc chắn. Một danh sách nguyện vọng chỉ có 1 lưới an       │
│  toàn là quá mỏng — nên mình chưa đưa ra danh sách vội.      │
│                                                              │
│  Mình đã thử mở rộng sang TP.HCM và Đà Nẵng, vẫn chưa đủ.    │
│                                                              │
│  Mấy hướng này vẫn còn mở cho em:                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ 1  Cao đẳng cùng lĩnh vực, có lộ trình liên thông    │    │
│  │    lên đại học sau 2 năm            [ Xem thử → ]    │    │
│  ├──────────────────────────────────────────────────────┤    │
│  │ 2  Xét tuyển bằng học bạ — nhiều trường còn nhận     │    │
│  │                                     [ Xem thử → ]    │    │
│  ├──────────────────────────────────────────────────────┤    │
│  │ 3  Nới ngân sách học phí lên 30 triệu/năm            │    │
│  │    → mở thêm 6 lựa chọn        [ Thử lại với 30 → ]  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Chỗ này nên có thầy cô hướng nghiệp ngồi cùng em một        │
│  buổi. Em mang mấy hướng trên đi hỏi nhé.                    │
└──────────────────────────────────────────────────────────────┘
```

Không có từ *"kém"*, *"thấp"*, *"khó"* (G-03). Mỗi hướng đi là một nút bấm được, không phải một lời khuyên chung chung. Hướng 3 nêu **con số cụ thể sẽ mở thêm được bao nhiêu lựa chọn** — đó là thứ giúp HS quyết định, khác hẳn "em thử nới điều kiện xem sao".

---

## 8. Học sinh — ba màn hình lỗi

**L6 · Chạm trần lặp (G-05)**

```text
│  🧭 Anh/chị tìm hơi lâu mà chưa ra được danh sách đầy đủ.     │
│     Đây là phần đã tìm được — chưa đủ 10 nguyện vọng:        │
│     ┌────────────────────────────────────────────────┐       │
│     │ ● An toàn  Sư phạm Toán · ĐH Vinh   23.3 ± 1.0 │       │
│     │ ● An toàn  Nông học · HV Nông nghiệp 19.1 ± 0.5│       │
│     └────────────────────────────────────────────────┘       │
│     [[ Hỏi lại theo cách khác ]]   [ Giữ 2 lựa chọn này ]    │
```

**L7 · Lỗi API / hết quota**

```text
│  ⚠ Hệ thống đang bận, em thử lại sau 30 giây nhé.            │
│    Phần trò chuyện của em vẫn còn nguyên ở trên.             │
│    [ Thử lại ]                                               │
```

**L8 · Mất mạng giữa lúc stream**

```text
│  🧭 Với 24.5 điểm khối A00, mấy ngành sau đang trong tầm      │
│     với của em: Khoa học Máy tính, Kỹ thuật Điề              │
│     ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄        │
│     ⚠ Câu trả lời bị ngắt giữa chừng.       [ Chạy lại ]     │
```

Cả ba: **giữ nguyên lịch sử hội thoại**, nói được ba điều — chuyện gì xảy ra, ở đâu, **giờ làm gì tiếp**. Câu thứ ba là câu hay bị quên nhất.

---

## 9. Học sinh — mobile 360px

Không phải bản desktop bị nén. Ba thay đổi thật:

```text
┌────────────────────────┐
│ 🧭 La Bàn      ☰   ☾   │  ← sidebar thành ngăn kéo sau ☰
├────────────────────────┤
│ Chào em 👋             │
│ Kể cho anh/chị nghe    │
│ em thích làm gì…       │
│                        │
│ ┌────────────────────┐ │  ← 4 gợi ý xếp DỌC,
│ │ Em không biết mình │ │    không phải lưới 2×2 bị bóp
│ │ thích gì cả     →  │ │
│ └────────────────────┘ │
│ ┌────────────────────┐ │
│ │ Em được 24.5 khối  │ │
│ │ A00, ngành CNTT… → │ │
│ └────────────────────┘ │
│           ···          │
├────────────────────────┤
│ ┌──────────────┐ ┌───┐ │  ← ô nhập dính đáy,
│ │ Nhắn…        │ │ ➤ │ │    trong tầm ngón cái
│ └──────────────┘ └───┘ │
└────────────────────────┘
```

- Thẻ nhập điểm: **2 ô mỗi hàng** thay vì 3, bàn phím số (`inputmode="decimal"`).
- Thẻ nguyện vọng: `Dự báo` và `Em có` xếp **dọc** thay vì hai cột — 26.1 ± 0.5 cạnh 24.5 trên màn 360px thì chữ bé không đọc nổi.
- Sidebar hồ sơ → ngăn kéo sau nút ☰, **mặc định đóng**.

---

## 10. Cán bộ tư vấn — danh sách ca & chấm nhanh

```text
┌──────────────────────────────────────────────────────────────┐
│ 🧭 Cổng Tư vấn          Cô Hương · THPT Chu Văn An   [Thoát]  │
├──────────────────────────────────────────────────────────────┤
│  CHẤM NHANH — học sinh đang ngồi trước mặt                   │
│  ┌───────┐ ┌────────┐ ┌──────────────┐ ┌──────────────────┐  │
│  │ 22.0  │ │  A01 ▾ │ │ Đà Nẵng    ▾ │ │ thích máy móc    │  │
│  └───────┘ └────────┘ └──────────────┘ └──────────────────┘  │
│   điểm      tổ hợp      khu vực          sở thích            │
│                                          [[ Chấm nhanh ]]    │
├──────────────────────────────────────────────────────────────┤
│  CA HÔM NAY (12)     Tìm: [_______________]  Lọc: [ Tất cả ▾]│
│                                                              │
│  Mã ca      HS      Điểm   Kết quả              Trạng thái   │
│  ─────────────────────────────────────────────────────────── │
│  T029-0142  N.V.A   22.0   ●3  ◐4  ▲3   ⚠ đã nới  Đã có DS   │
│  T029-0141  T.T.B   16.5   ●1  ◐2  ▲0   🔴 Đỏ     Cần gặp    │
│  T029-0140  L.M.C   27.8   ●5  ◐3  ▲2   🟢 Xanh   Đã chốt    │
│  T029-0139  P.Q.D   24.5   —              ⟳ đang chạy…       │
│                            ···                               │
└──────────────────────────────────────────────────────────────┘
```

Hai điều đáng chú ý: **Chấm nhanh đứng trên danh sách ca**, vì tình huống thật là HS đang ngồi trước mặt chứ không phải cán bộ đi tra ca cũ. Và cột `Kết quả` dùng đúng bộ icon+màu của HS (`●◐▲`) — cán bộ nói chuyện với HS bằng cùng một từ vựng thì đỡ phải dịch.

---

## 11. Cán bộ tư vấn — chi tiết ca

```text
┌──────────────────────────────────────────────────────────────┐
│ ← Danh sách ca                                               │
│                                                              │
│  Ca #T029-0142 · 22.0 điểm · A01 · Đà Nẵng · RIASEC: R, I    │
│  Kết quả: ● 3 An toàn   ◐ 4 Vừa tầm   ▲ 3 Liều               │
│  Cập nhật 14:32 hôm nay                                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ 🟡 LUỒNG VÀNG                                        │    │
│  │ Đủ 2 lựa chọn An toàn nhưng biên dao động rộng.      │    │
│  │ Cần hỏi thêm ngân sách và môn mạnh trước khi chốt.   │    │
│  └──────────────────────────────────────────────────────┘    │
│  ⚠ Hệ thống đã tự nới khu vực — Đà Nẵng không đủ lựa chọn    │
├──────────────────────────────────────────────────────────────┤
│  BẢNG KẾT QUẢ MÔ HÌNH                          (cuộn ngang →)│
│  Ngành      fit  interest  outlook   P̂₂₀₂₆    Δ     Nhóm  Dữ │
│                                                          liệu│
│  ─────────────────────────────────────────────────────────── │
│  Cơ khí      78    82      4.1 Ổn    20.8±0.9 +1.2  ●    Đủ  │
│  CNTT        71    74      4.6 Bền   23.3±1.0 −1.3  ◐    Đủ  │
│  Kỹ thuật    69    71      3.8 Ổn    21.4±0.5 +0.6  ◐  ⚠Thiếu│
│  Điện                                                  học phí│
├──────────────────────────────────────────────────────────────┤
│  YẾU TỐ THUẬN LỢI            │  YẾU TỐ RỦI RO                │
│  · Sở thích khớp 2/2 mã      │  · Điểm chuẩn ngành dao động  │
│    Holland của ngành         │    mạnh giữa các năm (σ=1.03) │
│  · Nhu cầu tuyển dụng tăng   │  · HS chưa khai ngân sách     │
│    3 năm liên tiếp           │    học phí                    │
│  · Điểm vượt ngưỡng dự báo   │  · Chỉ còn đúng 2 lựa chọn    │
│    1.25 điểm                 │    nhóm An toàn               │
├──────────────────────────────────────────────────────────────┤
│  VIỆC CẦN LÀM                                                │
│  ☐ Hỏi ngân sách học phí/năm            ← thiếu, chặn chốt DS│
│  ☐ Hỏi môn mạnh nhất                                         │
│  ☑ Đã rà lại danh sách với HS                                │
│  Thời gian xử lý ca: 4 phút 12 giây                          │
│                                                              │
│  [[ In cho phụ huynh ]]  [ Chuyển lên chuyên viên ]          │
└──────────────────────────────────────────────────────────────┘
```

Nhãn thiếu dữ liệu (`⚠ Thiếu học phí`) nằm **trên đúng dòng đó**, không gom thành cảnh báo chung ở đầu trang — cán bộ đọc bảng theo dòng.

---

## 12. Quản trị — tổng quan

```text
┌──────────────────────────────────────────────────────────────┐
│ 🧭 Quản trị & Kiểm định     Tổng quan │ Trace │ Đối chứng │  │
│                             Test case │ Guardrail │ Cấu hình │
├──────────────────────────────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐     │
│  │ Phiên     │ │ Vòng TB   │ │ Chạm trần │ │ Độ trễ TB │     │
│  │    48     │ │    4.2    │ │  3 (6.3%) │ │   3.4s    │     │
│  │           │ │  /phiên   │ │           │ │   /lượt   │     │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘     │
│                                                              │
│  Phân bố luồng     🟢 Xanh 31  🟡 Vàng 12  🔴 Đỏ 5           │
│  Lặp trùng action  2      Gọi tool không tồn tại  0          │
│  Tool trả lỗi      7      (chủ yếu: điểm ngoài 0–30)         │
│  Nhánh D kích hoạt 9 phiên (18.8%)                           │
│                                                              │
│  Model: google/gemini-2.5-flash-lite · qua OpenRouter        │
│  MAX_ITERATIONS = 3   ⚠ prompts.py đang để 3, tài liệu ghi 8 │
├──────────────────────────────────────────────────────────────┤
│  PHIÊN GẦN NHẤT                                              │
│  Mã phiên   Câu hỏi gốc            Vòng  Luồng  Trace        │
│  ────────────────────────────────────────────────────────    │
│  S-0048     Em không biết mình…      4    🟡    [ Xem → ]    │
│  S-0047     Em 16.5 điểm A00, thí…   6    🔴    [ Xem → ]    │
│  S-0046     Ngành CNTT học những…    1    🟢    [ Xem → ]    │
└──────────────────────────────────────────────────────────────┘
```

Dòng cảnh báo `⚠ prompts.py đang để 3, tài liệu ghi 8` là **cố ý**: màn hình cấu hình đọc thẳng từ code, và khi code lệch tài liệu thì nói ra. Một bảng quản trị in ra con số lấy từ tài liệu thay vì từ hệ thống chính là kiểu bịa mà sản phẩm này đang chống.

---

## 13. Quản trị — trace một phiên

Mặc định **thu gọn một dòng mỗi bước**. Người xem tổng quan chỉ cần biết chạy tới đâu; người debug mới cần input/output đầy đủ.

```text
┌──────────────────────────────────────────────────────────────┐
│ ← Tổng quan          Phiên S-0048        [Sao chép] [Xuất md]│
├──────────────────────────────────────────────────────────────┤
│  Câu hỏi gốc                                                 │
│  "Em không biết mình thích gì cả. Em 22 điểm A01, muốn       │
│   học ở Đà Nẵng."                                            │
│                                                              │
│  gemini-2.5-flash-lite · OpenRouter · 4 vòng · 4,6s · 3.180 tk│
├──────────────────────────────────────────────────────────────┤
│  ▸ ✓ Bước 1 · mbti_quick_assess("BABA")             (0,9s)   │
│  ▾ ✓ Bước 2 · find_majors_by_interest("I,C")   (1,4s · 5 ng.)│
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Thought                                              │    │
│  │   HS đã cho 4 đáp án MBTI → INTJ → mã Holland I, C.  │    │
│  │   Giờ cần tìm ngành khớp 2 mã này.                   │    │
│  │ Action Input                                         │    │
│  │   {"so_thich": "I,C", "mon_manh": ""}                │    │
│  │ Observation                                          │    │
│  │   [{"ma_nganh":"CNTT","interest_match":74,…},        │    │
│  │    {"ma_nganh":"CO_KHI","interest_match":82,…}, …]   │    │
│  └──────────────────────────────────────────────────────┘    │
│  ▸ ⚠ Bước 3 · filter_universities(khu_vuc=["Đà Nẵng"])       │
│                                       (1,1s · 1 An toàn)     │
│  ▸ ✓ Bước 4 · filter_universities(khu_vuc=[])                │
│                                       (1,2s · nhánh D)       │
│  ─────────────────────────────────────────────────────────   │
│     🏁 Trả lời cuối                                          │
│                                                              │
│  Guardrail đã kích hoạt trong phiên này:                     │
│  G-10 (chặn <2 An toàn) → kéo theo G-11 nhánh D              │
└──────────────────────────────────────────────────────────────┘
```

Khối trace dùng `monospace`. Bước cảnh báo (`⚠ Bước 3`) có nền vàng nhạt + icon, không chỉ đổi màu chữ.

---

## 14. Quản trị — đối chứng Chatbot vs ReAct Agent ⭐ màn hình đi thi

Thiết kế để **chiếu lên máy chiếu đọc được từ hàng cuối**: chữ ≥ 20px, không phải 16px.

```text
┌──────────────────────────────────────────────────────────────┐
│  Câu hỏi   [ Em được 24.5 khối A00, ngành CNTT ĐH Bách Khoa  │
│              HN lấy bao nhiêu?                     ] [[Chạy]]│
├───────────────────────────────┬──────────────────────────────┤
│  CHATBOT THUẦN                │  REACT AGENT                 │
│  không có công cụ             │  4 lần gọi công cụ           │
├───────────────────────────────┼──────────────────────────────┤
│                               │                              │
│  Ngành CNTT ĐH Bách Khoa      │  Điểm chuẩn CNTT — ĐH Bách   │
│  Hà Nội năm 2025 lấy khoảng   │  Khoa Hà Nội, tổ hợp A00:    │
│  ┌─────────┐                  │  2023: ┌──────┐              │
│  │  27.5   │ ← không nguồn    │        │ 25.6 │ ← Bước 2     │
│  └─────────┘                  │  2024: ├──────┤              │
│  điểm. Với ┌──────┐ của em    │        │ 26.0 │              │
│            │ 24.5 │           │  2025: ├──────┤              │
│            └──────┘           │        │ 26.3 │              │
│  thì khá khó, em nên cân      │        └──────┘              │
│  nhắc ┌────────────────┐      │  Dự báo 2026 ┌───────────┐   │
│       │ nguyện vọng 2  │      │              │ 26.1 ± 0.5│   │
│       └────────────────┘.     │              └───────────┘   │
│                               │  ← Bước 3                    │
│                               │  Với 24.5 điểm, chênh −1.6   │
│                               │  → nhóm ⚫ Ngoài tầm         │
│                               │                              │
├───────────────────────────────┼──────────────────────────────┤
│  🔴 3 con số không truy được  │  🟢 4/4 con số truy được về  │
│     về nguồn nào              │     Observation cụ thể       │
│  Không có Observation         │  ▸ Xem trace đầy đủ          │
└───────────────────────────────┴──────────────────────────────┘
```

Ô viền đỏ = con số không truy được về Observation. Ô viền xanh = **hover/bấm vào nhảy tới đúng bước trong trace**. Đây là chỗ biến lập luận trừu tượng thành thứ nhìn thấy được — và là lý do màn này không dùng riêng màu mà kèm cả nhãn `← Bước 2` / `← không nguồn`.

Trên màn hẹp (<900px) hai cột **xếp chồng dọc**, chatbot trên, agent dưới — thứ tự này giữ được mạch "cái sai trước, cái đúng sau".

---

## 15. Quản trị — bộ test case & guardrail

```text
┌──────────────────────────────────────────────────────────────┐
│  BỘ TEST CASE · config/test_cases.json · 19 case             │
│  Đạt 16 · Không đạt 2 · Chưa chạy 1        [[ Chạy tất cả ]] │
│                                                              │
│  Mã    Loại         Kỳ vọng            Tool  KQ      Chạy    │
│  ─────────────────────────────────────────────────────────── │
│  TC01  Đơn giản     0 tool call         0    ✓ Đạt   [ ↻ ]   │
│  TC03  1 tool       T2 → điểm 3 năm     1    ✓ Đạt   [ ↻ ]   │
│  TC04  Multi-tool   T0→T1→T3            3    ✓ Đạt   [ ↻ ]   │
│  TC05a Edge case    hỏi lại, không lặp  1    ✗ Không [ ↻ ]   │
│        ▾ Kỳ vọng: agent hỏi lại người dùng 1 lần             │
│          Thực tế: gọi lại filter_universities cùng tham số   │
│          → G-08 chưa chặn được. Xem trace S-0031 →           │
│  TC06  Nhánh D      T1→T3→T3 (nới)      3    ⟳ …     [ ↻ ]   │
├──────────────────────────────────────────────────────────────┤
│  GUARDRAIL                                                   │
│  Mã    Rủi ro                       Kích hoạt  Gần nhất      │
│  ─────────────────────────────────────────────────────────── │
│  G-05  Vòng lặp vô hạn                    3    S-0047 →      │
│  G-08  Lặp trùng action                   2    S-0031 →      │
│  G-10  Danh sách không có lưới an toàn    9    S-0047 →      │
│  G-01  Khẳng định "chắc chắn đỗ"          0    ⓘ chưa được   │
│                                                kiểm chứng    │
│  G-09  Rò rỉ PII                          0    ⓘ chưa được   │
│                                                kiểm chứng    │
└──────────────────────────────────────────────────────────────┘
```

Guardrail chưa từng kích hoạt lần nào được đánh dấu **"chưa được kiểm chứng"**, không phải dấu ✓ xanh. Chưa chạy không đồng nghĩa với an toàn — và đây chính xác là câu mà người chấm chéo sẽ hỏi.

Case không đạt **mở ngay tại chỗ** thành kỳ vọng / thực tế / link tới trace. Bắt người debug bấm sang trang khác rồi tự đối chiếu trong đầu là chỗ mất thời gian nhất của loại bảng này.

---

## Tổng kết — cái gì to nhất trên mỗi màn hình

Kiểm tra cuối: cái to nhất phải là cái quan trọng nhất **với người dùng**, không phải với nhóm làm sản phẩm.

| Màn hình | Hành động chính duy nhất | Vì sao không phải cái khác |
| :--- | :--- | :--- |
| Cổng vào | `[[Dùng thử ngay]]` | HS không có tài khoản |
| Chat rỗng | 4 thẻ gợi ý | Ô nhập trống là rào cản, không phải lời mời |
| Thẻ nhập điểm | `[[Tiếp tục]]` | Mọi ô đều tuỳ chọn trừ việc đi tiếp |
| Đang chạy | `[Dừng]` | Người dùng nhận ra hỏi sai từ câu mở đầu |
| Danh sách NV | `[[Tải danh sách về]]` | Đây là thứ HS mang đi dùng thật |
| Chặn thiếu An toàn | 3 nút hướng đi | Không có hướng đi thì màn hình này chỉ là lời từ chối |
| Chi tiết ca | `[[In cho phụ huynh]]` | Ca kết thúc khi phụ huynh gật, không khi cán bộ đọc xong |
| Đối chứng | `[[Chạy]]` | Cả màn hình tồn tại để chạy một câu và so hai cột |
