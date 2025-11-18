import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load Face Detector
face_cap = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load Mask Detection Model
model = load_model("mask_detector.h5")

# Model expects (None, 100, 100, 3)
IMG_SIZE = 100

# Webcam
video_cap = cv2.VideoCapture(0)

while True:
    ret, frame = video_cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cap.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    for x, y, w, h in faces:
        # Crop face
        face = frame[y:y+h, x:x+w]

        # Resize to model input size (100x100)
        face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))

        # Preprocess
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=0)   # (1,100,100,3)

        # Predict
        pred = model.predict(face)[0][0]

        if pred < 0.5:
            label = "MASK"
            color = (0, 255, 0)
        else:
            label = "NO MASK"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Mask Detection", frame)

    if cv2.waitKey(10) == ord("a"):
        break

video_cap.release()
cv2.destroyAllWindows()
