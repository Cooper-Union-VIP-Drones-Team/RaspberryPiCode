import cv2
import numpy as np
import pyzbar
from pyzbar.pyzbar import decode
import math
import time
import imutils
from imutils import perspective
from imutils import contours
from math import atan2, pi
import multiple_qr as multi
import serial

# after I import multiple qr the code just starts working for no reason

# error when loading PyZbar
# https://github.com/NaturalHistoryMuseum/pyzbar
# fixed by installing C++ 2013

data1 = []
dataList = []

ArduinoUnoSerial = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = .1)

# decoder func
def decoder(image):

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    qr = decode(gray_img)
    CVdecoder = cv2.QRCodeDetector()
    CVdata, CVpoints, _ = CVdecoder.detectAndDecode(gray_img)

    for obj in qr:
        #if CVpoints is None:
        #    goto 
        pt1 = [0,0]
        
        if CVpoints is not None:
            points = CVpoints[0]

            # Coordinate system of 4 corner and rotation
            # separate coordinate data into 4 different points
            pt1 = [int(val) for val in points[0]]
            # pt2 = [int(val) for val in points[1]]
            # pt3 = [int(val) for val in points[2]]
            # pt4 = [int(val) for val in points[3]]
            
            print(pt1)
            
        string = 0;
        if pt1[0] < 315:
            string = "456"
            ArduinoUnoSerial.write(string.encode())
            # ArduinoUnoSerial.write(3, '30')
            time.sleep(1)
        if pt1[0] > 325:
            # a = 0;
            string = "654"
            ArduinoUnoSerial.write(string.encode())
                
        # time.sleep(3)
        msg = ArduinoUnoSerial.readline()
        print("Message from Arduino: ")
        print(msg)

            # use pt1 and pt2 to find the slope, arctan to find the angle
            # if pt1[0] == pt2[0]:
            #    angle = 90
            #else:               
                # slope = ((pt1[1] - pt2[1]) / (pt1[0] - pt2[0]))
                # angle = "{:.2f}".format(np.arctan(slope) * 180 / np.pi)ho
        if CVpoints is not None:
            x = int(pt1[0])
            y = int(pt1[1])

            print("top left corner location is x = ",  pt1[0], " y = ",  pt1[1])
            print("QR angle (in deg):")
            # print(angle)
            points = obj.polygon
        # box the qr
            (x, y, w, h) = obj.rect
            pt = np.array(points, np.int32)
            pt = pt.reshape((-1, 1, 2))
            cv2.polylines(image, [pt], True, (128, 0, 128), 2)

        # dim = gray_img.shape
        # add size = {dim} in print to display camera pixel size
        # Sophia's laptop camera size: 480*640 pixel

            qr_data = obj.data.decode("utf-8")
            qr_read = str(qr_data)
            str0 = str(qr_data)
            if str0 != "":
                str1 = str0.split()
                data1.append(str1.copy())
            # print(str0)
            # print(str1)
            # print(data1[len(data1) - 1])
                print("Total number of scan:")
                print(len(data1))
            for word in data1:
                if word not in dataList:
                    dataList.append(word)
            print("Number of unique QR stored:")
            print(len(dataList))
            print("Last seen QR reads:")
            print(dataList[len(dataList)-1])
        #print(qr_read)
        # display box and qr info on the screen, print qr read and location data
            cv2.putText(frame, qr_read, (x, y), cv2.QT_FONT_NORMAL, 0.3, (255, 255, 255), 1)
        # print(qr_read)
        #print(CVdata)
        

# OpenCV code to turn on live camera
cap = cv2.VideoCapture(0)

# main
while True:
    ret, frame = cap.read()
    # time.sleep(2)
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    # quit by entering q on keyboard
    if code == ord('q'):
        break