import cv2
import imutils
import threading
from playsound import playsound

cap = cv2.VideoCapture(3)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    if not alarm_mode:
        return
    print("Alarm!")
    playsound("sounds/alarm.mp3", False)
    
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)
    
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        
        if threshold.sum() > 300:
            if alarm_counter < 30:
                alarm_counter += 1
        elif alarm_counter > 0:
            alarm_counter -= 1
                
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
    
    print(alarm_counter)
    
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()
    else:
        alarm = False
            
    key_pressed = cv2.waitKey(30) & 0xFF
    if key_pressed == ord('t'):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord('q'):
        alarm_mode = False
        break
    
cap.release()
cv2.destroyAllWindows()