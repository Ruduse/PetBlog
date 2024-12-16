from ultralytics import YOLO
import cv2
import cvzone
import math
import time

# Khởi tạo webcam và mô hình YOLO
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Đặt chiều rộng thấp hơn để giảm tải
cap.set(4, 480)  # Đặt chiều cao thấp hơn để giảm tải

# Tải mô hình YOLO đã huấn luyện
model = YOLO("C:/Users/rimdang/Project/PetBlog/runs/detect/train/weights/last.pt")  # Đường dẫn tới mô hình huấn luyện

# Danh sách các lớp đối tượng (tùy chỉnh theo mô hình của bạn)
classNames = ['Cat', 'Dog', 'Chicken', 'Elephant', 'Human', 'Horse']

fps_limit = 15  # Giới hạn FPS để tiết kiệm tài nguyên
prev_frame_time = 0
is_running = True

while True:
    new_frame_time = time.time()
    # Kiểm tra xem thời gian từ frame trước có đủ để đạt FPS limit
    if (new_frame_time - prev_frame_time) < (1 / fps_limit):
        continue

    if is_running:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break

        # Dự đoán và nhận diện đối tượng
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Lấy toạ độ của Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))

                # Hiển thị độ tin cậy (confidence) và tên lớp đối tượng
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

        # Tính toán và hiển thị FPS
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Hiển thị kết quả
        cv2.imshow("Real-time Detection", img)

    # Phím điều khiển: 'q' để thoát, 's' để dừng, và 'r' để tiếp tục
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # 'q' để thoát
        break
    elif key == ord('s'):  # 's' để dừng
        is_running = False
    elif key == ord('r'):  # 'r' để tiếp tục
        is_running = True

# Giải phóng webcam và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
