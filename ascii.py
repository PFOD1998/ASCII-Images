# -*- coding: utf-8 -*-
"""
Created on Mon May 13 19:23:55 2019

Ascii Art Code
Basic console interface which takes input image, and desired output width
Returns a text document with an ASCII representation of the original image

@author: Peter O'Donoghue
"""
from PIL import Image

def brightness(r,g,b):
    """
    Takes R,G,B value and converts it to a brightness value
    """
    return round(0.33*r + 0.5*g + 0.16*b, 2)

def getChar(brightness):
    """
    Takes in a brightness value and returns it's corresponding ASCII character
    """
    chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    thisChar = chars[int(brightness//3.95)]
    return thisChar

def main():
    print("--- JPEG to ASCII converter ---\n")
    loop = True
    while loop:
        # Read in the image from the user
        try:
            path = input("Please enter name/path of jpeg image to be converted:\n")
            pic = Image.open(path)
            if "jpg" in path or "jpeg" in path:
                loop = False
            else:
                print("Incorrect image format. Try again.")
        except IOError:
            loop = True
            print("Error with file name! Try again.")
    loop = True
    while loop:
        # Read in the intended output width from user
        try:
            new_w = int(input("How many characters wide do you want your image?\n")) // 3
            loop = False
            width, height = pic.size
            new_h = round((height/width) * new_w)
            pic = pic.resize((new_w, new_h))
            
        except TypeError:
            loop = True
            print("Please enter an integer.")
    
    
    
    width, height = pic.size
    
    # Get the pixel by pixel representation of the image
    pixels = pic.load()
    result = ""
    # Store the character corresponding to each pixel
    for i in range(height):
        for j in range(width):
            r,g,b = pixels[j,i]
            char = getChar(brightness(r,g,b))
            result += char*3
        result += "\n"
    
    # Write result to the output file
    path += ".txt"
    file = open(path, "w")
    file.write(result)
    file.close()
            
        
if __name__ == "__main__":
    main()