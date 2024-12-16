import argparse
import os
import time
import cv2
from flask import Flask, render_template, request, redirect, send_from_directory, Response
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

# Tải mô hình YOLOv8
model = YOLO('C:/Users/rimdang/Project/PetBlog/DV_nuoi/runs/detect/train6/weights/last.pt')

# Đường dẫn upload ảnh
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flag để kiểm tra webcam đã được kích hoạt hay chưa
webcam_started = False

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=["POST"])
def predict_img():
    if 'file' in request.files:
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(filepath)

        # Kiểm tra định dạng tệp
        file_extension = f.filename.rsplit('.', 1)[1].lower()

        if file_extension in ['jpg', 'png']:
            img = cv2.imread(filepath)
            results = model(img)
            res_plotted = results[0].plot()
            return display(res_plotted)

        elif file_extension == 'mp4':
            video_path = filepath
            cap = cv2.VideoCapture(video_path)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                results = model(frame)
                res_plotted = results[0].plot()
                out.write(res_plotted)

            return send_from_directory('.', 'output.mp4')

    return render_template('index.html')


@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = os.path.join(folder_path, latest_subfolder)
    files = os.listdir(directory)
    latest_file = files[0]
    filename = os.path.join(directory, latest_file)

    file_extension = filename.rsplit('.', 1)[1].lower()
    if file_extension in ['jpg', 'png']:
        return send_from_directory(directory, latest_file)

    return "Invalid file format"


# def get_frame():
#     global webcam_started
#     cap = cv2.VideoCapture(0)
    
#     if not cap.isOpened():
#         return None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         if webcam_started:
#             # Phát hiện đối tượng chỉ khi webcam đã được kích hoạt
#             results = model(frame)
#             res_plotted = results[0].plot()
#             ret, jpeg = cv2.imencode('.jpg', res_plotted)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
#         else:
#             # Hiển thị webcam mà không phát hiện đối tượng
#             ret, jpeg = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

#         time.sleep(0.1)

def get_frame():
    global webcam_started
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Kiểm tra phím bấm 'q' để dừng hoặc 'S' để bắt đầu
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):  # Phím "q" để dừng webcam
            webcam_started = False
            break

        if key == ord('s'):  # Phím "S" để bắt đầu phát hiện
            webcam_started = True

        if webcam_started:
            # Phát hiện đối tượng khi webcam bắt đầu
            results = model(frame)
            res_plotted = results[0].plot()
            ret, jpeg = cv2.imencode('.jpg', res_plotted)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            # Hiển thị webcam mà không phát hiện đối tượng
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        time.sleep(0.1)

    cap.release()  # Đóng webcam khi dừng


@app.route("/video_feed")
def video_feed():
    # Đảm bảo webcam chỉ bắt đầu khi người dùng kích hoạt
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/start_webcam", methods=["POST"])
def start_webcam():
    global webcam_started
    webcam_started = True  # Bắt đầu phát hiện đối tượng khi nhấn nút
    return redirect('/video_feed')


# @app.route("/stop_webcam", methods=["POST"])
# def stop_webcam():
#     global webcam_started
#     webcam_started = False  # Dừng phát hiện đối tượng
#     return redirect('/video_feed')
@app.route("/stop_webcam", methods=["POST"])
def stop_webcam():
    global webcam_started
    webcam_started = False  # Dừng phát hiện đối tượng
    return render_template('index.html')  # Quay lại trang index.html


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov8 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)
