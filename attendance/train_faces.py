import cv2
import os
import numpy as np
from PIL import Image

# Paths
dataset_path = "attendance/dataset"
trainer_path = "attendance/trainer"

# Trainer folder तयार करा
os.makedirs(trainer_path, exist_ok=True)

# Face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier(
    "attendance/haarcascade/haarcascade_frontalface_default.xml"
)

face_samples = []
ids = []

# Dataset मधील images
image_paths = [
    os.path.join(dataset_path, file)
    for file in os.listdir(dataset_path)
]

print("Training started...")

for image_path in image_paths:

    # Image grayscale मध्ये convert
    pil_image = Image.open(image_path).convert("L")
    image_numpy = np.array(pil_image, "uint8")

    # Filename मधून Student ID घेणे
    filename = os.path.split(image_path)[-1]
    student_id = int(filename.split(".")[1])

    # Face detect
    faces = detector.detectMultiScale(image_numpy)

    for (x, y, w, h) in faces:

        face_samples.append(image_numpy[y:y+h, x:x+w])
        ids.append(student_id)

print(f"Images found: {len(face_samples)}")

if len(face_samples) == 0:
    print("No faces found in dataset.")
else:

    # Train model
    recognizer.train(face_samples, np.array(ids))

    # Model save
    recognizer.write(
        os.path.join(trainer_path, "trainer.yml")
    )

    print("Training completed successfully!")
    print("Model saved: attendance/trainer/trainer.yml")
