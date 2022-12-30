from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils

def visualize():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            
            phVideo.configure(image=img)
            phVideo.image = img
            phVideo.after(10,visualize)
        else:
            phVideo.image = ""
            cap.release()

def start_video():
    global cap
    cap = cv2.VideoCapture(0)
    visualize()
    
def end_video():
    global cap
    cap.release()
    
cap = None

#Create GUI
root = Tk()
root.title("Nevado 2.0")

##### Buttons #####

btnStart = Button(root, text="Start", width=45, command=start_video)
btnStart.grid(column=0, row=0, padx=5, pady=5)


btnEnd = Button(root, text="End", width=45, command=end_video)
btnEnd.grid(column=1, row=0, padx=5, pady=5)
#####

##### Video Place Holder #####

phVideo = Label(root)
phVideo.grid(column=0, row=1, columnspan=2)

root.mainloop()
