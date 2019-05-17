# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:09:56 2019

@author: Peter
"""

import cv2
from tkinter import *
import numpy as np

def brightness(r,g,b):
    """
    Takes R,G,B value and converts it to a brightness value
    """
    return round(0.33*r + 0.5*g + 0.16*b, 2)

def getChar(brightness):
    """
    Takes in a brightness value and returns it's corresponding ASCII character
    """
    # Map of chars based off brightness
    chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    thisChar = chars[int(brightness//3.95)] # 64 -
    return thisChar

def onStart():
    """
    Converts frame of the webcam stream to ASCII chars
    Updates the label in the interface to display the ASCII image    
    Calls itself to get the next frame
    """
    # Capture current frame
    ret, frame = cap.read()

    # Handles the mirroring of the current frame
    frame = cv2.flip(frame,1)

    # Get the frame info
    height, width, colors = frame.shape

    # Initialise variable for the output
    result = ""
    # Store the character corresponding to each pixel
    for i in range(0,height,2):
        for j in range(0,width,2):
            b,g,r = frame.item(i,j,0), frame.item(i,j,1), frame.item(i,j,2)
            char = getChar(brightness(r,g,b))
            result += char*2
        result += "\n"
    final = result
    # Update the text in the interface
    label["text"] = result
    # Call for the next frame
    root.after(30, onStart)
    
    
# Set up connection to the webcam
cap = cv2.VideoCapture(0)

# Set up the interface
root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth()-50, root.winfo_screenheight()-50))
label = Label(root, text="")
# Small font needed for displaying characters as image
label.config(font=("Courier", 2))
label.place(x=10,y=10,anchor="nw")

# Call function to start the webcam to ascii stream
onStart()

root.mainloop()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()