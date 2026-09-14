# Báo cáo — Ngày 2: phát hiện vật thể

**Họ và tên:** Kiều Quốc Hiếu<br>
**MSSV:** 2A202602186<br>
**Hình thức:** cá nhân<br>
**Mã cặp:** `SOLO`

## 1. Bài độc lập và nguồn dữ liệu

- Mã SHA-256 của ZIP ảnh được cấp: `f7d99888f21440fb0374d84962b93213bd8c14e665d093cc8d37f4c61b71ed33`
- Bốn mã ảnh: `drive_008.jpg`, `drive_022.jpg`, `drive_033.jpg`, `drive_038.jpg`
- Số vật thể thực tế: `79`
- Mã SHA-256 của gói YOLO của bạn: `1e8ecb3acf0ed34700b49da1ca9fbfdaa2d1a3bdece4bdee9d5ca5f09d15c500`
- Mã SHA-256 của gói CVAT gốc của bạn: `8c9f57f967d455cf8de866218c1cc6dd9cc8cd2aef8c5d934f1334f6c390da6e`
- Nguồn đối chiếu: bạn cùng cặp hoặc bộ tham chiếu do người hướng dẫn thực hành cấp: `Bộ tham chiếu do người hướng dẫn cấp`
- Mã SHA-256 của gói đối chiếu: `c8bbc767d8bb9a29f4ca5abf0c3516e5c2af94c58143a980b0148cfe0b500d2b`
- Nếu làm cá nhân, ghi mã lần phát và thời điểm nhận bộ tham chiếu: `(Bạn điền mã lần phát của bạn)`

Giải thích vì sao bài của bạn vẫn độc lập trước khi đối chiếu:
Tôi đã tự gán nhãn 4 ảnh dựa vào phiếu quy tắc (guideline), xuất đủ 2 định dạng CVAT và YOLO rồi kiểm tra chéo (audit) thành công trước khi nhận bộ tham chiếu để so sánh. Việc so sánh chỉ diễn ra ở bước cuối cùng (bước 5) sau khi đã chốt phiên bản làm việc.

## 2. Quyết định phân lớp

| Ảnh/vật thể | Lớp | Dấu hiệu nhìn thấy | Quy tắc áp dụng |
| --- | --- | --- | --- |
| `drive_022.jpg` (box giữa) | `car` | Xe con 4 chỗ, sedan | `sedan, hatchback, SUV...` -> `car` |
| `drive_022.jpg` (box to bên trái) | `bus` | Xe khách dài, nhiều cửa sổ | `thân xe khách dài, nhiều cửa sổ` -> `bus` |

Nêu một ví dụ cho thấy lớp và thuộc tính là hai loại thông tin khác nhau:
Lớp là định danh phương tiện (ví dụ `car` hoặc `truck`), trong khi thuộc tính (như `visibility` hay `boundary`) miêu tả trạng thái của phương tiện đó trong ảnh cụ thể (như bị che khuất `occluded` hay nằm trọn trong ảnh `inside`). Một chiếc `car` có thể ở trạng thái `occluded` hoặc `clear` tùy góc nhìn, bản chất nó vẫn là `car`.

## 3. Tự kiểm tra và sửa nhãn

| Trước khi sửa | Loại lỗi | Cách phát hiện | Sau khi sửa và quy tắc |
| --- | --- | --- | --- |
| Gán sai schema thứ tự lớp | lớp | Dùng script audit báo lỗi schema sai (nhầm vị trí bus và truck) | Chạy script đổi thứ tự schema về chuẩn `car, truck, bus, van` và remap ID |
| Lệch số lượng hộp YOLO và CVAT | hình học | Audit báo YOLO=5, CVAT=4 ở `drive_022` | Đồng bộ hóa lại dữ liệu YOLO dựa trên tọa độ chuẩn xác xuất từ CVAT để khớp trạng thái |

- Số hộp `needs_review` trước và sau khi kiểm: Trước: `5`, Sau: `0`
- Một quyết định chưa đủ bằng chứng và cách bạn xin hỗ trợ: Khi thấy một góc đuôi xe quá mờ, không thể phân biệt là SUV (car) hay xe van nhỏ (van), tôi đã đánh dấu `needs_review` và hỏi TA để phân xử.

## 4. Một dòng nhãn YOLO

- Dòng `class x_center y_center width height`: `2 0.397008 0.730070 0.475266 0.371109`
- Tên lớp và tọa độ điểm ảnh `xyxy`: Lớp `bus` (vì class_id=2). Tọa độ chuẩn hóa quy đổi ngược ra pixel với ảnh 640x640: `xtl ≈ 102`, `ytl ≈ 348`, `xbr ≈ 406`, `ybr ≈ 586`.
- Vì sao dòng đúng định dạng vẫn có thể sai lớp, phạm vi hoặc hình học?
Vì YOLO chỉ lưu class ID (chữ số) và tọa độ hình học thuần túy. Nó không quan tâm số 2 là `bus` hay `truck` (phụ thuộc vào `data.yaml`). Ngoài ra, nếu người gán nhãn vẽ hộp quá to (sai hình học), format của dãy số vẫn đúng tiêu chuẩn số thực của YOLO, YOLO không tự biết là hộp có sát mép vật thể hay không.

## 5. Huấn luyện và dự đoán thử

- Ba mã ảnh huấn luyện: `drive_022`, `drive_033`, `drive_038`
- Mã ảnh thẩm định: `drive_008`
- Mô tả một dự đoán trong `detect_result.jpg`: Mô hình dự đoán được một chiếc `car` với độ tự tin (confidence) là `0.85`
- Dự đoán đó gợi ý cần kiểm lại quy tắc hoặc dữ liệu nào?: Nếu dự đoán sai lớp hoặc vẽ hộp quá rộng, có thể cần kiểm tra lại độ chính xác của nhãn huấn luyện (ground truth).
- Minh chứng nào có thể bác bỏ nhận định của bạn?: Nếu ảnh kiểm tra chứa các loại xe có hình dáng đặc thù chưa từng xuất hiện trong tập huấn luyện (chỉ có 3 ảnh), mô hình đoán sai là do thiếu dữ liệu đa dạng chứ không hẳn do nhãn sai.
- Vì sao kết quả trên bốn ảnh không phải phép đánh giá mô hình dùng thực tế?: Tập dữ liệu 4 ảnh là quá nhỏ để mô hình học được tính khái quát hóa (generalization). Đây chỉ là bước "sanity check" để đảm bảo pipeline dữ liệu không bị lỗi kỹ thuật, chứ chưa đủ để đánh giá độ chính xác thực tế.

## 6. Đối chiếu nhãn

- Số hộp ghép được: `48`
- IoU trung bình và trung vị: trung bình `0.871828`, trung vị `0.89358`
- Mức đồng thuận lớp: `0.729167` (~72.9%)
- Số hộp phía bạn không ghép được: `30`
- Số hộp phía đối chiếu không ghép được: `2`
- Một điểm khác biệt cụ thể: Số hộp của tôi dư ra khá nhiều (30 hộp) so với bộ tham chiếu, có thể tôi đã gán nhãn cả những vật thể quá mờ hoặc quá xa mà phiếu quy tắc (guideline) bộ tham chiếu yêu cầu bỏ qua.
- Quy tắc hoặc hành động sửa phát sinh: Cần đọc lại quy tắc "Vật thể quá nhỏ hoặc mờ đến mức không thể phân lớp có căn cứ: không đoán". Sẽ xóa bớt các box gán những xe không rõ ràng.
- Vì sao mức đồng thuận cao không chứng minh mọi nhãn đều đúng?
Vì có thể cả hai người (bạn và đối chiếu) cùng mắc một lỗi hệ thống giống nhau (ví dụ: cùng bỏ sót một chiếc xe mờ ở góc, hoặc cùng hiểu sai một quy tắc ranh giới).

## 7. Kiểm tra kho GitHub cá nhân

- [x] Có phiếu quy tắc với ba tình huống mơ hồ.
- [x] Có kết quả kiểm hai gói xuất.
- [x] Có thông tin lần huấn luyện và ảnh dự đoán.
- [x] Có tóm tắt, bảng và ảnh phủ của bước đối chiếu.
- [x] Không có gói xuất thô, bộ nhãn tham chiếu hoặc trọng số mô hình.
- [x] Không có dữ liệu VinFast/khách hàng/ảnh cá nhân/mật khẩu/mã truy cập.

Minh chứng mạnh nhất trong bài và câu hỏi còn lại cho Lab Coach:
Minh chứng: Các gói export đã được đồng bộ hóa hoàn toàn (YOLO và CVAT khớp nhau 100% hình học và class). Khắc phục thành công lỗi schema nhầm ID.
Câu hỏi: Trong trường hợp một xe tải bị che đi phần thùng xe, chỉ còn hở mỗi cabin giống như xe van, quy tắc có bắt buộc phải dùng ngữ cảnh xung quanh để suy luận không hay chỉ gán theo những gì nhìn thấy?
