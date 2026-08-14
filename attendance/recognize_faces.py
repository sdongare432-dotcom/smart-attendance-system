import os
import sys
import cv2
import django
import urllib.request


# =========================================================
# DJANGO SETUP
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "smart_attendance.settings"
)

django.setup()


# =========================================================
# DJANGO MODELS
# =========================================================

from attendance.models import Student, Attendance
from django.utils import timezone


# =========================================================
# HAAR CASCADE FILE
# =========================================================

CASCADE_DIR = os.path.join(
    BASE_DIR,
    "attendance",
    "haarcascade"
)

CASCADE_PATH = os.path.join(
    CASCADE_DIR,
    "haarcascade_frontalface_default.xml"
)


# =========================================================
# CREATE HAAR CASCADE FOLDER
# =========================================================

if not os.path.exists(CASCADE_DIR):

    os.makedirs(CASCADE_DIR)


# =========================================================
# DOWNLOAD HAAR CASCADE IF NOT FOUND
# =========================================================

if not os.path.exists(CASCADE_PATH):

    print()
    print("======================================")
    print("Haar Cascade file not found.")
    print("Downloading Haar Cascade...")
    print("======================================")
    print()

    HAAR_URL = (
        "https://raw.githubusercontent.com/"
        "opencv/opencv/master/data/haarcascades/"
        "haarcascade_frontalface_default.xml"
    )

    try:

        urllib.request.urlretrieve(
            HAAR_URL,
            CASCADE_PATH
        )

        print(
            "Haar Cascade downloaded successfully!"
        )

        print(
            "Saved at:"
        )

        print(
            CASCADE_PATH
        )

        print()

    except Exception as e:

        print()
        print("======================================")
        print("ERROR: Could not download Haar Cascade")
        print("======================================")
        print()

        print(e)

        print()

        print(
            "Please check your internet connection."
        )

        print()

        sys.exit()


# =========================================================
# VERIFY HAAR CASCADE
# =========================================================

face_detector = cv2.CascadeClassifier(
    CASCADE_PATH
)


if face_detector.empty():

    print()
    print("======================================")
    print("ERROR: Haar Cascade could not be loaded!")
    print("======================================")
    print()

    print(
        "File:"
    )

    print(
        CASCADE_PATH
    )

    print()

    sys.exit()


# =========================================================
# TRAINER PATH
# =========================================================

TRAINER_PATH = os.path.join(
    BASE_DIR,
    "attendance",
    "trainer",
    "trainer.yml"
)


# =========================================================
# CHECK TRAINER
# =========================================================

if not os.path.exists(TRAINER_PATH):

    print()
    print("======================================")
    print("ERROR: trainer.yml not found!")
    print("======================================")
    print()

    print(
        "Expected location:"
    )

    print(
        TRAINER_PATH
    )

    print()

    print(
        "Please train the registered faces first."
    )

    print()

    sys.exit()


# =========================================================
# FACE RECOGNIZER
# =========================================================

try:

    recognizer = cv2.face.LBPHFaceRecognizer_create()

except AttributeError:

    print()
    print("======================================")
    print("ERROR: cv2.face is not available!")
    print("======================================")
    print()

    print(
        "Install opencv-contrib-python:"
    )

    print()

    print(
        "pip install opencv-contrib-python"
    )

    print()

    sys.exit()


# =========================================================
# LOAD TRAINER
# =========================================================

try:

    recognizer.read(
        TRAINER_PATH
    )

except Exception as e:

    print()
    print("======================================")
    print("ERROR: Could not load trainer.yml")
    print("======================================")
    print()

    print(e)

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

MAX_DISTANCE = 60

REQUIRED_FRAMES = 5


# =========================================================
# VARIABLES
# =========================================================

recognized_id = None

recognized_frames = 0

session_marked_students = set()


# =========================================================
# MARK ATTENDANCE
# =========================================================

def mark_attendance(student):

    today = timezone.localdate()

    current_time = timezone.localtime().time()


    # -----------------------------------------------------
    # Check today's attendance
    # -----------------------------------------------------

    already_marked = Attendance.objects.filter(

        student=student,

        date=today

    ).exists()


    if already_marked:

        print(
            "Already marked today:",
            student.name
        )

        return False


    # -----------------------------------------------------
    # Create attendance
    # -----------------------------------------------------

    Attendance.objects.create(

        student=student,

        date=today,

        time=current_time,

        status="Present"

    )


    print()
    print("======================================")
    print("       ATTENDANCE MARKED")
    print("======================================")

    print(
        "Student :",
        student.name
    )

    print(
        "Roll No :",
        student.roll_no
    )

    print(
        "Date    :",
        today
    )

    print(
        "Time    :",
        current_time
    )

    print("======================================")
    print()

    return True


# =========================================================
# START MESSAGE
# =========================================================

print()
print("======================================")
print("      SMART ATTENDANCE SYSTEM")
print("        FACE RECOGNITION")
print("======================================")
print()

print(
    "Camera started..."
)

print()

print(
    "Show registered student face."
)

print()

print(
    "Unknown faces will NOT be marked."
)

print()

print(
    "Press Q to quit."
)

print()


# =========================================================
# MAIN CAMERA LOOP
# =========================================================

while True:


    # -----------------------------------------------------
    # Read camera
    # -----------------------------------------------------

    ret, frame = camera.read()


    if not ret:

        print(
            "ERROR: Could not read camera."
        )

        break


    # -----------------------------------------------------
    # Grayscale
    # -----------------------------------------------------

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # -----------------------------------------------------
    # Detect faces
    # -----------------------------------------------------

    faces = face_detector.detectMultiScale(

        gray,

        scaleFactor=1.2,

        minNeighbors=5,

        minSize=(100, 100)

    )


    # -----------------------------------------------------
    # No face
    # -----------------------------------------------------

    if len(faces) == 0:

        recognized_id = None

        recognized_frames = 0


    # =====================================================
    # PROCESS FACES
    # =====================================================

    for (x, y, w, h) in faces:


        # -------------------------------------------------
        # Predict student
        # -------------------------------------------------

        student_id, distance = recognizer.predict(

            gray[
                y:y + h,
                x:x + w
            ]

        )


        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        confidence = max(

            0,

            min(

                100,

                int(
                    100 - distance
                )

            )

        )


        print(
            "ID:",
            student_id,
            "| Distance:",
            round(distance, 2),
            "| Confidence:",
            confidence
        )


        # =================================================
        # RECOGNIZED STUDENT
        # =================================================

        if distance <= MAX_DISTANCE:

            try:

                student = Student.objects.get(
                    id=student_id
                )


                # -----------------------------------------
                # Continuous recognition
                # -----------------------------------------

                if recognized_id == student.id:

                    recognized_frames += 1

                else:

                    recognized_id = student.id

                    recognized_frames = 1


                # -----------------------------------------
                # GREEN BOX
                # -----------------------------------------

                cv2.rectangle(

                    frame,

                    (x, y),

                    (x + w, y + h),

                    (0, 255, 0),

                    2

                )


                # -----------------------------------------
                # NAME
                # -----------------------------------------

                cv2.putText(

                    frame,

                    student.name,

                    (x, y - 35),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (0, 255, 0),

                    2

                )


                # -----------------------------------------
                # CONFIDENCE
                # -----------------------------------------

                cv2.putText(

                    frame,

                    f"Confidence: {confidence}%",

                    (x, y - 10),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.6,

                    (0, 255, 255),

                    2

                )


                # -----------------------------------------
                # VERIFYING
                # -----------------------------------------

                cv2.putText(

                    frame,

                    f"Verifying: {recognized_frames}/{REQUIRED_FRAMES}",

                    (x, y + h + 25),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.6,

                    (255, 255, 0),

                    2

                )


                # =================================================
                # MARK ATTENDANCE
                # =================================================

                if recognized_frames >= REQUIRED_FRAMES:


                    if student.id not in session_marked_students:

                        mark_attendance(
                            student
                        )

                        session_marked_students.add(
                            student.id
                        )


            # =================================================
            # STUDENT NOT FOUND
            # =================================================

            except Student.DoesNotExist:

                recognized_id = None

                recognized_frames = 0


                cv2.rectangle(

                    frame,

                    (x, y),

                    (x + w, y + h),

                    (0, 0, 255),

                    2

                )


                cv2.putText(

                    frame,

                    "Student Not Found",

                    (x, y - 10),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.7,

                    (0, 0, 255),

                    2

                )


        # =================================================
        # UNKNOWN
        # =================================================

        else:

            recognized_id = None

            recognized_frames = 0


            # ---------------------------------------------
            # YELLOW BOX
            # ---------------------------------------------

            cv2.rectangle(

                frame,

                (x, y),

                (x + w, y + h),

                (0, 255, 255),

                2

            )


            # ---------------------------------------------
            # UNKNOWN TEXT
            # ---------------------------------------------

            cv2.putText(

                frame,

                "UNKNOWN",

                (x, y - 10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 255, 255),

                2

            )


            # ---------------------------------------------
            # CONFIDENCE
            # ---------------------------------------------

            cv2.putText(

                frame,

                f"Confidence: {confidence}%",

                (x, y + h + 25),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0, 255, 255),

                2

            )


    # =====================================================
    # SHOW CAMERA
    # =====================================================

    cv2.imshow(

        "Smart Attendance - Face Recognition",

        frame

    )


    # =====================================================
    # PRESS Q
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# =========================================================
# CLOSE CAMERA
# =========================================================

camera.release()

cv2.destroyAllWindows()


print()
print("======================================")
print("Camera closed.")
print("Face recognition stopped.")
print("======================================")
