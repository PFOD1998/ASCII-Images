# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:09:56 2019

@author: Peter
"""

import cv2
from tkinter import *
import numpy as np
import time

    
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
    if gui.inverted:
        thisChar = chars[64 - int(brightness//3.95)]
    else:
        thisChar = chars[int(brightness//3.95)]
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
    gui.final = result
    # Update the text in the interface
    gui.ascii["text"] = result
    
    if not gui.paused:
        # Call for the next frame
        root.after(30, onStart)
    
class myGUI():
    def __init__(self, root):
        self.root = root
        self.root.state("zoomed")
        #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth()-50, root.winfo_screenheight()-50))
        
        # Toggle variables
        self.inverted = False
        self.paused = False
        self.final = ""
        
        # Frames
        self.images = Frame(self.root).pack(side=TOP)
        self.controls = Frame(self.root).pack(side=BOTTOM)
        
        self.ascii = Label(self.images, text="")
        # Small font needed for displaying characters as image
        self.ascii.config(font=("Courier", 2), foreground="white")
        self.root.configure(background="gray")
        self.ascii.config(background="black")
        self.ascii.pack()
        #self.ascii.place(x=10,y=10,anchor="nw")
        
        #control buttons
        self.pauseText = StringVar()
        self.pauseButton = Button(self.controls, textvariable=self.pauseText, command=self.togglePause).pack()
        self.pauseText.set("Pause")
        self.saveButton = Button(self.controls, text="Save", command=self.saveFile).pack()
        self.invertButton = Button(self.controls, text="Invert", command=self.invert).pack()
        
    def invert(self):
        """
        Changes inverted variable so bright areas dark/dark areas bright
        """
        if self.inverted:
            self.inverted = False
            return
        self.inverted = True
        return
    
    def togglePause(self):
        """
        Pauses image stream or unpauses image stream
        """
        if self.paused:
            self.paused = False
            onStart()
            self.pauseText.set("Pause")
            return
        self.paused = True
        self.pauseText.set("Unpause")
        return
    
    def saveFile(self):
        """
        Saves current ASCII string into a file
        file saved in current directory with time stamp filename
        """
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file = open(timestr + ".txt","w")
        file.write(self.final)
        file.close()
    
    
# Set up connection to the webcam
cap = cv2.VideoCapture(0)

# Set up the interface
root = Tk()
gui = myGUI(root)

# Call function to start the webcam to ascii stream
onStart()

root.mainloop()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()