# from ultralytics import YOLO
# import cv2
 
# model = YOLO('../Yolo-Weights/yolov8l.pt')
# # model = YOLO('../Yolo-Weights/yolov8l.l')
# # có những sự khác nhau giữa duôi .
# results = model("Yolo_ObjectDetection\images\download.png", show=True)
# cv2.waitKey(0)

from ultralytics import YOLO
import cv2
import tkinter as tk
from tkinter import filedialog

# Tạo một cửa sổ Tkinter
root = tk.Tk()
root.title("YOLO Object Detection")
root.geometry("900x900")

# Tải mô hình YOLO
model = YOLO('../Yolo-Weights/yolov8n.pt')

def choose_file():
    # Mở hộp thoại chọn tệp
    file_path = filedialog.askopenfilename(
        title="Choose an image file",
        filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*"))
    )
    
    if file_path:
        # Nhận diện đối tượng trên hình ảnh được chọn
        results = model(file_path, show=True)
        # Nếu bạn muốn giữ cửa sổ mở cho đến khi người dùng nhấn phím
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Tạo nút "Chọn Tệp" và gán hàm `choose_file` cho nó
btn_choose_file = tk.Button(root, text="Choose Image File", command=choose_file)
btn_choose_file.pack(pady=20)

# Bắt đầu vòng lặp chính của Tkinter
root.mainloop()
