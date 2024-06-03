#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 3 June 2024
# Purpose: library-ish of movement command functions

def sit(speed):
    
    print('\nCommand received: SIT')
    
    from picrawler import Picrawler
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

    ## [right front],[left front],[left rear],[right rear]
    new_step=[[20, 0, 0], [20, 0, 0], [20, 0, 0], [20, -5, 0]]
    # sit = [[50, 50, -33], [50, 50, -33], [50, 50, -33], [50, 50, -33]]

    crawler.do_step(new_step, speed)
    #print(new_step)


def move_forward(speed):
    
    print("\nCommand received: MOVE FORWARD")
    
    # cv2.circle(frame, (xc, yc), 10, (0, 0, 0), cv2.FILLED)
    from picrawler import Picrawler
    print('\nCommand received: MOVE FORWARD')
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])
    #sit = [[50, 50, -33], [50, 50, -33], [50, 50, -33], [50, 50, -33]]
    crawler.do_action('forward', 1, speed)
    #crawler.do_step(sit, speed)
 

def stay(speed):
    
    print("\nCommand received: STAY")
    
# Eof (end of file)