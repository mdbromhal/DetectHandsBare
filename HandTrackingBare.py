# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Frame rate fps
prevTime = 0  # Previous time
curTime = 0  # Current time

while True:
    ret, frame = cap.read()
    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            for ID, landmark in enumerate(hand_landmarks.landmark):
                # Each ID has corresponding landmark, which has x, y, z
                # We want x, y to determine where hand is
                # x, y, z coordinates given as ratio of image size, so must multiply by image width and height to get
                # the pixel value
                height, width, channels = frame.shape

                xc, yc = int(landmark.x * width), int(
                    landmark.y * height)  # x and y coordinates for center (pixel coordinate for landmark)
                print(ID, xc, yc)

            mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

    curTime = time.time()  # Gives us current time
    fps = 1 / (curTime - prevTime)
    prevTime = curTime  # Previous time is now the current time

    # Putting fps onto the frame when showing
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
    # Frame rate changes with hands in screen (lower rate with hands)

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
