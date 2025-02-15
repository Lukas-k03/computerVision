import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

def boxFilter(image,dimension):
   return 
WINDOWNAME = "Assignment 2 App"

imageLeft = cv2.imread('Assignment2/dog.bmp')
imageRight = cv2.imread('Assignment2/bicycle.bmp')


# Get dimensions
heightL, widthL, _ = imageLeft.shape
heightR, widthR, _ = imageRight.shape

# Resize imageRight to match the height of imageLeft
imageRight = cv2.resize(imageRight, (int(widthR * (heightL / heightR)), heightL))

stack = np.hstack((imageLeft,imageRight))

cv2.imshow(WINDOWNAME, stack)

root = tk.Tk()
root.title("Options Window")

# Create a dropdown menu for filter dimension
combo = ttk.Combobox(root, values=[3, 5])
combo.set(5)  # default value
combo.bind("<<ComboboxSelected>>", )#update_filter)
combo.pack(padx=10, pady=10)

# Create a button to close the application
close_button = tk.Button(root, text="Close", command=root.quit)
close_button.pack(pady=10)


cv2.waitKey(0)
cv2.destroyAllWindows()
