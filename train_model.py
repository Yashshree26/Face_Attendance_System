import cv2
import os
import numpy as np
from PIL import Image

DATASET_PATH = "dataset"
TRAINER_PATH = "trainer"

os.makedirs(TRAINER_PATH, exist_ok=True)


def train_model():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    face_samples = []
    ids = []

    image_paths = [
        os.path.join(DATASET_PATH, file)
        for file in os.listdir(DATASET_PATH)
        if file.lower().endswith(".jpg")
    ]

    if len(image_paths) == 0:

        return False, "No face images found."

    for image_path in image_paths:

        try:

            pil_image = Image.open(image_path).convert("L")

            image_numpy = np.array(pil_image, "uint8")

            filename = os.path.split(image_path)[-1]

            student_id = int(filename.split(".")[1])

            faces = detector.detectMultiScale(image_numpy)

            for (x, y, w, h) in faces:

                face_samples.append(
                    image_numpy[y:y+h, x:x+w]
                )

                ids.append(student_id)

        except Exception as e:

            print("Error:", e)

    if len(face_samples) == 0:

        return False, "No faces detected in dataset."

    recognizer.train(
        face_samples,
        np.array(ids)
    )

    model_path = os.path.join(
        TRAINER_PATH,
        "trainer.yml"
    )

    recognizer.write(model_path)

    return True, (
        f"Training completed successfully. "
        f"{len(face_samples)} face samples trained."
    )


if __name__ == "__main__":

    success, message = train_model()

    print(message)