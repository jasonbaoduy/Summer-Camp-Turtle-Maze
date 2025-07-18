import cv2
import numpy as np


def nothing(x):
    pass

# 1. Create window and trackbars for HSV min/max
cv2.namedWindow('HSV Adjust', cv2.WINDOW_NORMAL)
cv2.resizeWindow('HSV Adjust', 400, 240)
cv2.createTrackbar('Hue Min','HSV Adjust',  0, 179, nothing)
cv2.createTrackbar('Hue Max','HSV Adjust',179, 179, nothing)
cv2.createTrackbar('Sat Min','HSV Adjust',  0, 255, nothing)
cv2.createTrackbar('Sat Max','HSV Adjust',255, 255, nothing)
cv2.createTrackbar('Val Min','HSV Adjust',  0, 255, nothing)
cv2.createTrackbar('Val Max','HSV Adjust',255, 255, nothing)

# 2. Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Flip horizontally
    frame = cv2.flip(frame, 1)

    # 4. Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 5. Read trackbar positions
    h_min = cv2.getTrackbarPos('Hue Min', 'HSV Adjust')
    h_max = cv2.getTrackbarPos('Hue Max', 'HSV Adjust')
    s_min = cv2.getTrackbarPos('Sat Min', 'HSV Adjust')
    s_max = cv2.getTrackbarPos('Sat Max', 'HSV Adjust')
    v_min = cv2.getTrackbarPos('Val Min', 'HSV Adjust')
    v_max = cv2.getTrackbarPos('Val Max', 'HSV Adjust')

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # 6. Threshold and clean mask
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 7. Find largest contour and compute center
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        center_x = x + w // 2
        center_y = y + h // 2
        center = np.array([center_x, center_y], dtype=int)
        print("Center of bounding box:", center)

        # 8. Draw bounding box and center point
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # 9. Display
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
