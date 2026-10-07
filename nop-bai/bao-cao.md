# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

| | |
|---|---|
| Họ và tên | ___ |
| MSSV | ___ |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/___/___ |
| Ngày nộp | ___ |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

<!-- Khoảng 120 - 150 từ. Điền kết quả thật từ MLflow UI ở Bước 1, tối thiểu 3 lần chạy. -->

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ tham số này đạt giá trị F1 cao nhất (0.7149), vượt qua ngưỡng tối thiểu (0.65). Lần chạy có accuracy cao nhất là lần 1 (0.8780) nhưng F1 lại thấp hơn, cho thấy accuracy có thể gây hiểu nhầm đối với dữ liệu mất cân bằng. Quan sát thấy khi giảm learning_rate thì f1 giảm đáng kể, và tăng số cây cùng với độ sâu cây đã giúp tăng năng lực mô hình để dự đoán các trường hợp khó (thu nhập > 50K).

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

<!-- Khoảng 120 - 150 từ. -->

Tập dữ liệu Adult có phân bố cực kỳ mất cân bằng, chỉ có 24.8% số người có thu nhập trên 50K (lớp dương). Điều này dẫn đến việc nếu mô hình học được rất ít mà luôn đoán "thu nhập thấp" cho tất cả các mẫu, độ chính xác (accuracy) vẫn có thể đạt tới mức 75.2%. Do đó, con số accuracy này không phản ánh khả năng phân loại chính xác các trường hợp quan trọng, và khiến chúng ta lầm tưởng là mô hình hoạt động tốt.

Ngược lại, F1-score của lớp dương (tính từ precision và recall của việc dự đoán lớp thu nhập > 50K) thể hiện trực tiếp khả năng của mô hình trong việc bắt đúng các trường hợp thiểu số mà không dự đoán sai quá nhiều. Chúng ta chỉ lấy f1 cho lớp dương (không dùng `average="weighted"` hay `"macro"`) để đảm bảo không bị lớp đa số làm lu mờ. Đây là lý do F1-score là thước đo chất lượng phù hợp và đáng tin cậy nhất cho bài toán này.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___
