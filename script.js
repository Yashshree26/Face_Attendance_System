let cameraRunning = false;

const cameraFeed = document.getElementById("cameraFeed");
const cameraPlaceholder = document.getElementById("cameraPlaceholder");
const startButton = document.getElementById("startCamera");
const stopButton = document.getElementById("stopCamera");


// =============================
// CURRENT DATE
// =============================

function showCurrentDate() {

    const dateElement = document.getElementById("currentDate");

    if (!dateElement) {
        return;
    }

    const today = new Date();

    const options = {
        weekday: "short",
        day: "numeric",
        month: "short",
        year: "numeric"
    };

    dateElement.innerText =
        today.toLocaleDateString("en-IN", options);
}

showCurrentDate();


// =============================
// START CAMERA
// =============================

function startCamera() {

    if (cameraRunning) {
        return;
    }

    cameraRunning = true;

    cameraFeed.src = "/video";

    cameraFeed.style.display = "block";

    cameraPlaceholder.style.display = "none";

    document
        .querySelector(".camera-container")
        .classList.add("camera-active");

    document
        .querySelector(".recognition-status")
        .classList.add("active");

    document.getElementById("recognitionStatus").innerText =
        "Face recognition is active";

    document.getElementById("recognizedName").innerText =
        "Scanning...";

    document.getElementById("recognizedMessage").innerText =
        "Looking for a registered face.";

    document.getElementById("confidenceProgress").style.width =
        "45%";

    document.getElementById("confidenceText").innerText =
        "Scanning";

    startButton.disabled = true;

    startButton.style.opacity = "0.6";
}


// =============================
// STOP CAMERA
// =============================

function stopCamera() {

    cameraRunning = false;

    cameraFeed.src = "";

    cameraFeed.style.display = "none";

    cameraPlaceholder.style.display = "block";

    document
        .querySelector(".camera-container")
        .classList.remove("camera-active");

    document
        .querySelector(".recognition-status")
        .classList.remove("active");

    document.getElementById("recognitionStatus").innerText =
        "Camera is currently inactive";

    document.getElementById("recognizedName").innerText =
        "Ready to recognize";

    document.getElementById("recognizedMessage").innerText =
        "Start the camera to detect a student.";

    document.getElementById("confidenceProgress").style.width =
        "0%";

    document.getElementById("confidenceText").innerText =
        "Waiting";

    startButton.disabled = false;

    startButton.style.opacity = "1";
}


// =============================
// PAGE LOAD ANIMATION
// =============================

document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(
        ".stat-card, .card"
    );

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(15px)";

        setTimeout(() => {

            card.style.transition =
                "opacity 0.5s ease, transform 0.5s ease";

            card.style.opacity = "1";

            card.style.transform =
                "translateY(0)";

        }, index * 80);

    });

});


// =============================
// STOP CAMERA WHEN LEAVING PAGE
// =============================

window.addEventListener("beforeunload", function () {

    if (cameraRunning) {
        cameraFeed.src = "";
    }

});