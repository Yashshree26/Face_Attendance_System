from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    Response
)

import cv2
import os

from database import (
    initialize_database,
    add_student,
    get_students,
    get_student,
    mark_attendance,
    get_attendance,
    get_attendance_by_date
)

from face_recognition_system import capture_faces
from train_model import train_model
from face_detector import detect_faces


app = Flask(__name__)

initialize_database()


TRAINER_PATH = "trainer/trainer.yml"


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def index():

    students = get_students()

    attendance = get_attendance()

    present_count = len(attendance)

    return render_template(
        "index.html",
        students=students,
        attendance=attendance,
        present_count=present_count
    )


# --------------------------------------------------
# REGISTER STUDENT
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")

        if not student_id or not name:

            return render_template(
                "register.html",
                error="Student ID and Name are required."
            )

        result = add_student(
            student_id,
            name,
            email,
            department
        )

        if not result:

            return render_template(
                "register.html",
                error="Student ID already exists."
            )

        return redirect(
            url_for(
                "capture",
                student_id=student_id
            )
        )

    return render_template("register.html")


# --------------------------------------------------
# CAPTURE FACE
# --------------------------------------------------

@app.route("/capture/<student_id>")
def capture(student_id):

    student = get_student(student_id)

    if not student:

        return redirect(
            url_for("register")
        )

    success, message = capture_faces(
        student_id
    )

    return render_template(
        "register.html",
        success=message,
        student=student
    )


# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

@app.route("/train", methods=["POST"])
def train():

    success, message = train_model()

    return jsonify({
        "success": success,
        "message": message
    })


# --------------------------------------------------
# ATTENDANCE
# --------------------------------------------------

@app.route("/attendance")
def attendance_page():

    attendance = get_attendance()

    return render_template(
        "attendance.html",
        attendance=attendance
    )


# --------------------------------------------------
# ATTENDANCE BY DATE
# --------------------------------------------------

@app.route("/attendance/date", methods=["POST"])
def attendance_date():

    date = request.form.get("date")

    attendance = get_attendance_by_date(date)

    return render_template(
        "attendance.html",
        attendance=attendance,
        selected_date=date
    )


# --------------------------------------------------
# STUDENTS
# --------------------------------------------------

@app.route("/students")
def students_page():

    students = get_students()

    return render_template(
        "students.html",
        students=students
    )


# --------------------------------------------------
# CAMERA
# --------------------------------------------------

camera = None


def generate_frames():

    global camera

    camera = cv2.VideoCapture(0)

    recognizer = None

    if os.path.exists(TRAINER_PATH):

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        recognizer.read(
            TRAINER_PATH
        )

    while True:

        success, frame = camera.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = detect_faces(gray)

        for (x, y, w, h) in faces:

            student_name = "Unknown"
            confidence = 0

            if recognizer:

                student_id, confidence = recognizer.predict(
                    gray[y:y+h, x:x+w]
                )

                # LBPH confidence:
                # Lower = better
                if confidence < 70:

                    student = get_student(
                        str(student_id)
                    )

                    if student:

                        student_name = student["name"]

                        marked = mark_attendance(
                            student["student_id"],
                            student["name"]
                        )

                        if marked:

                            print(
                                f"Attendance marked: "
                                f"{student['name']}"
                            )

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                student_name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )

    if camera:

        camera.release()


@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )