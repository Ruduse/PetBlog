import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from filterpy.kalman import KalmanFilter

# Khởi tạo video
cap = cv2.VideoCapture("C:/Users/rimdang/Project/PetBlog/Videos/cars.mp4")  # Đường dẫn video

# Khởi tạo mô hình YOLO
model = YOLO("../Yolo-Weights/yolov8l.pt")

# Danh sách tên lớp
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# Đọc mask và kiểm tra lỗi
# Đọc mask và kiểm tra lỗi
mask = cv2.imread("C:/Users/rimdang/Project/PetBlog/images/mask.png")
if mask is None:
    print(f"Không thể đọc tệp mask: images/mask.png. Kiểm tra đường dẫn.")
else:
    # Kiểm tra kích thước của mask và thay đổi kích thước nếu cần
    success, img = cap.read()
    if not success:
        print("Không thể đọc video.")
        break
    mask = cv2.resize(mask, (img.shape[1], img.shape[0]))  # Thay đổi kích thước của mask

    imgRegion = cv2.bitwise_and(img, mask)


# Khởi tạo bộ theo dõi (Kalman Filter)
class KalmanTracker:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.x = np.zeros((7, 1))  # State vector
        self.kf.P *= 1000.  # Uncertainty
        self.kf.F = np.eye(7)  # State transition matrix
        self.kf.H = np.eye(4, 7)  # Measurement matrix
        self.kf.R *= 10  # Measurement uncertainty
        self.kf.Q = np.eye(7)  # Process uncertainty

    def update(self, detection):
        self.kf.predict()
        self.kf.update(detection)

    def get_position(self):
        return self.kf.x[:4].flatten()

# Khởi tạo danh sách theo dõi
trackers = []
limits = [400, 297, 673, 297]
totalCount = []

while True:
    success, img = cap.read()
    if not success:
        print("Không thể đọc video.")
        break
    # test
    mask = cv2.resize(mask, (img.shape[1], img.shape[0]))  # Thay đổi kích thước của mask
    # 
    imgRegion = cv2.bitwise_and(img, mask)

    imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED)
    if imgGraphics is not None:
        img = cvzone.overlayPNG(img, imgGraphics, (0, 0))

    results = model(imgRegion, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0].int()
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass in ["car", "truck", "bus", "motorbike"] and conf > 0.3:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    # Cập nhật vị trí đối tượng
    for detection in detections:
        tracker = KalmanTracker()
        tracker.update(detection[:4])
        trackers.append(tracker)

    # Vẽ đường giới hạn
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
    
    for tracker in trackers:
        position = tracker.get_position()
        x1, y1, x2, y2 = int(position[0]), int(position[1]), int(position[2]), int(position[3])
        
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cvzone.putTextRect(img, f'ID: {trackers.index(tracker)}', (max(0, x1), max(35, y1)),
                           scale=2, thickness=3, offset=10)

        cx, cy = x1 + w // 2, y1 + h // 2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
            if trackers.index(tracker) not in totalCount:
                totalCount.append(trackers.index(tracker))
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

    cv2.putText(img, str(len(totalCount)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
