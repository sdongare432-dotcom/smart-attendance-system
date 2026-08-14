import cv2
import os
import sys


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# =========================================================
# STUDENT ID
# =========================================================

student_id = input(
    "Enter Student ID: "
).strip()


if not student_id:

    print()
    print("ERROR: Student ID is required.")
    print()

    sys.exit()


# =========================================================
# DATASET FOLDER
# =========================================================

dataset_path = os.path.join(
    BASE_DIR,
    "attendance",
    "dataset"
)


os.makedirs(
    dataset_path,
    exist_ok=True
)


# =========================================================
# HAAR CASCADE
# =========================================================

cascade_path = os.path.join(
    BASE_DIR,
    "attendance",
    "haarcascade",
    "haarcascade_frontalface_default.xml"
)


if not os.path.exists(cascade_path):

    print()
    print("======================================")
    print("ERROR: Haar Cascade file not found!")
    print("======================================")
    print()

    print("Expected location:")
    print(cascade_path)

    print()

    sys.exit()


face_detector = cv2.CascadeClassifier(
    cascade_path
)


if face_detector.empty():

    print()
    print("ERROR: Could not load Haar Cascade.")
    print()

    sys.exit()


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print()
    print("======================================")
    print("ERROR: Camera could not be opened!")
    print("======================================")
    print()

    sys.exit()


# =========================================================
# SETTINGS
# =========================================================

TOTAL_IMAGES = 50

count = 0


# =========================================================
# START MESSAGE
# =========================================================

print()
print("======================================")
print("       SMART ATTENDANCE SYSTEM")
print("          FACE REGISTRATION")
print("======================================")
print()

print(
    "Student ID:",
    student_id
)

print()

print(
    "Camera started..."
)

print(
    "Look directly at the camera."
)

print(
    "Slowly move your face left, right,")
print(
    "up and down."
)

print()

print(
    f"Collecting {TOTAL_IMAGES} face images..."
)

print()

print(
    "Press Q to stop."
)

print()


# =========================================================
# CAMERA LOOP
# =========================================================

while True:

    ret, frame = camera.read()


    # -----------------------------------------------------
    # CAMERA FRAME CHECK
    # -----------------------------------------------------

    if not ret:

        print(
            "ERROR: Camera frame not received!"
        )

        break


    # -----------------------------------------------------
    # GRAYSCALE
    # -----------------------------------------------------

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # -----------------------------------------------------
    # FACE DETECTION
    # -----------------------------------------------------

    faces = face_detector.detectMultiScale(

        gray,

        scaleFactor=1.2,

        minNeighbors=5,

        minSize=(80, 80)

    )


    # -----------------------------------------------------
    # PROCESS DETECTED FACES
    # -----------------------------------------------------

    for (x, y, w, h) in faces:


        # -----------------------------------------------
        # STOP AFTER 50 IMAGES
        # -----------------------------------------------

        if count >= TOTAL_IMAGES:

            break


        count += 1


        # -----------------------------------------------
        # FILE NAME
        # -----------------------------------------------

        filename = os.path.join(

            dataset_path,

            f"User.{student_id}.{count}.jpg"

        )


        # -----------------------------------------------
        # SAVE FACE IMAGE
        # -----------------------------------------------

        face_image = gray[
            y:y + h,
            x:x + w
        ]


        cv2.imwrite(

            filename,

            face_image

        )


        # -----------------------------------------------
        # FACE BOX
        # -----------------------------------------------

        cv2.rectangle(

            frame,

            (x, y),

            (x + w, y + h),

            (0, 255, 0),

            2

        )


        # -----------------------------------------------
        # IMAGE COUNT
        # -----------------------------------------------

        cv2.putText(

            frame,

            f"Images: {count}/{TOTAL_IMAGES}",

            (x, y - 10),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 0),

            2

        )


    # =====================================================
    # DISPLAY CAMERA
    # =====================================================

    cv2.imshow(

        "Smart Attendance - Face Registration",

        frame

    )


    # =====================================================
    # QUIT
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


    # =====================================================
    # COMPLETED
    # =====================================================

    if count >= TOTAL_IMAGES:

       
