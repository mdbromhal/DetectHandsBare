# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode  # Creating an object that has its own variable
        self.maxHands = maxHands  # Defining as user defines
        self.detectionConfidence = int(detectionConfidence * 100) # Edit from ChatGPT
        self.trackConfidence = int(trackConfidence * 100)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionConfidence,
                                        self.trackConfidence)  # Creating a Hands object, only uses RGB images
        # Passing Hands the parameters used in its __init__ (cntrl-enter/click to see functions inside function)
        self.mpDraw = mp.solutions.drawing_utils  # Drawing utilities

    def find_hands(self, frame, draw=True):

        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)

        # Now we want to extract that information
        # Going to open object, checking if we have multiple hands
        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(frame, handLandmarks,
                                               self.mpHands.HAND_CONNECTIONS)  # Want to use the original frame from capture read
            # Using the RGB one does not work
            # HAND_CONNECTIONS draws connections between points

        return frame

    def find_position(self, frame, handNo=0, draw=True):

        landmark_lst = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[handNo]

            for id, lndmrk in enumerate(my_hand.landmark):
                # Each ID has corresponding landmark, which has x, y, z
                # We want x, y to determine where hand is
                # x, y, z coordinates given as ratio of image size, so must multiply by image width and height to get
                # the pixel value
                height, width, channels = frame.shape

                xc, yc = int(lndmrk.x * width), int(
                    lndmrk.y * height)  # x and y coordinates for center (pixel coordinate for landmark)

                landmark_lst.append([id, xc, yc])

                if draw:
                    cv2.circle(frame, (xc, yc), 15, (255, 0, 255), cv2.FILLED)

        return landmark_lst


def main():
    # Frame rate fps
    prevTime = 0  # Previous time
    curTime = 0  # Current time

    cap = cv2.VideoCapture(0)

    # Creating a handDetector object
    detector = HandDetector()

    while True:
        ret, frame = cap.read()

        # Send image to detector
        frame = detector.find_hands(frame)

        landmark_lst = detector.find_position(frame)
        # if len(landmark_lst) !=0:
        #     print()

        curTime = time.time()  # Gives us current time
        fps = 1 / (curTime - prevTime)
        prevTime = curTime  # Previous time is now the current time

        # Putting fps onto the frame when showing
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
        # Frame rate changes with hands in screen (lower rate with hands)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    # If we're running this script, do this...
    main()
