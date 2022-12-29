from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils


##### Create GUI #####

root = Tk()

#Buttons
btnStart =  Button(root, text="Start", width=45)
btnStart.grid(column=0, row=0, padx=5, pady=5)

btnEnd =  Button(root, text="End", width=45)
btnEnd.grid(column=1, row=0, padx=5, pady=5)

#Video place holder
lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=2)

root.mainloop()