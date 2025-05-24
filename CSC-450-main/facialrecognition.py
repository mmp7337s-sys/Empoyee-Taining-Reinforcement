import cv2
import mediapipe as mp
import numpy as np
import time
from tkinter import *
import tkinter.messagebox
import threading #using multi threadding so that program does not lag
import signal
global timer 
timer=0
stop = threading.Event()
# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

nose_positions = []
looking_direction = "Looking Straight"  # Default state


def popup():
    popupwindow = tkinter.Tk()
    popupwindow.title("Warning")
    popupwindow.geometry ("200x100")
    warning=tkinter.Label(popupwindow, text="Please turn attention to the screen")
    warning.pack()
    button1= tkinter.Button(popupwindow, text="OK", command=popupwindow.destroy)
    
    button1.pack()
    popupwindow.mainloop()

    
    
    
#def interrupt_thread():


def countdown():
    global timer, my_timer
    while True:
        if timer == 1:
            my_timer = 5
            interrupted = False
            for x in range(my_timer):
                if stop.is_set():
                    
                    stop.clear()
                    my_timer=5
                    timer=0
                    interrupted = True
                    
                    break
                    
                my_timer -= 1
                time.sleep(1)
                
            if not interrupted:
                popup()
                
            timer = 0
def FacialRecognition():
    global timer
    while cap.isOpened():
       
        ret, image = cap.read()
        if not ret:
            break
    
        height, width, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        result = face_mesh.process(rgb_image)
    
        if result.multi_face_landmarks:
            for facial_landmarks in result.multi_face_landmarks:
                # Nose Tip (Index 1)
                nose = facial_landmarks.landmark[1]
                x_nose = int(nose.x * width)
                y_nose = int(nose.y * height)
    
                left_eye = facial_landmarks.landmark[33]
                right_eye = facial_landmarks.landmark[263]
    
                x_left_eye = int(left_eye.x * width)
                x_right_eye = int(right_eye.x * width)
                y_left_eye = int(left_eye.y * height)
                y_right_eye = int(right_eye.y * height)
    
                face_center_x = (x_left_eye + x_right_eye) // 2
                face_center_y = (y_left_eye + y_right_eye) // 2
    
                
               ## nose_positions.append(y_nose)
               ## if len(nose_positions) > moving_avg_window: ##Five frames
               ##     nose_positions.pop(0)  
               ## avg_nose_y = int(np.mean(nose_positions))
    
                
                y_end = y_nose  
    
                
                if(facial_landmarks.landmark[1]!=None):
                    if y_nose < face_center_y+20:
                        timer=1
                        y_end = y_nose - 50
                        looking_direction = "Looking Up"
                    elif y_nose > face_center_y + 50:
                        timer=1
                        y_end = y_nose + 50
                        looking_direction = "Looking Down"
                        
                    else:
                        stop.set()
                        timer=0
                        looking_direction = "Looking Straight"
                        #interrupt_thread()
                        
                 
                    if x_nose < (face_center_x - 25):  
                        timer=1
                        x_end = x_nose-250
                        looking_direction = "Looking Right"
                        
                        
                        
                    elif x_nose > (face_center_x + 25):
                        timer=1
                        x_end = x_nose+250
                        looking_direction = "Looking Left"
                        
                    else:
                        
                        x_end = x_nose 
    
                if(facial_landmarks.landmark[1]==None):
                    print("Please position your face on the screen")
                cv2.circle(image, (x_nose, y_nose), 3, (0, 255, 0), -1)
    
                # Draw vertical up/down and horizontal left/right movement line
                cv2.line(image, (x_nose, y_nose), (x_end, y_end), (255, 0, 0), 2)
    
                # Display text on the screen
                cv2.putText(image, looking_direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
        cv2.imshow("Nose Tracking", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ =="__main__":
    t1=threading.Thread(target=countdown)
    t2=threading.Thread(target=FacialRecognition)
    t1.start()
    t2.start()
    t1.join()
    t2.join()