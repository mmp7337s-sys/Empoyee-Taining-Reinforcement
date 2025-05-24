"""
video.py

Video player that tracks face while restricting user functions
"""

import time, vlc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading
import pythoncom
import pygetwindow as gw                                                                                                                                   
import time 
import sys
from tkinter import *
from tkthread import *
import os
from win32api import GetSystemMetrics
from datetime import timedelta
import keyboard
import cv2
import mediapipe as mp
from ctypes import windll

global timer 
hard_timer = threading.Event()
# Lock that forces video thread to wait until volume is above 0
check = threading.Condition()
# Time left on video
v_length = 1
# variable used to check if volume is more than zero. 0 = yes, 1 = no
v = 0
close = False
# Lock that forces video thread to wait until volume is above 0
check = threading.Condition()

timer=0
stop = threading.Event()
# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=False,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

cap = cv2.VideoCapture(0)
nose_positions = []
looking_direction = "Looking Straight"  # Default state

#/
    #Used for warning message pop ups
#/
def show_popup(message):
    global v
    def destroy():
        if((AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume).GetMasterVolumeLevel()> -65.25)
           or (AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume).GetMute() == True)):
            root.destroy()
    def disable_event():
        pass
    root = Tk()
    root.title("Warning")
    root.geometry("300x120")
    root.attributes('-topmost', True)
    root.protocol("WM_DELETE_WINDOW", disable_event)
    label = Label(root, text=message, font=("Times", 12), fg="red")
    contin = Button(root, text='Okay', command = destroy)

    label.pack(expand=True)
    contin.pack(side=LEFT,padx=130,pady=0)
    root.mainloop()

#/
    #Countdown of 5 seconds for facial tracking before it pauses the video
#/
def countdown():
    global timer, my_timer, close
    while (close == False):
        if timer == 1:
            my_timer = 2
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
                print("HARD TIMER SET")
                hard_timer.set()  
                
            timer = 0

#/
    #Facial detection functions
#/
def FacialRecognition():
    cv2.namedWindow("Face Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Face Tracking", 320, 240)
    win = gw.getWindowsWithTitle('Face Tracking')[0]
    first_time=True
    was_distracted = False
    global close
    global timer
    frame_counter = 0

    while cap.isOpened() and not close:
    
        ret, image = cap.read()
        if not ret:
            break
    
        frame_counter += 1
        if frame_counter % 2 == 0:
            continue  



        image = cv2.resize(image, (480, 270))
        height, width, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        result = face_mesh.process(rgb_image)
    
        if result.multi_face_landmarks:
            for facial_landmarks in result.multi_face_landmarks:
               
                nose = facial_landmarks.landmark[1]
                left_eye = facial_landmarks.landmark[33]
                right_eye = facial_landmarks.landmark[263]
                x_nose = int(nose.x * width)
                y_nose = int(nose.y * height)

                center_x = (left_eye.x + right_eye.x) / 2
                center_y = (left_eye.y + right_eye.y) / 2

                
                xs = [lm.x for lm in facial_landmarks.landmark]
                ys = [lm.y for lm in facial_landmarks.landmark]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                bbox_width = max_x - min_x
                bbox_height = max_y - min_y

              
                if bbox_width < 0.10:
                    cv2.putText(image, "Move closer", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

               
                face_center_x = (nose.x - center_x) / bbox_width
                face_center_y = (nose.y - center_y) / bbox_height
    
                x_end = x_nose
                y_end = y_nose
                
                if face_center_y < .08:
                    timer=1
                    y_end = y_nose - 50
                    looking_direction = "Looking Up"
                elif face_center_y >.32:
                    timer=1
                    y_end = y_nose + 50
                    looking_direction = "Looking Down"
                elif face_center_x <-.12:
                    timer =1
                    x_end=x_nose-250
                    looking_direction = "Looking Right"
                elif face_center_x>.12:
                    timer=1
                    x_end =x_nose+250
                    looking_direction ="Looking Left"
                    
                else:
                    
                    
                    looking_direction = "Looking Straight"
                    if was_distracted:
                        
                        stop.set()         
                        was_distracted = False
                        timer = 0
                    else:
                        timer = 1
                        was_distracted = True
                    #interrupt_thread()
                    
                 
                    
    

                cv2.circle(image, (x_nose, y_nose), 3, (0, 255, 0), -1)
    
                # Draw vertical up/down and horizontal left/right movement line
                cv2.line(image, (x_nose, y_nose), (x_end, y_end), (255, 0, 0), 2)
    
                # Display text on the screen
                cv2.putText(image, looking_direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.namedWindow("Face Tracking", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Face Tracking", 320, 240)
            cv2.imshow("Face Tracking", image)
            cv2.waitKey(1)
            if first_time:
                time.sleep(0.2)
                win.activate()
                win.alwaysOnTop = True
                first_time = False
                try:
                    win.activate()
                    win.alwaysOnTop = True
                    first_time = False
                except Exception as e:
                    print(f"Could not set always on top: {e}")
            if win:
                try:
                    if not win.isActive:
                        win.activate()
                        win.alwaysOnTop = True
                except Exception as e:
                    print(f"Error re-activating window: {e}")
        else:
            timer=1
            cv2.putText(image, "No face detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            win.activate()
            win.alwaysOnTop = True
        cv2.namedWindow("Face Tracking", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Face Tracking", 320, 240)
        cv2.imshow("Face Tracking", image)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists("cert_done.signal"):
        os.remove("cert_done.signal")

#/
    #The video player
    
    #video(stirng): The path to the video file
#/
def vlc_video(video):
    global close
    global v
    global v_length
    volume = 100.00
    class VlcPlayer(Tk):

        def __init__(self):
            def monitor_thread():
                while(True):
                                        
                    if hard_timer.is_set():
                        self.pause_video_facial_recognition()
                    if stop.is_set() and self.video_paused and self.button_flag == False and v == 0:
                        self.vlcplayer.play()
                        self.video_paused = False
                        stop.clear()  # clear the signal
                    
                    if(v == 1 and not self.video_paused):
                        self.vlcplayer.pause()
                        self.video_paused = True
                        with check:
                            check.wait()
                    if self.vlcplayer.get_state() == vlc.State.Ended:

                        with open("cert_done.signal", "w") as f:
                            f.write("done")
                        self.destroy()

            super().__init__()
            self.button_flag = False
            self.title(os.path.basename(video))
            self.geometry(str(GetSystemMetrics(0))+'x'+str(GetSystemMetrics(1)))
            self.config(background="#5E0009")
            self.initialize_player()
            self.t3=threading.Thread(target=monitor_thread)
            self.t3.daemon = True

        def initialize_player(self):
            self.vlcplayer = vlc.MediaPlayer()
            self.current_file = vlc.Media(video)
            self.playing_video = False
            self.video_paused = False
            self.create_widgets()
        
        def create_widgets(self):
            self.media_canvas = Canvas(self, bg="black", width=800, height=400)
            self.media_canvas.pack(pady=10, fill= BOTH, expand=True)
            self.time_label = Label(
                self,
                text="00:00:00 / 00:00:00",
                font=("Arial", 12, "bold"),
                fg="#555555",
                bg="#f0f0f0",
            )
            self.time_label.pack(pady=5)
            self.control_buttons_frame = Frame(self, bg="#f0f0f0")
            self.control_buttons_frame.pack(pady=5)
            self.play_button = Button(
                self.control_buttons_frame,
                text="Play",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=self.play_video,
            )
            self.play_button.pack(side=LEFT, padx=5, pady=5)
            self.pause_button = Button(
                self.control_buttons_frame,
                text="Pause/Resume",
                font=("Arial", 12, "bold"),
                bg="#FF9800",
                fg="white",
                command=self.pause_video,
            )
            self.pause_button.pack(side=LEFT, padx=10, pady=5)
            self.slider = Scale(
                font=("Arial", 12, "bold"),
                bg="#5E0009",
                fg="white",
                from_=30,
                to=100,
                orient=HORIZONTAL,
                variable = volume,
                command = self.set_volume
            )
            # self.slider.bind("<ButtonRelease-1>",self.set_volume)
            self.slider.pack(side=BOTTOM, padx=5, pady=5)
            self.slider.set(50)

        def set_volume(self,volume):
            self.vlcplayer.audio_set_volume(int(volume))

        def select_file(self):
            self.current_file = video
            self.time_label.config(text="00:00:00 / " + self.get_duration_str())
            self.play_video()
        
        def get_duration_str(self):
            if self.playing_video:
                total_duration = self.vlcplayer.get_length()
                total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
                return total_duration_str
            return "00:00:00"
        
        def play_video(self):
            if not self.playing_video:
                self.vlcplayer.set_media(self.current_file)
                self.vlcplayer.set_hwnd(self.media_canvas.winfo_id())
                self.t3.start()
                while v == 1:
                    pass
                self.vlcplayer.play()
                self.playing_video = True
        
        def pause_video(self):
            if self.playing_video and v == 0:
                if (self.video_paused):
                    self.vlcplayer.play()
                    self.video_paused = False
                    self.button_flag = False
                else:
                    self.vlcplayer.pause()
                    self.video_paused = True
                    self.button_flag = True
        def pause_video_facial_recognition(self):
            global hard_timer
            if self.vlcplayer.get_state() == vlc.State.Playing and not self.video_paused and self.button_flag == False:
                self.vlcplayer.pause()
                self.button_flag = False
                self.video_paused = True
                hard_timer.clear()  # clear the signal to prevent re-trigger

        def set_video_position(self, value):
            if self.playing_video:
                total_duration = self.vlcplayer.get_length()
                position = int((float(value) / 100) * total_duration)
                self.vlcplayer.set_time(position)
        
        def update_video_progress(self):
            if self.playing_video:
                total_duration = self.vlcplayer.get_length()
                current_time = self.vlcplayer.get_time()
                current_time_str = str(timedelta(milliseconds=current_time))[:-3]
                total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
                self.time_label.config(text=f"{current_time_str}/{total_duration_str}")
            self.after(1000, self.update_video_progress)
    
    vlcplayer = VlcPlayer()
    vlcplayer.update_video_progress()
    vlcplayer.wm_protocol("WM_DELETE_WINDOW")
    vlcplayer.overrideredirect(True)
    vlcplayer.mainloop()
    close = True

#/
    #Checks that volume is not 0, or that the mute button is not pressed
#/
def volume():
    global v
    global v_length
    pythoncom.CoInitialize()
    # Runs thread as long as the video does not reach end (which is 191 for some reason)
    while(close == False):
        volume = AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume).GetMasterVolumeLevel()
        if (volume <= -65.25 or (AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume).GetMute() == True)):
            v = 1
            t3 = threading.Thread(target=show_popup, args = ("Volume must be above 0!",))
            t3.daemon = True
            if( t3._started.is_set() == False):
                t3.start()
                t3.join()
        else:
            v = 0
            with check:
                check.notify()

#/
    # main function handling the face detection, volume checking, and video player threads. Also restricts user functions until all threads are ended
#/
if __name__ =="__main__":
    if ((AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume).GetMasterVolumeLevel() <= -65.25)
        or (AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume).GetMute() == True)):
        show_popup("Volume must be above 0, or muted!")
    windll.user32.ShowWindow(windll.user32.FindWindowA(b'Shell_TrayWnd', None), 0)
    keyboard.block_key('win')
    keyboard.block_key('alt')
    keyboard.block_key('shift')
    keyboard.block_key('tab')
    keyboard.block_key('delete')
    keyboard.block_key('ctrl')
    keyboard.block_key('home')
    keyboard.block_key('print_screen')
    t1 = threading.Thread(target=countdown)
    t2 = threading.Thread(target=FacialRecognition)
    t3 = threading.Thread(target=vlc_video, args = (sys.argv[1],))
    t4 = threading.Thread(target=volume)


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    windll.user32.ShowWindow(windll.user32.FindWindowA(b'Shell_TrayWnd', None), 1)