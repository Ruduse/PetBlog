import os
import shutil
from sklearn.model_selection import train_test_split

# Đường dẫn dữ liệu gốc
image_dir = "images/"
label_dir = "labels/"

# Tạo thư mục output
for split in ["train", "val", "test"]:
    os.makedirs(f"dataset/images/{split}", exist_ok=True)
    os.makedirs(f"dataset/labels/{split}", exist_ok=True)

# Lấy danh sách file ảnh
images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
labels = [f.replace(".jpg", ".txt") for f in images]

# Chia tập dữ liệu
train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)
val_images, test_images = train_test_split(val_images, test_size=0.5, random_state=42)

# Copy dữ liệu
def move_files(images, split):
    for image in images:
        shutil.copy(image_dir + image, f"dataset/images/{split}/{image}")
        shutil.copy(label_dir + image.replace(".jpg", ".txt"), f"dataset/labels/{split}/{image.replace('.jpg', '.txt')}")

move_files(train_images, "train")
move_files(val_images, "val")
move_files(test_images, "test")
