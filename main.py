#!usr/bin/python3
import os
import sys
from picamera2 import Picamera2
import struct
import pickle
#import imutils
import socket
import cv2



if __name__ == '__main__':

    picam2 = Picamera2()
    picam2.start_and_record_video("out/test.mp4", duration=5)

    # Server socket
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    #host_ip = socket.gethostbyname(host_name)
    host_ip = '0.0.0.0'
    print('HOST IP:',host_ip)
    port = 10050
    socket_address = (host_ip,port)
    print('Socket created')
    # bind the socket to the host. 
    #The values passed to bind() depend on the address family of the socket
    server_socket.bind(socket_address)
    print('Socket bind complete')
    #listen() enables a server to accept() connections
    #listen() has a backlog parameter. 
    #It specifies the number of unaccepted connections that the system will allow before refusing new connections.
    server_socket.listen(5)
    print('Socket now listening')

    while True:
        client_socket,addr = server_socket.accept()
        print('Connection from:',addr)
        if client_socket:
            #vid = cv2.VideoCapture(0)
            vid = cv2.VideoCapture(picam2)
            while(vid.isOpened()):
                img,frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                cv2.imshow('Sending...',frame)
                key = cv2.waitKey(10) 
                if key ==13:
                    client_socket.close()

    input("Press ENTER to exit.")
    print("Bye!")
