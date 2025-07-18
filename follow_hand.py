import math
import turtle

import cv2
import mediapipe as mp


def draw_barrier(wn):
    max_x = wn.window_width()  // 2
    max_y = wn.window_height() // 2
    barrier = turtle.Turtle()
    barrier.hideturtle()
    barrier.penup()
    barrier.goto(-max_x, -max_y)
    barrier.pendown()
    barrier.pensize(3)
    for x, y in [
        ( max_x, -max_y),
        ( max_x,  max_y),
        (-max_x,  max_y),
        (-max_x, -max_y)
    ]:
        barrier.goto(x, y)
    barrier.penup()
    return max_x, max_y

def main():
    # 1. Init MediaPipe Hands with higher precision
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )
    mp_draw = mp.solutions.drawing_utils

    # 2. Open webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 3. Turtle screen + barrier
    wn = turtle.Screen()
    wn.title("Smoothed Point‑Follower with Equal Turning")
    max_x, max_y = draw_barrier(wn)

    t = turtle.Turtle()
    t.shape("turtle")
    t.speed(1)

    # 4. Smoothing state
    alpha = 0.2
    prev_angle = None
    step = 10

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip & process
        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            h_img, w_img, _ = frame.shape

            # Wrist & index tip
            lm_w = hand.landmark[mp_hands.HandLandmark.WRIST]
            lm_t = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x_w, y_w = int(lm_w.x * w_img), int(lm_w.y * h_img)
            x_t, y_t = int(lm_t.x * w_img), int(lm_t.y * h_img)

            # Draw for debug
            cv2.arrowedLine(frame, (x_w, y_w), (x_t, y_t), (0, 255, 0), 3)
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # 5. Raw angle [0,360)
            dx = x_t - (w_img / 2)
            dy = (h_img / 2) - y_t
            raw_angle = math.degrees(math.atan2(dy, dx)) % 360

            # 6. Angle smoothing with wrap-around
            if prev_angle is None:
                smooth_angle = raw_angle
            else:
                diff = (raw_angle - prev_angle + 180) % 360 - 180
                smooth_angle = prev_angle + alpha * diff
            prev_angle = smooth_angle

            # 7. Compute potential next position
            rad   = math.radians(smooth_angle)
            new_x = t.xcor() + step * math.cos(rad)
            new_y = t.ycor() + step * math.sin(rad)

            # 8. Move if inside barrier
            if -max_x < new_x < max_x and -max_y < new_y < max_y:
                t.setheading(smooth_angle)
                t.goto(new_x, new_y)

        # Display & exit
        cv2.imshow("Smoothed Follower", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    turtle.bye()

if __name__ == "__main__":
    main()
