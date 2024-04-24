#!/usr/bin/env python3
# detect_hands_ssh.py
# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp
import time
from time import sleep
import math

from picrawler import Picrawler
speed = 70 # Speed we want Yelena to move at

# if __name__ == '__main__':

# Starting the video capture with opencv; outlet 1 for usb camera
cap = cv2.VideoCapture(0)

# Creating objects from mediapipe libraries to detect and draw hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prevTime = 0  # Previous time
curTime = 0  # Current time

# Add a count to slow processing rate
count = 1

while True:

    # Start reading from video capture
    ret, frame = cap.read()
    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    # Making an empty landmark list to append to later
    landmark_list = []

    # If we're finding any landmarks
    if results.multi_hand_landmarks:

        # For each hand we're identifying
        for hand_landmarks in results.multi_hand_landmarks:

            # For each landmark in a hand, label the identified landmarks as the corresponding mediapipe landmarks
            for ID, landmark in enumerate(hand_landmarks.landmark):
                # Each ID has corresponding landmark, which has x, y, z
                # We want x, y to determine where hand is
                # x, y, z coordinates given as ratio of image size, so must multiply by image width and height to get
                # the pixel value
                height, width, channels = frame.shape

                # Identifying the x and y coordinates for the center of each landmark in a hand
                xc, yc = int(landmark.x * width), int(landmark.y * height)  # x and y coordinates for center (pixel coordinate for landmark)
                # print(ID, xc, yc)

                # And we're appending these center coordinates, with each landmark ID, to the list we made earlier
                landmark_list.append([ID, xc, yc])

            # Drawing the landmarks we found onto the image (frame), with connections between the landmarks
            mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

    # print(landmark_list)
    # print(len(landmark_list)) # Should get 21 for the 21 landmarks in the hand

    # If we're actually finding any landmarks, identify the thumb and index
        if len(landmark_list) != 0:

            # Stop: 4 (thumb), 8 (index), 12 (middle), 16 (ring), 20 (pinky) are like a standard deviation curve
            # Come:
            # For simplicity's sake, let's do index (8) as come and index and middle (8 and 12) as stop
            print(landmark_list[8], landmark_list[12])

            x1, y1 = landmark_list[8][1], landmark_list[8][2]
            x2, y2 = landmark_list[12][1], landmark_list[12][2]

            # Check that it's identifying the correct points by drawing circles on the fingers
            #cv2.circle(frame, [x1, y1], 10, [255, 255, 255], -1)
            #cv2.circle(frame, [x2, y2], 10, [255, 0, 255], -1)

            # Draw a line between the two fingers; we'll measure the distance of this line for commands later
            #cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)

            # Most important = length; calculate the length of the line
            xc, yc = (x1 + x2) // 2, (y1 + y2) // 2
            #cv2.circle(frame, (xc, yc), 10, (255, 255, 255), cv2.FILLED) # Draw a circle in the center of the line

            length = math.hypot(x2-x1, y2-y1) # Calculating the length of the line
            # print(length)

            # Signal that ready to receive movement commands
            #permission = input('Ready for movement command? ')

            # Frame rate fps



            #sleep(5)
            #print("Analyzing command...")
            print('LENGTH: ', length)
            print()

            if (count % 2) == 1:
                if (length <= 90) & (length > 60):  # Stop moving (for now)
                    # cv2.circle(frame, (xc, yc), 10, (0, 255, 0), cv2.FILLED)

                    print('Going into reset mode...')
                    from picrawler import Picrawler
                    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

                    ## [right front],[left front],[left rear],[right rear]
                    new_step=[[20, 0, 0], [20, 0, 0], [20, 0, 0], [20, -5, 0]]
                    # sit = [[50, 50, -33], [50, 50, -33], [50, 50, -33], [50, 50, -33]]

                    crawler.do_step(new_step, speed)
                    #print(new_step)

                    print("In reset position.")

                elif length > 120:  # Come forward (for now)
                    # cv2.circle(frame, (xc, yc), 10, (0, 0, 0), cv2.FILLED)
                    from picrawler import Picrawler
                    print('Moving forward...')
                    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])
                    #sit = [[50, 50, -33], [50, 50, -33], [50, 50, -33], [50, 50, -33]]
                    crawler.do_action('forward', 1, speed)
                    #crawler.do_step(sit, speed)

                elif length < 50:
                    print('Command to stay. Not moving.')

    #count += 1
    #curTime = time.time()  # Gives us current time
    #fps = 1 / (curTime - prevTime)
    #prevTime = curTime  # Previous time is now the current time

    # Putting fps onto the frame when showing
    #cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
    # Frame rate changes with hands in screen (lower rate with hands)

    #cv2.imshow("Frame", frame)
    #cv2.waitKey(1)