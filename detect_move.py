#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: January 2024 -- 3 June 2024
# Purpose: to detect hands in Yelena's camera and determine which action to take, then takes that action

# Importing necessary packages
import cv2 # Open CV -- for capturing image/video and processing images
import mediapipe as mp # Google's Mediapipe -- for detecting landmarks on hands
import time # time -- to calculate the frame rate (frames per second)
import math # math -- for calculating distance between fingers for gesture recognition
from picrawler import Picrawler # Sunfounder's Picrawler script -- for moving Yelena
import yelena_move as move # Script that contains custom movement functions for Yelena

def init_hands():
    '''
    Creating objects from mediapipe libraries to detect and draw hands.
    Returns Mediapipe's hand library, a Hand object, and drawing utilities
    '''
    
    # Defining what body part we want to detect with Mediapipe's library
    mpHands = mp.solutions.hands
    
    # Creating a Hands object
    hands = mpHands.Hands()
    
    # Initializing our drawing object to draw the landmarks
    mpDraw = mp.solutions.drawing_utils 

    return mpHands, hands, mpDraw

    
def hand_landmarks(imageRGB, hands, mpDraw):
    '''
    Processing the results from the frame & Hands object to determine the landmarks on each hand in the frame.
    For each landmark, label with an ID and determine the center of the landmark.
    Then add to a landmark list and draw onto frame.
    
    Returns landmark_list: a Python list of each landmark's ID and (x, y) center coordinate
    '''
    
    # Converting the frame's color to RGB
    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Processing the image with the Hands object we created earlier
    results = hands.process(imageRGB)

    # Making an empty landmark list to append to later
    landmark_list = []

    # If we're finding any hands landmarks
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

    return landmark_list


def fingers_calculate_draw(landmark_list, frame, finger1=int, finger2=int):
    '''
    Takes the x and y from the two fingers identified in the landmark list and draws circles on each.
    Draws a line between the two fingers, then calculates the center of the line.
    Draws a circle in the center of the line.
    
    Returns length: the length of the line between the fingers
    '''
    
    # Stop: 4 (thumb), 8 (index), 12 (middle), 16 (ring), 20 (pinky) are like a standard deviation curve
    # Come:
    # For simplicity's sake, let's do index (8) as come and index and middle (8 and 12) as stop
    #print(landmark_list[8], landmark_list[12])
    x1, y1 = landmark_list[finger1][1], landmark_list[finger1][2]
    x2, y2 = landmark_list[finger2][1], landmark_list[finger2][2]

    # Check that it's identifying the correct points by drawing circles on the fingers
    cv2.circle(frame, [x1, y1], 10, [255, 255, 255], -1)
    cv2.circle(frame, [x2, y2], 10, [255, 0, 255], -1)

    # Draw a line between the two fingers; we'll measure the distance of this line for commands later
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)

    # Most important = length; calculate the length of the line
    xc, yc = (x1 + x2) // 2, (y1 + y2) // 2
    cv2.circle(frame, (xc, yc), 10, (255, 255, 255), cv2.FILLED) # Draw a circle in the center of the line

    length = math.hypot(x2-x1, y2-y1) # Calculating the length of the line
    #print('Distance between index & thumb: ', length)
    
    return length


def determine_command(length, speed):
    '''
    Takes length of line between fingers and determines which command to follow for each gesture.
    Calls sit() function if fingers at a relaxed distance apart.
    Calls move_forward() function if fingers are stretched apart.
    Calls stay() function if fingers are squished together.
    
    Returns None
    '''
    
    if (length <= 90) & (length > 60):  # Stop moving (for now)
        move.sit(speed)

    elif length > 120:  # Come forward (for now)
        move.move_forward(speed)

    elif length < 50:
        move.stay(speed)


def main():
    
    # Setting the speed we want Yelena to move at
    speed = 70

    # Starting the video capture with opencv; outlet 1 for usb camera
    cap = cv2.VideoCapture(0)

    mpHands, hands, mpDraw = init_hands()
    
    # Preparation for calculating the frame rate
    prevTime = 0  # Previous time
    curTime = 0  # Current time

    # Addding a count to slow the processing rate; processes commands 1/8 times that gets an image
    count = 0

    # Starting an infinite loop to capture hand gestures and move as commanded
    while True:
    
        # Start reading from video capture
        ret, frame = cap.read()
        
        # Using modulo 8 to only run commands every 8th time process a gesture
        # Keeps Yelena from getting stuck in a gesture with a slower frame rate
        if (count % 8) == 1:
            
            # Gets the landmark list from the Hands object & image frame
            landmark_list = hand_landmarks(frame, hands, mpDraw)
            
            # If we're actually finding any landmarks...
            if len(landmark_list) != 0:

                # Identify the index and middle fingers and calculate length between them
                length = fingers_calculate_draw(landmark_list, frame, int(8), int(12))
                # 8 = index finger tip
                # 12 = middle finger tip

                # With the length, determine which movement follows the gesture command
                determine_command(length, speed)

        # Increase the count by one so Yelena takes a command every 1/8th iteration
        count += 1
        
        # Calculate frame rate
        curTime = time.time()  # Gives us current time
        fps = 1 / (curTime - prevTime) # Frame rate is inverse of the current time minus the previous time
    
        prevTime = curTime  # Previous time is now the current time

        # Putting fps onto the frame when showing
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
        # Frame rate changes with hands in screen (lower rate with hands)
        #print("Frame rate: ", int(fps))
        
        # Showing the frame with all the drawings on it (might not show ALL drawings)
        cv2.imshow("Frame", frame)
        
        # Using a waitKey to keep the frame on the screen so we can see it
        cv2.waitKey(1)
        
        
if __name__ == '__main__':
    main()
        
# Eof (end of file)