import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="🤚 Live Finger Detector", layout="centered")
st.title("🤚 Real-Time Finger Detector")
st.markdown("""
Apna **haath green box** ke andar rakhein aur apni fingers count hoti dekhein — live!
""")

# -------------- Finger Counting Logic --------------
def count_fingers(frame):
    h, w, _ = frame.shape
    x1, y1, x2, y2 = w//4, h//4, 3*w//4, 3*h//4
    roi = frame[y1:y2, x1:x2]

    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 3)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35,35), 0)
    _, thresh = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)==0:
        return 0, frame
    cnt = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(cnt, returnPoints=False)
    if hull is None or len(hull)<3:
        return 0, frame
    defects = cv2.convexityDefects(cnt, hull)
    if defects is None:
        return 0, frame

    finger_count = 0
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = np.linalg.norm(np.array(end)-np.array(start))
        b = np.linalg.norm(np.array(far)-np.array(start))
        c = np.linalg.norm(np.array(end)-np.array(far))
        angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c + 1e-6))
        if angle <= np.pi/2:
            finger_count += 1
            cv2.circle(roi, far, 8, [255,0,0], -1)

    finger_count = finger_count + 1 if finger_count > 0 else 0
    return finger_count, frame

# -------------- Real-Time Camera Feed --------------
run = st.checkbox("Start Camera 🎥")
FRAME_WINDOW = st.image([])

camera = None
if run:
    camera = cv2.VideoCapture(0)
else:
    st.info("✅ Click 'Start Camera 🎥' to begin live detection.")

while run:
    ret, frame = camera.read()
    if not ret:
        st.warning("⚠️ Camera not detected!")
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    fingers, annotated = count_fingers(frame)
    cv2.putText(annotated, f"Fingers: {fingers}", (30, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
    FRAME_WINDOW.image(annotated, channels="BGR")

if camera is not None:
    camera.release()