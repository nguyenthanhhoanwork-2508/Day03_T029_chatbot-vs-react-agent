# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)

*Dành cho Role 5: Observability & Reviewer*

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX)

Đề tài xây dựng chatbot định hướng ngành học và sắp xếp nguyện vọng cho học sinh lớp 12 sau khi có điểm thi THPT.

| Tiêu chí                       |  Điểm (1-5)  | Lý do đánh giá                                                                                                                                                     |
| :------------------------------- | :-------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🧠**Multi-step Reasoning** |     `5/5`     | Hệ thống phải phân tích sở thích, gợi ý ngành, tra cứu điểm chuẩn, đánh giá khả năng trúng tuyển và lọc theo khu vực, học phí.               |
| 🛠️**Tool Interaction**   |     `5/5`     | Agent cần dùng công cụ để tra cứu điểm chuẩn, học phí, trường đào tạo và triển vọng nghề nghiệp, tránh đưa ra thông tin không có căn cứ. |
| 🔀**Dynamic Decision**     |     `5/5`     | Luồng tư vấn thay đổi theo từng học sinh. Khi chưa rõ sở thích hoặc thiếu lựa chọn an toàn, Agent phải chủ động chuyển hướng phù hợp.         |
| ⏳**Long Horizon**         |     `4/5`     | Một phiên tư vấn gồm nhiều lượt hỏi đáp và gọi công cụ; Agent phải duy trì điểm thi, tổ hợp, sở thích, khu vực và ngân sách trong phiên.   |
| **TỔNG ĐIỂM FIT**       | **19/20** | **KẾT LUẬN: BÀI TOÁN RẤT PHÙ HỢP VỚI REACT AGENT.**                                                                                                      |

### Kết luận

Bài toán cần kết hợp thông tin cá nhân, dữ liệu tuyển sinh và nhiều bước xử lý nên phù hợp với ReAct Agent. Tuy nhiên, các câu hỏi kiến thức chung vẫn có thể được Chatbot trả lời trực tiếp để tiết kiệm thời gian và chi phí.

> **Lưu ý:** Đây là điểm đánh giá mức độ phù hợp của bài toán, không phải điểm hiệu năng thực tế của Agent.

---

## 🔍 2. ĐÁNH GIÁ

## 🤖 CHATBOT BASELINE

Kết quả lấy nguyên văn từ `baseline_output.txt`, chạy trên 24 `test_cases[].input` bằng `OpenRouterProvider` và model `google/gemini-2.5-flash-lite`. Baseline không gọi tool và không có Observation từ dữ liệu tuyển sinh/thị trường. File log không ghi system prompt thực tế, nên đánh giá dưới đây chỉ kết luận từ hành vi quan sát được.

|    Test case    | Tool calls | Phân loại                           | Kết quả chính                                                                                         |
| :-------------: | :--------: | :------------------------------------ | :------------------------------------------------------------------------------------------------------- |
| **TC01** |   `0`   | `Correct`                           | Trả lời đúng kiến thức nền CNTT, không cần dữ liệu thực tế.                                 |
| **TC02** |   `0`   | `Acceptable with caveat`            | Đúng ý ưu tiên nhưng thiếu nguyên tắc các NV được xét bình đẳng về điểm chuẩn.      |
| **TC03** |   `0`   | `Hallucinated / Ungrounded`         | Tự nêu khoảng điểm chuẩn và trường thay thế không có nguồn.                                 |
| **TC04** |   `0`   | `Unsupported inference / Failed`    | Suy sở thích từ điểm môn, bỏ qua survey và tự liệt kê trường/ngành.                        |
| **TC05a** |   `0`   | `Failed input guard`                | Chấp nhận 12/18/15 và tổng A00 = 45 như dữ liệu hợp lệ.                                         |
| **TC05b** |   `0`   | `Failed guard + Hallucinated`       | Chấp nhận 45 điểm và đưa nhiều khoảng điểm chuẩn không nguồn.                              |
| **TC06** |   `0`   | `Partially relevant / Ungrounded`   | Gợi ý đúng hướng cơ khí/cao đẳng nhưng không tính 16.5 hay xác minh học phí.             |
| **TC07** |   `0`   | `Truncated / Failed`                | Bị cắt giữa câu, chưa xử lý đủ hai khu vực và học phí.                                      |
| **TC08** |   `0`   | `Truncated / Failed`                | Bị cắt trước danh sách, không chứng minh gộp đủ ba khu vực.                                   |
| **TC09** |   `0`   | `Truncated / Failed`                | Bị cắt, không hoàn tất tư vấn hoặc cơ chế khu vực mặc định.                                |
| **TC10** |   `0`   | `Out-of-scope / Ungrounded`         | Hiểu Sài Gòn nhưng vẫn tư vấn Cần Thơ ngoài phạm vi dataset.                                  |
| **TC11** |   `0`   | `Correct boundary, failed safety`   | Chấp nhận đúng 10/10/10 nhưng nói gần như/chắc chắn có suất.                                 |
| **TC12** |   `0`   | `Unsupported / Not executed`        | Tự viết unit test giả định, không chạy boundary matrix trên tool thật.                          |
| **TC13** |   `0`   | `Hallucinated / Wrong risk method`  | Tự nêu khoảng 24–26, không tính biên dao động từ dữ liệu ba năm.                            |
| **TC14** |   `0`   | `Truncated / Failed`                | Bị cắt, không xử lý hội thoại survey`BAB` → `baba`.                                          |
| **TC15** |   `0`   | `Acceptable with caveat`            | Kiến thức nghề bác sĩ hợp lý nhưng không truy vết được về Observation.                     |
| **TC16** |   `0`   | `Hallucinated / Ungrounded`         | Tự đưa lương 7–15 và trên 20 triệu/tháng, không có nguồn thị trường.                     |
| **TC17** |   `0`   | `Safe fallback but incomplete`      | Thừa nhận không có điểm chuẩn, không bịa số nhưng bị cắt và thiếu phương án thay thế. |
| **TC18** |   `0`   | `Ungrounded estimate`               | Không cam kết đỗ nhưng tự nêu các khoảng 22–29 điểm theo nhóm trường.                     |
| **TC19** |   `0`   | `Hallucinated / Failed`             | Mô tả biểu đồ tưởng tượng với ba số điểm minh họa không nguồn.                           |
| **TC20a** |   `0`   | `Partial boundary, failed workflow` | Chấp nhận điểm 0 nhưng không tính A01 tối ưu và tư vấn không nguồn.                        |
| **TC20b** |   `0`   | `Data corruption / Failed guard`    | Tự đổi Lý = −5 thành +5 và chuyển sai sang tư vấn trường THPT.                               |
| **TC21** |   `0`   | `Incomplete / Failed`               | Không chỉ ra cần thêm Tiếng Anh để có D01; gợi ý khối khi mới có hai môn.                  |
| **TC22** |   `0`   | `Arithmetic hallucination / Failed` | Tính sai 8.5 + 8 + 8 thành 26.5 thay vì 24.5, rồi bịa điểm chuẩn.                                |

### Nhóm 1 — Kiến thức nền (TC01, TC02, TC15)

### 🤖 Chatbot Baseline:

* **Phản hồi tiêu biểu**: TC01 trình bày đúng các nhóm môn CNTT và hướng chuyên sâu; TC02 giải thích thứ tự ưu tiên nguyện vọng; TC15 nêu ngành Y đa khoa và kỹ năng nghề bác sĩ.
* **Phân loại**: 1 Correct, 2 Acceptable with caveat.
* **Ảo giác**: Không thấy số liệu tuyển sinh bị bịa ở TC01–TC02. TC15 nhìn chung hợp lý nhưng chi tiết đào tạo/hành nghề không có nguồn truy vết.
* **Nhận xét**: Đây là nhóm baseline làm tốt nhất. TC02 vẫn thiếu ý các nguyện vọng được xét bình đẳng về điểm chuẩn; phản hồi nhìn chung dài hơn cần thiết.

### Nhóm 2 — Dữ liệu tuyển sinh và thị trường (TC03, TC13, TC16, TC18, TC19)

### 🤖 Chatbot Baseline:

* **Phản hồi tiêu biểu**: TC03 nói CNTT Bách khoa Hà Nội thường trên 27, có năm 28–29; TC13 tự ước lượng Sư phạm Toán ĐH Vinh 24–26; TC16 nêu lương CNTT 7–15 hoặc trên 20 triệu/tháng; TC19 tạo các điểm “minh họa” 28.25/28.00/29.05.
* **Phân loại**: Hallucinated / Ungrounded.
* **Ảo giác**: Các con số nghe hợp lý nhưng không đến từ tool, Observation hay nguồn có timestamp. Cảnh báo “tham khảo/minh họa” không biến số tự tạo thành dữ liệu đáng tin.
* **Nhận xét**: Chỉ TC17 ở nhóm trường ngoài dữ liệu chủ động nói không biết. Hành vi fallback vì vậy không nhất quán giữa các câu hỏi cùng cần dữ liệu thực tế.

### Nhóm 3 — Validation và tính toán (TC05a, TC05b, TC20b, TC22)

### 🤖 Chatbot Baseline:

* **Phản hồi tiêu biểu**: TC05a/TC05b coi 45 điểm A00 là hợp lệ; TC20b đổi im lặng Lý = −5 thành +5; TC22 tính `8.5 + 8 + 8 = 26.5` thay vì 24.5.
* **Phân loại**: Failed input guard / Data corruption / Arithmetic hallucination.
* **Ảo giác**: Không chỉ thiếu dữ liệu thực tế, model còn làm sai hoặc tự sửa dữ liệu đầu vào. TC20b sau đó chuyển nhầm bối cảnh từ đại học sang tuyển sinh THPT.
* **Nhận xét**: Đây là nhóm lỗi nghiêm trọng nhất vì output vẫn trôi chảy và tự tin, khiến người dùng khó nhận ra tư vấn đang dựa trên điểm không tồn tại.

### Nhóm 4 — Workflow, ràng buộc và phạm vi (TC04, TC06, TC10, TC12, TC20a, TC21)

### 🤖 Chatbot Baseline:

* **Phản hồi tiêu biểu**: TC04 suy sở thích từ điểm thay vì survey; TC06 có gợi ý cao đẳng nhưng không chứng minh nhánh nới ràng buộc; TC10 tư vấn Cần Thơ ngoài phạm vi; TC12 tự dựng code test; TC21 không chỉ ra thiếu Tiếng Anh để ghép D01.
* **Phân loại**: Unsupported workflow / Out-of-scope / Incomplete.
* **Ảo giác**: Baseline tự lấp phần còn thiếu bằng suy diễn hoặc danh sách trường/ngành từ trí nhớ, thay vì tuân thủ schema, enum khu vực và pipeline.
* **Nhận xét**: TC20a chấp nhận đúng điểm 0 nhưng không tính A01 = 22.5 là tổ hợp tối ưu. Điều này cho thấy xử lý được ngôn ngữ không đồng nghĩa với thực thi đúng nghiệp vụ nhiều bước.

### Nhóm 5 — Độ hoàn chỉnh output và safety (TC07, TC08, TC09, TC11, TC14, TC17)

### 🤖 Chatbot Baseline:

* **Phản hồi tiêu biểu**: TC07, TC08, TC09, TC14 và TC17 đều kết thúc giữa câu. TC11 chấp nhận đúng cận 30 nhưng nói “gần như chắc chắn sẽ có suất” và “chắc chắn” đạt điều kiện ở FPT.
* **Phân loại**: Truncated / Failed; Correct boundary, failed safety.
* **Ảo giác**: TC17 là trường hợp tốt khi model thừa nhận không có điểm chuẩn và không bịa số. Ngược lại, TC11 biến điểm cao thành cam kết tuyển sinh chưa được kiểm chứng.
* **Nhận xét**: Năm phản hồi bị cắt khiến yêu cầu không hoàn thành; cần log `max_tokens` và trạng thái kết thúc để phân biệt giới hạn provider với lỗi nội dung model.

---

### 2.3. Kết luận Baseline

* Baseline làm tốt nhất với kiến thức nền ổn định: TC01 đạt đầy đủ; TC02 và TC15 hữu ích nhưng còn caveat.
* Khi cần dữ liệu tuyển sinh hoặc thị trường, model thường trả lời từ trí nhớ thay vì thừa nhận không biết. Ví dụ rõ nhất là điểm chuẩn ở TC03/TC13/TC18, lương ở TC16 và số “minh họa” ở TC19.
* Guardrail đầu vào không đáng tin cậy: TC05a/TC05b chấp nhận 45 điểm A00; TC20b tự đổi −5 thành +5; TC22 tính sai `8.5 + 8 + 8` thành 26.5.
* Có 5 phản hồi bị cắt giữa câu: TC07, TC08, TC09, TC14 và TC17.
* Chỉ TC17 chủ động thừa nhận không có dữ liệu thực tế và không bịa điểm chuẩn, cho thấy khả năng fallback của baseline không nhất quán.
* Cả 24 case đều có 0 tool call và không có Observation. Chỉ TC01 đáp ứng trọn vẹn acceptance criteria; phần lớn case nghiệp vụ, dữ liệu thực tế và edge case không đạt.

> **Kết luận:** Chatbot Baseline có biểu hiện ảo giác và không biết dữ liệu thực tế một cách nhất quán. Nó phù hợp với kiến thức chung, nhưng không đủ an toàn cho tính điểm, tra điểm chuẩn/học phí/lương, phân nhóm rủi ro, lọc trường hoặc xếp nguyện vọng. Các tác vụ này cần backend validation và ReAct Agent có tool để grounding.

> **Giới hạn phép thử:** `baseline_output.txt` không ghi system prompt hoặc tham số sinh; báo cáo vì vậy không quy lỗi cho riêng prompt hay model. Lần chạy sau nên log thêm system prompt identifier, temperature, max tokens, timestamp, provider/model và số tool call để so sánh A/B tái lập được.

### Nguồn đối chiếu

* [O*NET Interest Profiler](https://www.onetcenter.org/reports/IP_Manual.html) — mô hình RIASEC, các phiên bản công cụ và tài liệu về độ tin cậy/độ giá trị.
* [Bộ GDĐT — cấu trúc kỳ thi THPT 2026](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/ky-thi-tot-nghiep-thpt-nam-2026-giu-on-dinh-mot-so-dieu-chinh-khong-anh-huong-toi-thi-sinh-226.html) — phương án hai môn bắt buộc và hai môn tự chọn.
* [Bộ GDĐT — đăng ký xét tuyển](https://moet.gov.vn/content/vanban/Lists/VBDH/Attachments/3955/qd-cb-tthc-quy-che-06.pdf) — nguyện vọng được xếp theo mức ưu tiên; nếu đủ điều kiện ở nhiều nguyện vọng thì chỉ công nhận nguyện vọng cao nhất.
* [Đại học Bách khoa Hà Nội — điểm chuẩn và học phí 2025](https://www.hust.edu.vn/vi/news/hoat-dong-chung/dai-hoc-bach-khoa-ha-noi-cong-bo-diem-chuan-xet-tuyen-dai-hoc-nam-2025-655575.html) — nguồn chính thức để đối chiếu các nhận định tuyển sinh do baseline tự nêu.

## 🧠 REACT AGENT

### 3.1. Thiết lập phép thử

Kết quả lấy nguyên văn từ `react_output.txt`, chạy trên 24 `test_cases[].input` bằng backend `ReAct Agent`, `OpenRouterProvider` và model `google/gemini-2.5-flash-lite`. Tổng cộng Agent thực hiện **44 tool call**; 10/24 case kết thúc với `Is error: True` do chạm giới hạn 3 bước.

`react_output.txt` chỉ lưu câu hỏi, số tool call, trạng thái lỗi và Final Answer. Để hoàn thành checklist Role 5 Mốc 3, nhóm đã bổ sung chế độ trace đánh giá và kiểm toán lại TC03, TC04, TC14, TC16. Trace có thể tái tạo bằng `src/run_react_trace.py`; UI công khai vẫn không hiển thị Thought/Action/Observation.

> **Phạm vi “thông tin thực tế”:** Agent được grounding vào hai JSON nội bộ. Hai dataset này tự ghi rõ là **dữ liệu mô phỏng phục vụ học tập**, không phải dữ liệu tuyển sinh/thị trường thời gian thực. Cụm “đã được kiểm chứng” trong Final Answer chỉ nên hiểu là đã truy xuất từ dataset nội bộ, không phải đã xác minh với nguồn chính thức hiện hành.

|    Test case    | Tool calls |   Error   | Phân loại                                | Kết quả chính                                                                                                  |
| :-------------: | :--------: | :-------: | :----------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **TC01** |   `0`   | `False` | `Safe but incomplete`                    | Không bịa số nhưng né câu hỏi kiến thức đơn giản, chỉ hỏi lại.                                     |
| **TC02** |   `1`   | `False` | `Safe refusal / unnecessary tool`        | Không bịa quy chế nhưng gọi tool không cần thiết và không trả lời kiến thức nền.                   |
| **TC03** |   `2`   | `False` | `Partially grounded`                     | Điểm 28.8 và dải 28.3–28.8 khớp tool; thiếu trường thay thế phù hợp và gọi 2025 là “dự đoán”. |
| **TC04** |   `3`   | `True` | `Guardrail fallback`                     | Dừng an toàn sau 3 bước, không hoàn thành survey/Đà Nẵng.                                               |
| **TC05a** |   `1`   | `False` | `Failed input validation`                | Chấp nhận tổng A00 = 45 và tiếp tục hỏi năm/vùng.                                                        |
| **TC05b** |   `3`   | `True` | `Guardrail fallback`                     | Không bịa danh sách trường nhưng không phát hiện điểm sai trước khi hết bước.                     |
| **TC06** |   `2`   | `False` | `Grounded but incomplete`                | Dải 20.8–26.7 và học phí 26–32 khớp tool; chưa chạy nhánh nới ràng buộc.                             |
| **TC07** |   `2`   | `False` | `Grounded data, wrong inference`         | Số TMU/UEH đúng nhưng nói 22.5 có khả năng vào mức chuẩn 27.0.                                         |
| **TC08** |   `3`   | `True` | `Guardrail fallback`                     | Không tổng hợp được ba khu vực trong 3 bước.                                                             |
| **TC09** |   `1`   | `True` | `Guardrail fallback`                     | Dừng an toàn nhưng không hoàn thành tư vấn khi thiếu khu vực.                                           |
| **TC10** |   `2`   | `True` | `Guardrail fallback`                     | Không xử lý xong alias Sài Gòn và Cần Thơ.                                                                |
| **TC11** |   `3`   | `True` | `Guardrail fallback`                     | Không cam kết chắc chắn nhưng không hoàn thành case biên 30 điểm.                                      |
| **TC12** |   `0`   | `False` | `Toolset mismatch detected`              | Nói đúng`filter_universities` không có trong registry hiện tại.                                          |
| **TC13** |   `2`   | `False` | `Safe fallback / grounded list`          | Không bịa điểm ĐH Vinh; liệt kê đúng các trường có trong dataset hiện tại.                         |
| **TC14** |   `2`   | `False` | `Hallucinated despite tools`             | Bóp méo số tin tuyển dụng, tăng trưởng, điểm chuẩn, học phí và tự thêm lương.                   |
| **TC15** |   `1`   | `False` | `Safe refusal / wrong coverage`          | Không bịa nghề bác sĩ nhưng chọn nhầm luồng tool và không trả lời kiến thức nghề.                 |
| **TC16** |   `2`   | `False` | `Partially grounded / distorted summary` | Biết dataset không có lương nhưng mô tả sai xu hướng Miền Trung và bỏ số liệu tool.                |
| **TC17** |   `2`   | `True` | `Guardrail fallback`                     | Không bịa trường ngoài dữ liệu nhưng không đưa phương án thay thế.                                 |
| **TC18** |   `1`   | `False` | `Safe clarification`                     | Hỏi trường/vùng thay vì tự bịa điểm chuẩn; tool call chưa cần thiết.                                 |
| **TC19** |   `3`   | `True` | `Guardrail fallback`                     | Không bịa biểu đồ/số liệu nhưng không trả bảng văn bản.                                              |
| **TC20a** |   `3`   | `True` | `Guardrail fallback`                     | Không bình phẩm điểm 0 nhưng không tính tổ hợp tối ưu.                                                |
| **TC20b** |   `1`   | `False` | `Failed input validation`                | Không phát hiện Lý = −5, tiếp tục hỏi năm/ngành/vùng.                                                  |
| **TC21** |   `3`   | `True` | `Guardrail fallback`                     | Không tự điền môn thiếu nhưng không chỉ ra cần thêm Tiếng Anh cho D01.                                |
| **TC22** |   `1`   | `False` | `Grounded benchmark, corrupted premise`  | Điểm BKA 28.8 đúng tool nhưng tin tổng tự khai 27 thay vì cộng lại thành 24.5.                         |

### 3.2. Kiểm toán trace Thought → Action → Observation

| Test case | Tool selection | Observation và tổng hợp | Termination |
| :-------: | :------------- | :---------------------- | :---------- |
| **TC03** | Chọn đúng tool tuyển sinh theo trường và nhóm ngành. | Observation chứa điểm BKA 28.8 và dải 28.3–28.8; Final Answer bám số nhưng diễn giải sai dữ liệu 2025 là dự đoán. | Kết thúc bằng Final Answer sau 2 tool call. |
| **TC04** | Không có tool khảo sát RIASEC/MBTI nên chuyển qua các tool không giải quyết đủ yêu cầu. | Observation không đủ để suy ra nhóm nghề và trường tại Đà Nẵng. | Chạm `max_iterations` sau 3 bước và trả fallback có kiểm soát. |
| **TC14** | Gọi đúng luồng dữ liệu thị trường và tuyển sinh nhưng thiếu tool yêu cầu nghề nghiệp. | Final Answer bóp méo nhiều số đã có trong Observation và tự thêm khoảng lương không được tool cung cấp. | Kết thúc bằng Final Answer sau 2 tool call, nhưng factuality không đạt. |
| **TC16** | Gọi dữ liệu thị trường cho các vùng liên quan. | Nhận biết dataset không có lương, nhưng làm mất số cụ thể và diễn giải sai xu hướng Miền Trung khi tổng hợp. | Kết thúc bằng Final Answer sau 2 tool call. |

Runner xuất từng model step, Action đã parse, trạng thái tool có được thực thi hay không, Observation, số tool call và lý do kết thúc. Có thể tái tạo phép kiểm toán bằng lệnh:

```powershell
.\.venv\Scripts\python.exe src\run_react_trace.py --ids TC03 TC04 TC14 TC16 --output react_trace_output.txt
```

File output là artifact cục bộ của mỗi lần chạy và không cần commit; kết quả có thể thay đổi theo model/provider. Các nhận xét dưới đây dựa trên lần chạy đã ghi trong `react_output.txt` và lần kiểm toán trace nêu trên.

### 3.3. Quan sát grounding và ảo giác

### Nhóm 1 — Grounding hoạt động đúng hoặc tương đối đúng

### 🧠 ReAct Agent:

* **TC03**: Điểm Khoa học máy tính BKA 28.8 và dải IT Miền Bắc 28.3–28.8 khớp output của `get_admission_by_university`/`get_admission_by_major_group`. Đây là cải thiện rõ so với Baseline vốn dùng khoảng 27–29 từ trí nhớ.
* **TC06**: Dải điểm nhóm Sản xuất–Cơ khí 20.8–26.7 và học phí 26–32 triệu/năm khớp dataset. Agent kết luận ràng buộc dưới 20 triệu chưa được đáp ứng mà không tự bịa trường.
* **TC13**: Khi ĐH Vinh không có trong dataset, Agent nói thẳng chưa có dữ liệu và đưa danh sách trường đang hỗ trợ thay vì tự ước lượng 24–26 như Baseline.
* **TC18**: Khi chưa có trường/vùng, Agent hỏi lại thay vì đưa ngay các khoảng điểm chuẩn tưởng tượng.
* **Nhận xét**: Tool giúp giảm ảo giác rõ rệt khi model sử dụng Observation đúng. Tuy nhiên TC03 vẫn gọi điểm 2025 là “được dự đoán”, trong khi dataset chỉ ghi đây là điểm chuẩn mô phỏng của năm 2025.

### Nhóm 2 — Có tool nhưng vẫn ảo giác hoặc suy luận sai

### 🧠 ReAct Agent:

* **TC14 — lỗi nghiêm trọng nhất**: Tool thực tế cho IT Miền Nam năm 2025 là **25.400 tin, +13.4%**; Final Answer lại ghi **hơn 125.800 tin trong 2024, +15%**, tự thêm lương **15–30 triệu/tháng** dù tool không có trường lương.
* Cùng TC14, tool tuyển sinh cho IT Miền Nam trả dải **24.5–28.8**; Agent đổi thành **23.0–25.6**, nói An toàn thông tin UIT 23.0 và Mạng máy tính 23.2 trong khi dataset lần lượt là **27.2** và **26.1**. Agent còn ghi học phí QSB/UIT 12–15 triệu, trong khi dataset là **30/35 triệu**.
* **TC07**: TMU 27.0 và UEH 27.3 là số liệu đúng tool, nhưng tổng D01 từ điểm người dùng là 22.5. Agent vẫn nói người dùng “có khả năng trúng tuyển” TMU — một phán quyết không theo phép so sánh chính số liệu đã có.
* **TC16**: Tool cho cả ba miền đều “tăng mạnh” (Miền Bắc +15.0%, Miền Nam +13.4%, Miền Trung +12.0%); Final Answer lại gọi Miền Trung “tăng trưởng ổn định” và bỏ toàn bộ số cụ thể.
* **TC22**: Điểm BKA 28.8 có grounding, nhưng Agent tin con số người dùng tự khai là 27. Tổng đúng của 8.5 + 8.0 + 8.0 phải là 24.5; kết luận cuối vì vậy được xây trên tiền đề sai.
* **Kết luận nhóm**: ReAct không tự động bảo đảm factuality. Observation đúng vẫn có thể bị model chép sai, pha thêm kiến thức ngoài tool hoặc suy luận sai ở bước tổng hợp.

### Nhóm 3 — Guardrail dừng vòng lặp

### 🧠 ReAct Agent:

* 10 case chạm fallback sau tối đa 3 bước: **TC04, TC05b, TC08, TC09, TC10, TC11, TC17, TC19, TC20a, TC21**.
* Điểm tích cực: tất cả đều dừng có kiểm soát, không crash, không lặp vô hạn và không xuất lộ Thought/Action/Observation ra UI.
* Điểm hạn chế: fallback dùng cùng một câu chung cho mọi nguyên nhân, không giữ lại kết quả từng phần đã thu được và không nói tool/tham số nào còn thiếu.
* `MAX_ITERATIONS = 3` thấp hơn requirement là 8 và không đủ cho các case cần liệt kê options → tra ngành/vùng → tổng hợp. Số fallback cao chủ yếu phản ánh lệch kiến trúc/toolset, không chỉ năng lực model.

### Nhóm 4 — Validation và toolset không khớp acceptance tests

### 🧠 ReAct Agent:

* **TC05a/TC20b**: Backend không có tầng validate điểm trước ReAct, nên 45 điểm hoặc Lý = −5 vẫn lọt vào model/tool loop.
* **TC20a/TC21/TC22**: Không có hàm tính tổ hợp, nên Agent không xác định A01 tối ưu, môn còn thiếu hoặc mâu thuẫn giữa tổng tự khai và tổng từng môn.
* **TC04/TC14/TC15**: Registry không có MBTI/RIASEC và `lookup_career_requirements`, nên model phải dùng nhầm các tool thị trường/tuyển sinh hoặc fallback.
* **TC12**: Agent nhận ra `filter_universities` không tồn tại. Đây là phản hồi đúng theo code hiện tại, nhưng cũng xác nhận bộ 24 test case đang nhắm tới toolset khác với 8 tool thực tế trong `AVAILABLE_TOOLS`.
* **Nhận xét**: Không nên dùng các failure này để kết luận riêng rằng prompt ReAct yếu; trước hết phải đồng bộ requirement, fixtures và tool registry.

### 3.4. So sánh Baseline và ReAct Agent

| Tiêu chí                   | Baseline                                    | ReAct Agent                                                        |
| :--------------------------- | :------------------------------------------ | :----------------------------------------------------------------- |
| Kiến thức chung            | Trả lời đầy đủ hơn ở TC01/TC02/TC15 | Quá phụ thuộc tool, thường hỏi lại hoặc từ chối          |
| Grounding số liệu          | 0 tool; số liệu không truy vết          | 44 tool call; nhiều số khớp dataset ở TC03/TC06/TC07/TC13      |
| Ảo giác số liệu          | Thường xuyên ở điểm chuẩn/lương    | Giảm nhưng chưa hết; TC14 bóp méo Observation nghiêm trọng |
| Input validation             | Fail 45, −5 và phép cộng                | Vẫn fail vì backend chưa có validator/tính tổ hợp           |
| Termination                  | Có 5 output bị cắt                       | 10 fallback có kiểm soát, không crash/lặp vô hạn            |
| Hoàn thành acceptance test | 1/24 case đầy đủ                        | 0/24 case đầy đủ theo tiêu chí hiện tại                    |
| Tính tái lập              | Không có nguồn                           | Tốt hơn nhờ tool deterministic, nhưng log thiếu raw trace     |

### 3.5. Kết luận ReAct Agent

* ReAct Agent **giảm ảo giác nhưng chưa loại bỏ ảo giác**. Khi Observation được dùng nguyên vẹn, câu trả lời có căn cứ hơn Baseline; khi model diễn giải lại, nó vẫn có thể thay đổi số hoặc thêm dữ liệu không tồn tại.
* Agent **không có dữ liệu thời gian thực**. Nó chỉ biết dữ liệu mô phỏng 2024–2025 trong hai file JSON; vì vậy không nên gọi output là số liệu tuyển sinh/thị trường thực tế đã xác minh.
* Guardrail vòng lặp hoạt động: 10 case dừng an toàn sau 3 bước, không crash. Tuy nhiên tỷ lệ fallback `41.7%` là quá cao và câu fallback chưa tận dụng kết quả từng phần.
* Lỗi TC14 chứng minh cần guardrail hậu kiểm: mọi con số trong Final Answer phải xuất hiện nguyên văn trong một Observation, nếu không phải bị loại hoặc trả fallback.
* Validation điểm và tính tổ hợp phải nằm ở backend deterministic trước LLM. Không nên giao các phép kiểm `[-5, 45, 0, thiếu môn, tổng mâu thuẫn]` cho prompt tự xử lý.
* Đã kiểm toán đầy đủ tool selection, Observation và termination cho bốn case TC03/TC04/TC14/TC16. Bảng 24 case vẫn dựa trên Final Answer của lần chạy trước, nên lần nghiệm thu tiếp theo nên xuất structured trace cho toàn bộ bộ test.

> **Kết luận:** ReAct Agent hiện tốt hơn Baseline về khả năng grounding và từ chối khi thiếu dữ liệu, nhưng chưa đạt yêu cầu nghiệp vụ của bộ test. Nguyên nhân kết hợp giữa toolset không khớp, thiếu backend validation/state, giới hạn 3 bước và model vẫn có thể bóp méo Observation khi tổng hợp Final Answer.
