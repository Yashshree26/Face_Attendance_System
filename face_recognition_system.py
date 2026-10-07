import cv2
import os
from face_detector import detect_faces

DATASET_PATH = "dataset"

os.makedirs(DATASET_PATH, exist_ok=True)


def capture_faces(student_id, number_of_images=30):

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        return False, "Camera could not be opened."

    count = 0

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detect_faces(gray)

        for (x, y, w, h) in faces:

            count += 1

            face_image = gray[y:y+h, x:x+w]

            filename = os.path.join(
                DATASET_PATH,
                f"User.{student_id}.{count}.jpg"
            )

            cv2.imwrite(filename, face_image)

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Images: {count}/{number_of_images}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Face Registration - Press Q to Stop",
            frame
        )

        key = cv2.waitKey(100) & 0xff

        if key == ord("q"):
            break

        if count >= number_of_images:
            break

    camera.release()
    cv2.destroyAllWindows()

    if count >= number_of_images:

        return True, f"{count} face images captured."

    return False, f"Only {count} images captured."