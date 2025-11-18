import cv2
import numpy as np
from tensorflow.keras.models import load_model

# -----------------------------
# Load Face Detector
# -----------------------------
face_cap = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# -----------------------------
# Load Mask Detection Model
# -----------------------------
model = load_model("mask_detector.h5")

IMG_SIZE = 100

# -----------------------------
# Webcam
# -----------------------------
video_cap = cv2.VideoCapture(0)
video_cap.set(3, 640)   # Width
video_cap.set(4, 480)   # Height


while True:
    ret, frame = video_cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # Face Detection
    # -----------------------------
    faces = face_cap.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40)
    )

    for (x, y, w, h) in faces:

        # Handle invalid ROI safely
        if y < 0 or x < 0:
            continue 
        
        face = frame[y:y+h, x:x+w]

        # Skip too-small detections
        if face.size == 0:
            continue

        # Preprocess for model
        face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=0)

        # Prediction
        pred = model.predict(face, verbose=0)[0][0]

        if pred > 0.5:
            label = "MASK"
            color = (0, 255, 0)
            confidence = pred * 100
        else:
            label = "NO MASK"
            color = (0, 0, 255)
            confidence = (1-pred) * 100

        # -----------------------------
        # Draw UI
        # -----------------------------
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        text = f"{label} ({confidence:.1f}%)"
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Mask Detection - Syed Muhammad Arsalan Shah", frame)

    if cv2.waitKey(10) & 0xFF == ord('a'):
        break

video_cap.release()
cv2.destroyAllWindows()
