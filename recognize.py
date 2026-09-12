import cv2
import csv
import os
import sys


# ==========================================
# 1. GET PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==========================================
# 2. LOAD STUDENT INFORMATION FROM CSV
# ==========================================

students = {}

students_file = os.path.join(
    BASE_DIR,
    "data",
    "students.csv"
)

try:

    with open(
        students_file,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            student_id = int(row["ID"])

            students[student_id] = {
                "name": row["Name"],
                "enrollment": row["Enrollment No"],
                "email": row["Email"]
            }

except FileNotFoundError:

    print("❌ students.csv not found.")
    sys.exit()


# ==========================================
# 3. RECOGNITION THRESHOLD
# ==========================================

# Lower LBPH distance = better match
THRESHOLD = 82


# ==========================================
# 4. LOAD HAAR CASCADE
# ==========================================

cascade_file = os.path.join(
    BASE_DIR,
    "haarcascade_frontalface_default.xml"
)

face_detector = cv2.CascadeClassifier(
    cascade_file
)

if face_detector.empty():

    print("❌ Haar Cascade could not be loaded.")
    sys.exit()


# ==========================================
# 5. LOAD TRAINED LBPH MODEL
# ==========================================

model_file = os.path.join(
    BASE_DIR,
    "trainer",
    "trainingData.yml"
)

if not os.path.exists(model_file):

    print("❌ Trained face model not found.")
    print("Please run train.py first.")
    sys.exit()


recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    model_file
)


# ==========================================
# 6. START WEBCAM
# ==========================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("❌ Could not open webcam.")
    sys.exit()


print("📷 Recognition started!")
print("Look at the camera.")
print("Press Q to stop.")


# ==========================================
# 7. MAIN RECOGNITION LOOP
# ==========================================

while True:

    ret, frame = camera.read()

    if not ret:

        print("❌ Could not read camera frame.")
        break


    # ======================================
    # STEP 1 — CONVERT TO GRAYSCALE
    # ======================================

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # ======================================
    # STEP 2 — HISTOGRAM EQUALIZATION
    # ======================================
    # Improves contrast and helps recognition
    # under different lighting conditions.

    equalized = cv2.equalizeHist(
        gray
    )


    # ======================================
    # STEP 3 — MEDIAN BLUR
    # ======================================
    # Reduces small image noise while
    # preserving important face features.

    processed = cv2.medianBlur(
        equalized,
        5
    )


    # ======================================
    # STEP 4 — DETECT FACES USING HAAR
    # ======================================

    faces = face_detector.detectMultiScale(
        processed,
        scaleFactor=1.3,
        minNeighbors=5
    )


    # ======================================
    # PROCESS EACH DETECTED FACE
    # ======================================

    for (x, y, w, h) in faces:


        # ==================================
        # GET PROCESSED FACE REGION
        # ==================================

        face_region = processed[
            y:y + h,
            x:x + w
        ]


        # ==================================
        # RESIZE FACE REGION
        # ==================================
        # Keeps the input size consistent.

        face_region = cv2.resize(
            face_region,
            (100, 100)
        )


        # ==================================
        # LBPH FACE RECOGNITION
        # ==================================

        student_id, confidence = recognizer.predict(
            face_region
        )


        # Print distance in CMD

        print(
            f"Detected ID: {student_id}, "
            f"Distance: {confidence:.2f}"
        )


        # ==================================
        # CHECK RECOGNITION THRESHOLD
        # ==================================

        if confidence <= THRESHOLD:

            student = students.get(
                student_id
            )


            if student is not None:

                name = student["name"]

                display_text = (
                    f"{name} | ID: {student_id}"
                )

            else:

                display_text = "Unknown Student"

        else:

            display_text = "Unknown Student"


        # ==================================
        # DRAW FACE RECTANGLE
        # ==================================

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )


        # ==================================
        # DISPLAY NAME / UNKNOWN
        # ==================================

        cv2.putText(
            frame,
            display_text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # ======================================
    # SHOW CAMERA WINDOW
    # ======================================

    cv2.imshow(
        "Face Recognition",
        frame
    )


    # ======================================
    # PRESS Q TO EXIT
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# 8. CLOSE EVERYTHING
# ==========================================

camera.release()

cv2.destroyAllWindows()

print("\n✅ Recognition stopped.")