from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
from gpiozero import Motor
import time
import matplotlib.pyplot as plt

##### HSV Color detection parameters ####

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

##### Motor Ports and speed #####

motorX_fordward = 3
motorX_backward = 2

motorY_fordward = 14
motorY_backward = 15

speedX = 0
speedY = 0

##### Controler Parameters #####

#Kp
#Ki
#Kd

def param_init():
    global azulBajo
    global azulAlto
    global redBajo1
    global redAlto1

    global redBajo2
    global redAlto2
    
    global motorY
    global motorX
    global speedY
    global speedX
    
    
    motorX = Motor(forward=motorX_fordward, backward=motorX_backward, pwm=True)
    motorY = Motor(forward=motorY_fordward, backward=motorY_backward, pwm=True)
    motorX.stop()
    motorY.stop()
    
    speedX=0.13 #PWM signal, 0<SpeedA=Duty_Cycle<1
    speedY=0.06 #PWM signal, 0<SpeedA=Duty_Cycle<1
    
    azulBajo = np.array([100, 100, 25], np.uint8)
    azulAlto = np.array([125, 255, 255], np.uint8)
    redBajo1 = np.array([0, 100, 20], np.uint8)  #Delimiting Red Color
    redAlto1 = np.array([8, 255, 255], np.uint8)

    redBajo2 = np.array([140, 0, 47], np.uint8)
    redAlto2 = np.array([180, 240, 255], np.uint8)
        
def color_detect(frame):
    global azulBajo
    global azulAlto
    global redBajo1
    global redAlto1

    global redBajo2
    global redAlto2
    
    global motorY
    global motorX
    global speedY
    global speedX
    
    
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #RGB2HSV
    maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1) #Masks
    maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
    maskRed = cv2.add(maskRed1, maskRed2) #Adding mask
    maskBlue = cv2.inRange(frameHSV, azulBajo, azulAlto)
    contornos, _ = cv2.findContours(maskRed2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        
        if area>1000:
            
            dead_zone = [350,250,250,150]
            M=cv2.moments(c)
            if(M["m00"]==0): M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M["m01"]/M["m00"])
            x_e = x - 300
            y_e = y - 200
            
            
            frame = cv2.circle(frame,(x,y),3,(0,255,0),-1)
            frame = cv2.rectangle(frame,(dead_zone[1],dead_zone[3]),(dead_zone[0],dead_zone[2]),(125,255,255),2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            frame = cv2.putText(frame,'{},{}'.format(x_e,y_e),(x+10,y),font,0.5,(0,255,0),1,cv2.LINE_AA)
            
            if x > dead_zone[0]:
               motorX.forward(speedX)
            elif x < dead_zone[1]:
                motorX.backward(speedX)
            else:
                motorX.stop()
               
            
            if y > dead_zone[2]:
              motorY.forward(speedY)
            elif y < dead_zone[3]:
               motorY.backward(speedY)
            else:
               motorY.stop()
             
            
            c=cv2.convexHull(c)
            frame = cv2.drawContours(frame, [c], 0, (0,255,0),2)
    return frame
    

def visualize():
    global cap
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=640)
        frame = color_detect(frame)
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
    global motorX
    global motorY
    
    motorX.stop()
    motorY.stop()
    cap.release()

param_init()
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
