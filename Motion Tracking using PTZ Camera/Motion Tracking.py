import time

import cv2
import sys
import threading
import numpy as np
from sensecam_control import onvif_control

ip = '192.168.0.100'
login = 'admin'
password = '043113'

exit_program = 0


def event_keyboard(k):
    global exit_program

    if k == 27:
        exit_program = 1

    # top
    elif k == ord('w') or k == ord('W'):
        X.relative_move(0, 0.5, 0)

    # left
    elif k == ord('a') or k == ord('A'):
        X.relative_move(-0.1, 0, 0)

    # down
    elif k == ord('s') or k == ord('S'):
        X.relative_move(0, -0.5, 0)

    # right
    elif k == ord('d') or k == ord('D'):
        X.relative_move(0.1, 0, 0)

    # home position
    elif k == ord('h') or k == ord('H'):
        X.go_home_position()

    # Set home position
    elif k == ord('m') or k == ord('M'):
        X.set_home_position()

    # Get PTZ Value
    elif k == ord('n') or k == ord('N'):
        print(X.get_ptz())

    # top left
    elif k == ord('i') or k == ord('I'):
        X.absolute_move(0.5, 0.25, 0)

    # top right
    elif k == ord('o') or k == ord('O'):
        X.absolute_move(-0.5, 0.25, 0)

    # bottom left
    elif k == ord('k') or k == ord('K'):
        X.absolute_move(0.5, -1, 0)

    # bottom right
    elif k == ord('l') or k == ord('L'):
        X.absolute_move(-0.5, -1, 0)


def capture(ip_camera):
    global exit_program

    lst01 = []
    lst02 = []
    a = 0
    b = 0

    ip2 = 'rtsp://admin:043113@192.168.0.100:554/live/profile.0'

    cap = cv2.VideoCapture(ip2)


    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while True:
        ret, frame = cap.read()
        if ret is not False:
            break

    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 2500:
                continue
            a = x + (w / 2)
            b = y + (h / 2)
            lst01.append(a)
            lst02.append(b)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('movement'), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        if len(lst02) > 0:
            x_value = sum(lst01) / len(lst02)
            y_value = sum(lst02) / len(lst02)
            lst01.clear()
            lst02.clear()
            if x_value < 70:
                X.relative_move(-0.1, 0, 0)
            if x_value > 1850:
                X.relative_move(0.1, 0, 0)
            if y_value < 70:
                X.relative_move(0, 0.25, 0)
            if y_value > 1010:
                X.relative_move(0, -0.25, 0)
            print(x_value, y_value)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)



        if exit_program == 1:
            sys.exit()

        frame1 = cv2.resize(frame1, (960, 540))
        cv2.imshow('feed', frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        event_keyboard(cv2.waitKey(1) & 0xff)


X = onvif_control.CameraControl(ip, login, password)
X.camera_start()

t = threading.Thread(target=capture, args=(ip,))
t.start()
