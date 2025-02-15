import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Function to apply box filter (this is just a placeholder for now)
def boxFilter(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #Convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    # Convert to numpy array
    image_np = np.array(image)
    #convert color backl
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Apply box filter
    filtered_image = cv2.boxFilter(image_np, -1, (dimension, dimension))

    # Convert back to RGB format for Tkinter
    filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filtered_image)

    # Convert to Tkinter-compatible image
    filtered_tk = ImageTk.PhotoImage(filtered_pil)

    # Update the label widget
    imageBottom.config(image=filtered_tk)
    imageBottom.image = filtered_tk
    
    return 


def boxFilterManual(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #Convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    # Convert to numpy array
    image_np = np.array(image)
    #convert color backl
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Get image dimensions
    height, width, channels = image_np.shape

    # Create an empty image to store the filtered result
    filtered_image = np.zeros_like(image_np, dtype=np.uint8)

    # Define the kernel (each element is 1 / (kernel_size * kernel_size))
    kernel = np.ones((dimension, dimension), dtype=np.float32) / (dimension * dimension)

    # Compute the padding size
    pad = dimension // 2

    # Pad the image with reflection padding
    padded_image = cv2.copyMakeBorder(image_np, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    #Apply the filter manually
    for y in range(height):
        for x in range(width):
            #channels repersent each color so we can go color by color (3)
            for c in range(channels):
                # Extract kernel window
                window = padded_image[y:y + dimension, x:x + dimension, c]
                # Compute the mean value using element-wise multiplication and sum
                filtered_image[y, x, c] = np.sum(window * kernel)

    #convert to Tkinter-compatible image
    filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
    filtered_tk = ImageTk.PhotoImage(Image.fromarray(filtered_image))
    #update image
    imageBottom.config(image=filtered_tk)
    imageBottom.image = filtered_tk

    return


def reset():
    # Load images
    imageLeft = cv2.imread('Assignment2/dog.bmp')
    imageRight = cv2.imread('Assignment2/bicycle.bmp')

    # Get dimensions
    heightL, widthL, _ = imageLeft.shape
    heightR, widthR, _ = imageRight.shape

    # Resize imageRight to match the height of imageLeft
    imageRight = cv2.resize(imageRight, (int(widthR * (heightL / heightR)), heightL))

    # Stack images horizontally
    stack1 = np.hstack((imageLeft, imageRight))
    stack2 = np.hstack((imageLeft, imageRight))

    #Convert OpenCV image (BGR) to RGB format
    stackConvert1 = cv2.cvtColor(stack1, cv2.COLOR_BGR2RGB)
    stackConvert2 = cv2.cvtColor(stack2, cv2.COLOR_BGR2RGB)

    # Convert the initial image to a format suitable for Tkinter after the root window is created
    photo1 = ImageTk.PhotoImage(Image.fromarray(stackConvert1))
    photo2 = ImageTk.PhotoImage(Image.fromarray(stackConvert2))

    # Update the image label
    imageTop.config(image=photo1)
    imageBottom.config(image=photo2)

    #keeps image refernec so scope dosent destroy it
    imageBottom.image = photo2
    imageTop.image = photo1

    return

# Load images
imageLeft = cv2.imread('Assignment2/dog.bmp')
imageRight = cv2.imread('Assignment2/bicycle.bmp')

# Get dimensions
heightL, widthL, _ = imageLeft.shape
heightR, widthR, _ = imageRight.shape

# Resize imageRight to match the height of imageLeft
imageRight = cv2.resize(imageRight, (int(widthR * (heightL / heightR)), heightL))

# Stack images horizontally
stack1 = np.hstack((imageLeft, imageRight))
stack2 = np.hstack((imageLeft, imageRight))

#Convert OpenCV image (BGR) to RGB format
stackConvert1 = cv2.cvtColor(stack1, cv2.COLOR_BGR2RGB)
stackConvert2 = cv2.cvtColor(stack2, cv2.COLOR_BGR2RGB)

# Create Tkinter window
root = tk.Tk()
root.title("Assignment 2 App")
    
# Convert the initial image to a format suitable for Tkinter after the root window is created
photo1 = ImageTk.PhotoImage(Image.fromarray(stackConvert1))
photo2 = ImageTk.PhotoImage(Image.fromarray(stackConvert2))

# Label to display image
imageTop = tk.Label(root, image=photo1)
imageTop.pack(padx=10, pady=10)
imageBottom = tk.Label(root, image=photo2)
imageBottom.pack(padx=10, pady=10)

# Dropdown for filter dimension
combo = ttk.Combobox(root, values=['3x3', '5x5'], state="readonly")
combo.set('5x5')  # default value
combo.pack(side = tk.LEFT,pady=10)

# Close button
closeButton = tk.Button(root, text="Close", command=root.quit)
closeButton.pack(side = tk.LEFT, pady=10)
resetButton = tk.Button(root, text="Reset", command=reset)
resetButton.pack(side = tk.LEFT, pady=10)
BoxMfilterButton = tk.Button(root, text="Box Filter (Manual)", command=lambda:boxFilterManual(photo2))
BoxMfilterButton.pack(side = tk.LEFT, pady=10)
BoxfilterButton = tk.Button(root, text="Box Filter", command=lambda:boxFilter(photo2))
BoxfilterButton.pack(side = tk.LEFT, pady=10)

# Run the Tkinter window
root.mainloop()
