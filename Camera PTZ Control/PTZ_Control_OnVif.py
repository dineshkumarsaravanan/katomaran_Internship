import cv2
import sys
import threading
from sensecam_control import onvif_control


ip = '192.168.0.104'
login = 'admin'
password = '043113'

exit_program = 0


def event_keyboard(k):
    global exit_program

    if k == 27:  
        exit_program = 1

    #top
    elif k == ord('w') or k == ord('W'):
        X.relative_move(0, 0.5, 0)

    #left
    elif k == ord('a') or k == ord('A'):
        X.relative_move(-0.1, 0, 0)

    #down
    elif k == ord('s') or k == ord('S'):
        X.relative_move(0, -0.5, 0)

    #right
    elif k == ord('d') or k == ord('D'):
        X.relative_move(0.1, 0, 0)

    #home position
    elif k == ord('h') or k == ord('H'):
        X.go_home_position()

    #Set home position
    elif k == ord('m') or k == ord('M'):
        X.set_home_position()
        
    #Get PTZ Value
    elif k == ord('n') or k == ord('N'):
        print(X.get_ptz())  

    #Stop Move
    elif k == ord('v') or k == ord('V'):
        X.stop_move()    

    #top left
    elif k == ord('i') or k == ord('I'):
        X.absolute_move(0.5, 0.25, 0)

    #top right
    elif k == ord('o') or k == ord('O'):
        X.absolute_move(-0.5, 0.25, 0)

    #bottom left
    elif k == ord('k') or k == ord('K'):
        X.absolute_move(0.5, -1, 0)
        
    #bottom right
    elif k == ord('l') or k == ord('L'):
        X.absolute_move(-0.5, -1, 0)


def capture(ip_camera):
    global exit_program

    ip2 = 'rtsp://admin:043113@192.168.0.104:554/live/profile.0'
    print("W - Top")
    print("A - Left")
    print("S - Down")
    print("D - Right")
    print("H - Home Position")
    print("M - Set Home Position")
    print("N - Get PTZ Value")
    print("V - Stop Move")
    print("I - Top Left")
    print("O - Top Right")
    print("K - Bottom Left")
    print("L - Bottom Right")

    cap = cv2.VideoCapture(ip2)

    while True:
        ret, frame = cap.read()
        if ret is not False:
            break

    while True:
        ret, frame = cap.read()

        if exit_program == 1:
            sys.exit()

        frame = cv2.resize(frame, (960, 540))
        cv2.imshow('Camera', frame)

        event_keyboard(cv2.waitKey(1) & 0xff)


X = onvif_control.CameraControl(ip, login, password)
X.camera_start()

t = threading.Thread(target=capture, args=(ip,))
t.start()