import cv2
import os
import numpy as np


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)

TRAINER_FOLDER = os.path.join(
    BASE_DIR,
    "trainer"
)

MODEL_FILE = os.path.join(
    TRAINER_FOLDER,
    "trainingData.yml"
)


# ============================================================
# CREATE TRAINER FOLDER
# ============================================================

os.makedirs(
    TRAINER_FOLDER,
    exist_ok=True
)


# ============================================================
# CREATE LBPH RECOGNIZER
# ============================================================

recognizer = cv2.face.LBPHFaceRecognizer_create()


# ============================================================
# LOAD DATASET
# ============================================================

faces = []
ids = []


if not os.path.exists(DATASET_FOLDER):

    print("❌ Dataset folder not found.")

    exit()


print("\n==========================================")
print("📚 Loading Training Dataset")
print("==========================================\n")


for student_folder in sorted(
    os.listdir(DATASET_FOLDER)
):

    student_path = os.path.join(
        DATASET_FOLDER,
        student_folder
    )


    if not os.path.isdir(student_path):

        continue


    # Student folder must be numeric
    try:

        student_id = int(
            student_folder
        )

    except ValueError:

        continue


    image_count = 0


    for image_name in sorted(
        os.listdir(student_path)
    ):

        image_path = os.path.join(
            student_path,
            image_name
        )


        # ================================================
        # READ IMAGE AS GRAYSCALE
        # ================================================

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )


        if image is None:

            print(
                f"⚠️ Could not read: {image_path}"
            )

            continue


        # ================================================
        # RESIZE
        # ================================================

        image = cv2.resize(
            image,
            (100, 100)
        )


        # ================================================
        # ADD TO TRAINING DATA
        # ================================================

        faces.append(
            image
        )

        ids.append(
            student_id
        )

        image_count += 1


    print(
        f"Student ID {student_id}: "
        f"{image_count} images loaded"
    )


# ============================================================
# CHECK DATA
# ============================================================

if len(faces) == 0:

    print(
        "\n❌ No training images found."
    )

    exit()


print("\n==========================================")

print(
    f"📸 Total images: {len(faces)}"
)

print(
    f"👨‍🎓 Student IDs: {sorted(set(ids))}"
)

print("==========================================\n")


# ============================================================
# TRAIN MODEL
# ============================================================

print(
    "🧠 Training LBPH model..."
)

recognizer.train(
    faces,
    np.array(ids)
)


# ============================================================
# SAVE MODEL
# ============================================================

recognizer.write(
    MODEL_FILE
)


# ============================================================
# COMPLETE
# ============================================================

print("\n==========================================")
print("✅ TRAINING COMPLETED")
print("==========================================")

print(
    f"📸 Images used: {len(faces)}"
)

print(
    f"👨‍🎓 Students trained: {len(set(ids))}"
)

print(
    f"💾 Model saved at:\n{MODEL_FILE}"
)

print("==========================================\n")