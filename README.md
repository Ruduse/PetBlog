
Chuẩn bị dữ liệu
1.1. Cài đặt thư viện cần thiết
1.2. Tạo thư mục dữ liệu
1.3. Tạo tập dữ liệu giả lập
1.4. Chia tập train/test

Huấn luyện mô hình
2.1. File cấu hình data.yaml
2.2. Huấn luyện với YOLO

Kiểm tra mô hình
3.1. Đánh giá kết quả trên tập validation

Dự đoán hình ảnh mới
4.1. Tải mô hình đã huấn luyện
4.2. Hiển thị kết quả dự đoán

Xuất mô hình
5.1. Lưu mô hình dưới định dạng ONNX

Ghi chú và lời khuyên
6.1. Lưu ý khi làm việc với tập dữ liệu thực tế
6.2. Tinh chỉnh tham số huấn luyện

Các bước để hoàn thành project

1.Installation: tải các IDE,Python

2.Package Installations: tải các thư viện cần cho đồ án



lưu ý:Tạo môi truong ảo ,cài đặt numpy trước,rồi đến các thư viện khác, hạ cấp hoặc thăng cấp các thư 
3.Creat Project: tạo đồ án
Chuẩn bị dữ liệu
1.1. Cài đặt thư viện cần thiết
1.2. Tạo thư mục dữ liệu
1.3. Tạo tập dữ liệu giả lập
1.4. Chia tập train/test

Huấn luyện mô hình
2.1. File cấu hình data.yaml
2.2. Huấn luyện với YOLO

Kiểm tra mô hình
3.1. Đánh giá kết quả trên tập validation

Dự đoán hình ảnh mới
4.1. Tải mô hình đã huấn luyện
4.2. Hiển thị kết quả dự đoán

Xuất mô hình
5.1. Lưu mô hình dưới định dạng ONNX

Ghi chú và lời khuyên
6.1. Lưu ý khi làm việc với tập dữ liệu thực tế
6.2. Tinh chỉnh tham số huấn luyện

4.Các lệnh git
git init
git remote add origin https://github.com/Ruduse/PetBlog.git
git remote -v
git add .
git commit -m "Initial commit"  # Thay đổi thông điệp theo ý bạn
git push -u origin master  # Sử dụng "main" nếu branch chính của bạn là "main"






<!-- Thêm nút Start Webcam -->
<!-- <button id="start-webcam" class="btn btn-block btn-primary btn-sm">Start Webcam</button>
<video id="webcam-video" style="height:640px; width:640px;" autoplay></video>

<script>
  // Chạy webcam khi nhấn nút Start Webcam
  document.getElementById("start-webcam").addEventListener("click", function() {
    const videoElement = document.getElementById('webcam-video');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
          videoElement.srcObject = stream;
        })
        .catch(function(error) {
          console.error("Something went wrong with webcam access: ", error);
        });
    } else {
      alert("Webcam not supported.");
    }
  });
</script> -->

    <button id="start-webcam" class="btn btn-block btn-primary btn-sm">Start Webcam</button>
    <button id="pause-webcam" class="btn btn-block btn-warning btn-sm" disabled>Pause Webcam</button>
    <button id="stop-webcam" class="btn btn-block btn-danger btn-sm" disabled>Stop Webcam</button>
    <video id="webcam-video" style="height:640px; width:640px;" autoplay></video>
<script>
  // Chạy webcam khi nhấn nút Start Webcam
  let videoElement = document.getElementById('webcam-video');
let startButton = document.getElementById('start-webcam');
let pauseButton = document.getElementById('pause-webcam');
let stopButton = document.getElementById('stop-webcam');
let stream = null; // Để lưu trữ đối tượng MediaStream

// Chạy webcam khi nhấn nút Start Webcam
startButton.addEventListener("click", function() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(cameraStream) {
        stream = cameraStream;  // Lưu trữ stream vào biến
        videoElement.srcObject = cameraStream;

        // Kích hoạt nút Pause và Stop
        pauseButton.disabled = false;
        stopButton.disabled = false;
        startButton.disabled = true;
      })
      .catch(function(error) {
        console.error("Something went wrong with webcam access: ", error);
      });
  } else {
    alert("Webcam not supported.");
  }
});

// Tạm dừng webcam khi nhấn nút Pause Webcam
pauseButton.addEventListener("click", function() {
  if (stream) {
    let tracks = stream.getTracks();
    tracks.forEach(track => track.enabled = false);  // Tạm dừng video stream
    pauseButton.disabled = true;
  }
});

// Dừng webcam khi nhấn nút Stop Webcam
stopButton.addEventListener("click", function() {
  if (stream) {
    let tracks = stream.getTracks();
    tracks.forEach(track => track.stop());  // Dừng video stream
    videoElement.srcObject = null;

    // Khôi phục trạng thái các nút
    startButton.disabled = false;
    pauseButton.disabled = true;
    stopButton.disabled = true;
  }
});

</script>
index.html đã code từ trước
# import os
# import time
# import cv2
# from flask import Flask, render_template, request, redirect, Response, send_from_directory
# from werkzeug.utils import secure_filename
# from ultralytics import YOLO

# app = Flask(__name__)

# # Tải mô hình YOLOv8
# model = YOLO('C:/Users/rimdang/Project/PetBlog/Yolo-Weights/Yolo-Weights/yolov8n.pt')

# # Thư mục upload
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/")
# def index():
#     return render_template('index.html')

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if 'file' in request.files:
#         file = request.files['file']
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         file_extension = filename.rsplit('.', 1)[1].lower()

#         if file_extension in ['jpg', 'png']:
#             img = cv2.imread(filepath)
#             results = model(img)
#             results.save(save_dir="static/results")
#             detected_file = os.path.join("static/results", results.files[0])
#             return send_from_directory('static/results', os.path.basename(detected_file))

#         elif file_extension == 'mp4':
#             return process_video(filepath)

#     return redirect('/')

# def process_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter('static/results/output.mp4', fourcc, 30.0, (frame_width, frame_height))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model(frame)
#         res_plotted = results[0].plot()
#         out.write(res_plotted)

#     cap.release()
#     out.release()
#     return send_from_directory('static/results', 'output.mp4')

# def gen_frames():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model(frame)
#         res_plotted = results[0].plot()
#         _, buffer = cv2.imencode('.jpg', res_plotted)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# @app.route("/video_feed")
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
mainApp.py p1


<!-- Chọn tệp để upload -->
<!-- Thêm nút Start Webcam -->
<!-- <button id="start-webcam" class="btn btn-block btn-primary btn-sm">Start Webcam</button>
<video id="webcam-video" style="height:640px; width:640px;" autoplay></video>

<script>
  // Chạy webcam khi nhấn nút Start Webcam
  document.getElementById("start-webcam").addEventListener("click", function() {
    const videoElement = document.getElementById('webcam-video');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
          videoElement.srcObject = stream;
        })
        .catch(function(error) {
          console.error("Something went wrong with webcam access: ", error);
        });
    } else {
      alert("Webcam not supported.");
    }
  });
</script> -->


# import argparse
# import os
# import time
# import cv2
# from flask import Flask, render_template, request, redirect, send_from_directory, Response
# from werkzeug.utils import secure_filename
# from ultralytics import YOLO

# app = Flask(__name__)

# # Tải mô hình YOLOv8
# model = YOLO('C:/Users/rimdang/Project/PetBlog/DV_nuoi/runs/detect/train/weights/last.pt')

# # Đường dẫn upload ảnh
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route("/")
# def index():
#     return render_template('index.html')


# @app.route("/", methods=["GET", "POST"])
# def predict_img():
#     if request.method == "POST":
#         if 'file' in request.files:
#             f = request.files['file']
#             basepath = os.path.dirname(__file__)
#             filepath = os.path.join(basepath, app.config['UPLOAD_FOLDER'], f.filename)
#             f.save(filepath)

#             # Kiểm tra định dạng tệp
#             file_extension = f.filename.rsplit('.', 1)[1].lower()

#             if file_extension == 'jpg' or file_extension == 'png':
#                 img = cv2.imread(filepath)
#                 results = model(img, save=True)
#                 return display(f.filename)

#             elif file_extension == 'mp4':
#                 video_path = filepath
#                 cap = cv2.VideoCapture(video_path)
#                 frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#                 frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#                 fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#                 out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))

#                 while cap.isOpened():
#                     ret, frame = cap.read()
#                     if not ret:
#                         break
#                     results = model(frame, save=True)
#                     res_plotted = results[0].plot()
#                     out.write(res_plotted)

#                 return video_feed()

#     return render_template('index.html')

# # @app.route('/realtime_detection', methods=["POST"])
# # def realtime_detection():
# #     return redirect('/video_feed')

# @app.route('/<path:filename>')
# def display(filename):
#     folder_path = 'runs/detect'
#     subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
#     latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
#     directory = folder_path + '/' + latest_subfolder
#     files = os.listdir(directory)
#     latest_file = files[0]
#     filename = os.path.join(folder_path, latest_subfolder, latest_file)

#     file_extension = filename.rsplit('.', 1)[1].lower()
#     if file_extension == 'jpg' or file_extension == 'png':
#         return send_from_directory(directory, latest_file)

#     return "Invalid file format"


# def get_frame():
#     cap = cv2.VideoCapture(0)  # Sử dụng webcam của máy tính
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model(frame)
#         res_plotted = results[0].plot()
#         ret, jpeg = cv2.imencode('.jpg', res_plotted)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
#         time.sleep(0.1)

# @app.route("/video_feed")
# def video_feed():
#     return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route("/start_webcam", methods=["POST"])
# def start_webcam():
#     return redirect('/video_feed')

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Flask app exposing yolov8 models")
#     parser.add_argument("--port", default=5000, type=int, help="port number")
#     args = parser.parse_args()
#     app.run(host="0.0.0.0", port=args.port)