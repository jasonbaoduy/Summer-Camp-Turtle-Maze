import cv2
import threading
from ultralytics import YOLO

# === USER CONFIGURATION ===
SRC         = 0                 # camera source index
WIDTH       = 640               # capture width
HEIGHT      = 480               # capture height
MODEL_PATH  = 'yolov8n.pt'      # YOLOv8 model
COLOR_SPACE = 'HSV'             # 'BGR', 'GRAY', or 'HSV'
BOX_COLOR   = (0, 255, 0)       # box color in BGR
TEXT_COLOR  = (0, 0, 0)         # text color in BGR
# ===========================

class CameraStream:
    """Continuously read frames in background."""
    def __init__(self, src=SRC, width=WIDTH, height=HEIGHT):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while not self.stopped:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.stopped = True
        self.cap.release()

# Load model
model = YOLO(MODEL_PATH)

# Start camera
cam = CameraStream()
if not cam.ret:
    print("Error: cannot access webcam.")
    cam.release()
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Convert for display
    cs = COLOR_SPACE.upper()
    if cs == 'GRAY':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        disp_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif cs == 'HSV':
        # Single-window HSV view
        disp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    else:  # BGR
        disp_frame = frame.copy()

    # Run detection on original BGR frame
    results = model(frame)[0]

    # Draw boxes + labels on disp_frame
    for box in results.boxes:
        if int(box.cls[0]) != 0:
            continue
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        label = f"person {conf:.2f}"

        cv2.rectangle(disp_frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
        (w, h_lbl), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(disp_frame,
                      (x1, y1 - h_lbl - 4),
                      (x1 + w, y1),
                      BOX_COLOR, -1)
        cv2.putText(disp_frame, label, (x1, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 2,
                    cv2.LINE_AA)

    # Show only the main window
    cv2.imshow('YOLOv8 Person Detection', disp_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cam.release()
cv2.destroyAllWindows()
