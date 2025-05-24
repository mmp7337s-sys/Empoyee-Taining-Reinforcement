from tkinter import *

window = Tk() ##instantiate an instance of a window
window.title("Are You Paying Attention?")   #title of window
icon = PhotoImage(file='dokk.png')      #icon in top left corner

window.iconphoto(True, icon)
window.geometry("800x600")  #screen dimensions
window.config(background="#009900") ##background color

window.mainloop() #place window on computer screen, listens for events

