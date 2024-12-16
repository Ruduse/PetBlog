import argparse
import os
import time
import cv2
from flask import Flask, render_template, request, redirect, send_from_directory, Response
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

# Tải mô hình YOLOv8
model = YOLO('C:/Users/rimdang/Project/PetBlog/Yolo-Weights/Yolo-Weights/yolov8n.pt')

# Đường dẫn upload ảnh
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/") 
def hello_world():
    return render_template('main.html')

@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath, app.config['UPLOAD_FOLDER'], f.filename)
            f.save(filepath)

            # Kiểm tra định dạng tệp
            file_extension = f.filename.rsplit('.', 1)[1].lower()

            if file_extension in ['jpg', 'png']:
                img = cv2.imread(filepath)
                results = model(img, save=True)
                return display(f.filename)

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
                    results = model(frame, save=True)
                    res_plotted = results[0].plot()
                    out.write(res_plotted)

                return video_feed()

    return render_template('main.html')

@app.route('/realtime_detection', methods=["POST"])
def realtime_detection():
    return redirect('/video_feed')

@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = folder_path + '/' + latest_subfolder
    files = os.listdir(directory)
    latest_file = files[0]
    filename = os.path.join(folder_path, latest_subfolder, latest_file)

    file_extension = filename.rsplit('.', 1)[1].lower()
    if file_extension in ['jpg', 'png']:
        return send_from_directory(directory, latest_file)

    return "Invalid file format"

def get_frame():
    cap = cv2.VideoCapture(0)  # Sử dụng webcam của máy tính
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        res_plotted = results[0].plot()
        ret, jpeg = cv2.imencode('.jpg', res_plotted)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        time.sleep(0.1)

@app.route("/video_feed")
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov8 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)
