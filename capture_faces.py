import cv2
import os
import sys


# Get Student ID from command line
if len(sys.argv) < 2:
    print("❌ Student ID not provided.")
    exit()

student_id = sys.argv[1]

dataset_folder = os.path.join("dataset", student_id)
os.makedirs(dataset_folder, exist_ok=True)


# Load Haar Cascade
face_detector = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open webcam.")
    exit()


print("📷 Camera started!")
print(f"Capturing faces for Student ID: {student_id}")
print("Look at the camera.")

count = 0

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Could not read camera frame.")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        count += 1

        face = gray[y:y + h, x:x + w]

        face = cv2.resize(
            face,
            (100, 100)
        )

        filename = os.path.join(
            dataset_folder,
            f"{count}.jpg"
        )

        cv2.imwrite(
            filename,
            face
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Images: {count}/30",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Face Capture",
        frame
    )

    # Stop after 30 images
    if count >= 30:
        break

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()


if count >= 30:
    print("\n✅ 30 face images captured successfully!")
else:
    print(f"\n⚠️ Capture stopped. Images captured: {count}")

print("================================")