# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp
import time
import math

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

    landmark_list = []

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
                # print(ID, xc, yc)
                landmark_list.append([ID, xc, yc])

            mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

    # print(landmark_list)
    # print(len(landmark_list)) # Should get 21 for the 21 landmarks in the hand

    if len(landmark_list) != 0:
        # Stop: 4 (thumb), 8 (index), 12 (middle), 16 (ring), 20 (pinky) are like a standard deviation curve
        # Come:
        # For simplicity's sake, let's do index (8) as come and index and middle (8 and 12) as stop
        print(landmark_list[8], landmark_list[12])

        x1, y1 = landmark_list[8][1], landmark_list[8][2]
        x2, y2 = landmark_list[12][1], landmark_list[12][2]

        # Check that it's identifying the correct points
        cv2.circle(frame, [x1, y1], 10, [255, 255, 255], -1)
        cv2.circle(frame, [x2, y2], 10, [255, 0, 255], -1)

        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)

        # Most important = length
        xc, yc = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(frame, (xc, yc), 10, (255, 255, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

	# Signal that ready to receive movement commands
#	print("Ready for movement command.")

        if length < 50:  # Stop moving (for now)
            cv2.circle(frame, (xc, yc), 10, (0, 255, 0), cv2.FILLED)

            from picrawler import Picrawler
            from time import sleep

            crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

            ## [right front],[left front],[left rear],[right rear]
            new_step=[[20, 0, 0], [20, 0, 0], [20, 0, 0], [20, -5, 0]]
            # sit = [[50, 50, -33], [50, 50, -33], [50, 50, -33], [50, 50, -33]]

            speed = 70
            sleep(1)
            crawler.do_step(new_step,speed)
            print(new_step)
            sleep(2)
            print("In reset position.")

        elif length > 75:  # Come forward (for now)
            cv2.circle(frame, (xc, yc), 10, (0, 0, 0), cv2.FILLED)

            from picrawler import Picrawler
            from time import sleep

            crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])
            speed = 70
	    # count = 3
            # while count > 0:
            crawler.do_action('forward',2,speed)
            sleep(0.05)
		# count -= 1

    curTime = time.time()  # Gives us current time
    fps = 1 / (curTime - prevTime)
    prevTime = curTime  # Previous time is now the current time

    # Putting fps onto the frame when showing
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
    # Frame rate changes with hands in screen (lower rate with hands)

#    cv2.imshow("Frame", frame)
#    cv2.waitKey(1)
