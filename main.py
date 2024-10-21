import cv2
import mediapipe as mp
import time
from gesture_judgment import detect_all_finger_state, detect_hand_state


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

recent_states = [''] * 30    # Store the last 30 gesture judgment results

cap = cv2.VideoCapture(0)

prev_time = 0
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Horizontal mirror flipping
    h, w = frame.shape[:2]
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    keypoints = hands.process(image)

    if keypoints.multi_hand_landmarks:
        lm = keypoints.multi_hand_landmarks[0]
        lmHand = mp_hands.HandLandmark

        landmark_list = [[] for _ in range(6)]  # Landmark List has 6 sub lists, which store the root node coordinates (0 point) and the key point coordinates of the other 5 fingers

        for index, landmark in enumerate(lm.landmark):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            if index == lmHand.WRIST:
                landmark_list[0].append((x, y))
            elif 1 <= index <= 4:
                landmark_list[1].append((x, y))
            elif 5 <= index <= 8:
                landmark_list[2].append((x, y))
            elif 9 <= index <= 12:
                landmark_list[3].append((x, y))
            elif 13 <= index <= 16:
                landmark_list[4].append((x, y))
            elif 17 <= index <= 20:
                landmark_list[5].append((x, y))

        # Obtain the coordinates of all joint points
        point0 = landmark_list[0][0]
        point1, point2, point3, point4 = landmark_list[1][0], landmark_list[1][1], landmark_list[1][2], landmark_list[1][3]
        point5, point6, point7, point8 = landmark_list[2][0], landmark_list[2][1], landmark_list[2][2], landmark_list[2][3]
        point9, point10, point11, point12 = landmark_list[3][0], landmark_list[3][1], landmark_list[3][2], landmark_list[3][3]
        point13, point14, point15, point16 = landmark_list[4][0], landmark_list[4][1], landmark_list[4][2], landmark_list[4][3]
        point17, point18, point19, point20 = landmark_list[5][0], landmark_list[5][1], landmark_list[5][2], landmark_list[5][3]

        # Store the coordinates of all key points together to simplify the parameters of subsequent functions
        all_points = {'point0': landmark_list[0][0],
                        'point1': landmark_list[1][0], 'point2': landmark_list[1][1], 'point3': landmark_list[1][2], 'point4': landmark_list[1][3],
                        'point5': landmark_list[2][0], 'point6': landmark_list[2][1], 'point7': landmark_list[2][2], 'point8': landmark_list[2][3],
                        'point9': landmark_list[3][0], 'point10': landmark_list[3][1], 'point11': landmark_list[3][2], 'point12': landmark_list[3][3],
                        'point13': landmark_list[4][0], 'point14': landmark_list[4][1], 'point15': landmark_list[4][2], 'point16': landmark_list[4][3],
                        'point17': landmark_list[5][0], 'point18': landmark_list[5][1], 'point19': landmark_list[5][2], 'point20': landmark_list[5][3]}

        # Call a function to determine the bending or straightening state of each finger
        bend_states, straighten_states = detect_all_finger_state(all_points)

        # Call a function to detect the current gesture
        current_state = detect_hand_state(all_points, bend_states, straighten_states)

        # Update recent status list
        recent_states.pop(0)
        recent_states.append(current_state)

        # Check if all states in the list are the same
        if len(set(recent_states)) == 1:        # If the gesture status remains the same for 30 consecutive frames, it is considered stable and the current gesture is output
            print("Detected consistent hand state:", recent_states[0])
            cv2.putText(frame, current_state, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        for hand_landmarks in keypoints.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

    curr_time = time.time()             # Calculate frame rate
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Draw frame rate on the screen
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()