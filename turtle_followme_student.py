# blue_follower_template.py

import turtle

import cv2
import numpy as np


def calculate_bounding_box(mask):
    """
    TODO (student):
      - Find contours in `mask`
      - Select the largest contour
      - Compute (x, y, w, h) via cv2.boundingRect
      - Compute centroid cx = x + w//2, cy = y + h//2
      - Return x, y, w, h, cx, cy
    """
    raise NotImplementedError("Implement bounding‑box & centroid")

def move_turtle(t, cx, cy, mask_shape, step=5):
    """

      - Given centroid (cx, cy) and mask_shape (h, w):
      - Compute dx = cx - w//2, dy = cy - h//2
      - Face east/west if |dx| > |dy| else north/south
      - Move forward by `step`
    """
    raise NotImplementedError("Implement turtle movement")

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    wn = turtle.Screen()
    wn.title("Blue Follower Turtle")
    t = turtle.Turtle()
    t.shape("turtle")
    t.speed(1)    # slow turtle

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip horizontally
        frame = cv2.flip(frame, 1)

        # Create blue mask
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv     = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        lower_b = np.array([100, 150,  50])
        upper_b = np.array([140, 255, 255])
        mask    = cv2.inRange(hsv, lower_b, upper_b)

        # Student fills in these:
        x, y, w, h, cx, cy = calculate_bounding_box(mask)

        # Draw feedback
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle   (frame, (cx, cy), 5, (0,   0,   255), -1)

        cv2.imshow("Webcam", frame)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            move_turtle(t, cx, cy, mask.shape)

    cap.release()
    cv2.destroyAllWindows()
    turtle.bye()

if __name__ == "__main__":
    main()
