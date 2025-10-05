import cv2
import numpy as np
import time

# Open webcam
cap = cv2.VideoCapture(0)
time.sleep(3)  # let camera adjust

# --- STEP 1: Capture background plate (no person) ---
print("Capturing background... stand out of frame!")
for i in range(60):  # capture for ~2 sec
    ret, bg = cap.read()
    if not ret:
        continue
bg = np.flip(bg, axis=1)  

print("Background captured. Now step in with cloak.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = np.flip(frame, axis=1)  

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

    
    mask_inv = cv2.bitwise_not(mask)

    cloak_area = cv2.bitwise_and(bg, bg, mask=mask)
    non_cloak_area = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final = cv2.addWeighted(cloak_area, 1, non_cloak_area, 1, 0)

    cv2.imshow("Movie-like Invisibility Cloak", final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
