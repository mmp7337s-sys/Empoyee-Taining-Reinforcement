"""
man_gui.py

Manager GUI to run hash comparison separate from the employee GUI
"""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from globals import verify_certificate
from globals import get_yt_video
import os
from datetime import datetime

window = Tk() ##instantiate an instance of a window             
window.title("Employee Training Completion Enforcement - Manager Interface")   #title of window
window.geometry("600x600")  #screen dimensions
window.config(background="#5E0009") ##background color
vers_text = StringVar()
vers_text.set("Manager Interface")
versionLbl = Label(window, textvariable=vers_text, anchor=CENTER, height=5, width=20, font=("Arial", 16), bg="#5E0009",fg="#FFFFFF")
versionLbl.pack()
global vidPath                          #set global path variable to be modified from anywhere in the code where we need to
raw_video_name = ""
accepted_dates = "%m/%d/%Y"     ##accept date format MM/DD/YYYY
url = StringVar()

#/
    #produce the form for user info entry
#/
def get_credentials():
    global form_win     #first set of global vars for getting textbox data
    global first_txtBox
    global last_txtBox
    global dob_txtBox
    global mNum_txtBox
    global hash_txtBox

    form_win = Tk()
    form_win.title("Enter Credentials")
    form_win.geometry("350x300")
    
    instr = Label(form_win, text="Please enter your information")
    instr.grid(row=0, column=0, padx=5, pady=5)

    first_label = Label(form_win, text="First Name")
    first_label.grid(row=1, column=0, padx=5, pady=10)

    first_txtBox = Entry(form_win)
    first_txtBox.grid(row=1, column=1, padx=10, pady=10)

    last_label = Label(form_win, text="Last Name")
    last_label.grid(row=2, column=0, padx=5, pady=10)
    last_txtBox = Entry(form_win)
    last_txtBox.grid(row=2, column=1, padx=10, pady=10)

    mNum_label = Label(form_win, text="M-Number")
    mNum_label.grid(row=3, column=0, padx=5, pady=10)
    mNum_txtBox = Entry(form_win)
    mNum_txtBox.grid(row=3, column=1, padx=10, pady=10)

    dob_label = Label(form_win, text="Date of Birth")
    dob_label.grid(row=4, column=0, padx=5, pady=10)
    dob_txtBox = Entry(form_win)
    dob_txtBox.grid(row=4, column=1, padx=10, pady=10)

    hash_txtBox = Label(form_win, text="Certificate Hash")
    hash_txtBox.grid(row=5, column=0, padx=5, pady=10)
    hash_txtBox = Entry(form_win)
    hash_txtBox.grid(row=5, column=1, padx=10, pady=10)

    submit = Button(form_win, text='Compare', command=confirm)
    submit.grid(row=6, column=0, pady=5, columnspan=3)
    submit.config(background="#5E0009", fg="#FFFFFF")

#/
    #check input DoB to match MM/DD/YYYY format

    #Retrun: Returns True if dob is formatted correctly, false otherwise
#/
def checkDOB():
    try:
        datetime.strptime(dob, accepted_dates)
        return True
    except ValueError:      ##catch user entering chars, special chars, or the wrong date format
        return False

#/
    #submit button command
#/
def confirm():
    global first    #second set of global vars to hold returned textbox data
    global last
    global dob
    global mNum
    global vidPath
    global hash
    first = first_txtBox.get()
    last = last_txtBox.get()
    mNum = mNum_txtBox.get()
    dob = dob_txtBox.get()
    hash = hash_txtBox.get()
    print("hash: " + hash)
    #input validation for first, last, dob, and M-number
    if not first or not last or not dob or not mNum:
        messagebox.showerror("Missing information",message="All fields must be filled before submission.", parent=form_win)
    elif not first.isalpha() or not last.isalpha():
        messagebox.showerror("Invalid input",message="First and last name must not contain numbers or symbols.", parent=form_win)
    elif not mNum.isdigit():
        messagebox.showerror("Invalid MNumber", message="M-number must not contain characters or symbols.", parent=form_win)
    elif len(mNum) < 8 or len(mNum) > 8:
        messagebox.showerror("Invalid M-number",message="Please enter 8-digit bear number", parent=form_win)
    elif not checkDOB():
        messagebox.showerror("Invalid DOB", message="Please enter a valid date. MM/DD/YYYY", parent=form_win)
    else:
        #get actual video name
        raw_video_name = os.path.basename(vidPath)
        ##hold value of certificate hash
        userHash = hash

        #hash comparison to verify user info and the correct video watched
        if verify_certificate(first, last, dob, mNum, raw_video_name, userHash):
            messagebox.showinfo(message="Verification Successful! You may check another hash.", parent=form_win)
            #close the form
            form_win.destroy()
        else:
            messagebox.showerror("Verification Failed", message="The hash values do not match. Check values and try again.", parent=form_win)

    
#/
    #Runs video.py with reference given by file explorer
#/
def vlc_player():
    global vidPath
    if(url.get() == ""):
        vidPath = filedialog.askopenfilename(               #open the filedialog to get the mp4 file
            title="Please select an mp4 file to play",      #message to user seen in title of filedialog once opened
            filetypes=(("MP4 files", "*.mp4"),)             #specify that only mp4 files should be selected
        )
        while not vidPath:
            print("no video selected!")
            retry = messagebox.askretrycancel("Missing video", message="You must select a video before continuing")
            if retry:
                vidPath = filedialog.askopenfilename(              
                title="Please select an mp4 file to play",      
                filetypes=(("MP4 files", "*.mp4"),)            
                )
            else:
                return     #way for user to exit the app
        print("Video path: " + vidPath)         #check the path in console
        #prompt user for credentials
    else:
        video = get_yt_video(url.get())
        if(video != -1):
            vidPath = video
            print(vidPath)
            #prompt user for credentials
            get_credentials()
            if(url.get() != ""):
                    os.remove(vidPath)
        else:
            vidPath = filedialog.askopenfilename(               #open the filedialog to get the mp4 file
                title="Please select an mp4 file to play",      #message to user seen in title of filedialog once opened
                filetypes=(("MP4 files", "*.mp4"),)             #specify that only mp4 files should be selected
            )
            retry = messagebox.askretrycancel("Missing video", message="You must select a video before continuing")
            while not vidPath:
                print("no video selected!")
                retry = messagebox.askretrycancel("Missing video", message="You must select a video before continuing")
                if retry:
                    vidPath = filedialog.askopenfilename(              
                    title="Please select an mp4 file to play",      
                    filetypes=(("MP4 files", "*.mp4"),)            
                    )
                else:
                    return     #way for user to exit the app
            print("Video path: " + vidPath)         #check the path in console
            get_credentials()


vidPath = ""    ##video path to be stored here afterword
labl = Label(window, anchor=CENTER, text='Enter youtube link below (leave blank if slecting local file). Video name cannot contain special characters like \ / : * ? " < > |')
labl.pack(padx=10,pady=100)
url = Entry(window, justify=CENTER , textvariable = url, width=40)
url.pack(padx=10)
contin = Button(window, anchor=CENTER, text='Continue', command=vlc_player)  #spawn another window, can use in future to access next video

contin.pack(padx=100,pady=100)

window.mainloop() #place window on computer screen, listens for events