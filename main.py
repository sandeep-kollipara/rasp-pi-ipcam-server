#!usr/bin/python3
import os
import sys
from picamera2 import Picamera2



if __name__ == '__main__':

    picam2 = Picamera2()
    picam2..start_and_record_video("out/test.mp4", duration=5)

    input("Press ENTER to exit.")
    print("Bye!")
