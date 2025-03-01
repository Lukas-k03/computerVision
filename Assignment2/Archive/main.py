import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def sobelFilterXManual(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    # Create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)
    # Get image dimensions
    height, width, channels = imageNP.shape
    
    if dimension == 3:
        kernelx =  np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    elif dimension == 5:
        kernelx =  np.array([[-2, -1, 0, 1, 2],
                             [-3, -2, 0, 2, 3],
                             [-4, -3, 0, 3, 4],
                             [-3, -2, 0, 2, 3],
                             [-2, -1, 0, 1, 2]])

    # Compute the padding size
    pad = dimension // 2

    #pad the image to when we are on the corners it dosent turn up an error for it having no data
    paddedImage = cv2.copyMakeBorder(imageNP, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    #box filter summation
    for y in range(height):
        for x in range(width):
            #channels repersent each color so we can go color by color (3)
            for c in range(channels):
                #get kernel window for average Y:Y gets from the current pixel to the kernel size
                window = paddedImage[y:y + dimension, x:x + dimension, c]
                #compute the mean value for the pixel by using sum of the window with the kernel
                filteredImage[y, x, c] = np.sum(window * kernelx)

    #convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filteredImage)

    #convert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)

    #update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

def sobelFilterYManual(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    # Create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)
    # Get image dimensions
    height, width, channels = imageNP.shape
    
    if dimension == 3:
        kernelY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    elif dimension == 5:
        kernelY = np.array([[-2, -3, -4, -3, -2],
                            [-1, -2, -3, -2, -1],
                            [ 0,  0,  0,  0,  0],
                            [ 1,  2,  3,  2,  1],
                            [ 2,  3,  4,  3,  2]])

    # Compute the padding size
    pad = dimension // 2

    #pad the image to when we are on the corners it dosent turn up an error for it having no data
    paddedImage = cv2.copyMakeBorder(imageNP, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    #box filter summation
    for y in range(height):
        for x in range(width):
            #channels repersent each color so we can go color by color (3)
            for c in range(channels):
                #get kernel window for average Y:Y gets from the current pixel to the kernel size
                window = paddedImage[y:y + dimension, x:x + dimension, c]
                # Compute the mean value for the pixel by using sum of the window with the kernel
                filteredImage[y, x, c] = np.sum(window * kernelY)

    #Convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filteredImage)

    # Convert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)

    # Update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

def sobelFilterY(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    # Create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)
    
    # Apply box filter
    filteredImage = cv2.Sobel(imageNP, cv2.CV_64F, dx=0, dy=1, ksize=dimension)

    # Convert back to uint8 before cvtColor
    filteredImage = cv2.convertScaleAbs(filteredImage)

    # Convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filteredImage)

    # Convert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)

    # Update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

def sobelFilterX(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    #create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)
    
    #apply box filter
    filteredImage = cv2.Sobel(imageNP, cv2.CV_64F, dx=1, dy=0, ksize=dimension)

    #convert back to uint8 before cvtColor so that we can modify it
    filteredImage = cv2.convertScaleAbs(filteredImage)
    #convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)
    filtered_pil = Image.fromarray(filteredImage)
    #convert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)
    #update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

def sobelFilterXYManual(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    elif dimension == '3x3':
        dimension = 3
    
    #convert TKinter image to PIL
    image = ImageTk.getimage(image)
    #convert to NumPy array
    imageNP = np.array(image)
    #convert color to BGR (OpenCV format)
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    #create an empty image for storing filtered results
    filteredImage = np.zeros_like(imageNP, dtype=np.float64)
    height, width, channels = imageNP.shape

    #define Sobel X and Y kernels
    if dimension == 3:
        kernelX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        kernelY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    elif dimension == 5:
        kernelX = np.array([[-2, -1, 0, 1, 2],
                            [-3, -2, 0, 2, 3],
                            [-4, -3, 0, 3, 4],
                            [-3, -2, 0, 2, 3],
                            [-2, -1, 0, 1, 2]])
        
        kernelY = np.array([[-2, -3, -4, -3, -2],
                            [-1, -2, -3, -2, -1],
                            [ 0,  0,  0,  0,  0],
                            [ 1,  2,  3,  2,  1],
                            [ 2,  3,  4,  3,  2]])

    #compute padding size
    pad = dimension // 2

    #pad the image to handle edge cases
    paddedImage = cv2.copyMakeBorder(imageNP, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    #Apply Sobel filter in X and Y directions
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                window = paddedImage[y:y + dimension, x:x + dimension, c]
                Gx = np.sum(window * kernelX)
                Gy = np.sum(window * kernelY)
                #Compute gradient magnitude
                filteredImage[y, x, c] = np.sqrt(Gx**2 + Gy**2)

     #convert back to uint8 before cvtColor so that we can modify it
    filteredImage = cv2.convertScaleAbs(filteredImage)

    #convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)
    #convert to Tkinter-compatible image
    filtered_pil = Image.fromarray(filteredImage)
    filteredTK = ImageTk.PhotoImage(filtered_pil)
    #update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

def sobelFilterXY(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    #create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)
    
    #apply box filter
    filteredImage = cv2.Sobel(imageNP, cv2.CV_64F, dx=1, dy=1, ksize=dimension)

    #convert back to uint8 before cvtColor so that we can modify it
    filteredImage = cv2.convertScaleAbs(filteredImage)

    #convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filteredImage)
    #xonvert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)
    #update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

def guassianFilter(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    #create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)
    
    #apply box filter
    filteredImage = cv2.GaussianBlur(imageNP, (dimension, dimension), 0)

    #convert back to uint8 before cvtColor so that we can modify it
    filteredImage = cv2.convertScaleAbs(filteredImage)

    #convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filteredImage)
    #convert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)
    #update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return

# Function to apply box filter (this is just a placeholder for now)
def boxFilter(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #convert to numpy array
    imageNP = np.array(image)
    #convert color
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    #apply box filter
    filteredImage = cv2.boxFilter(imageNP, -1, (dimension, dimension))

    #convert back to RGB format for Tkinter
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)

    filtered_pil = Image.fromarray(filteredImage)
    #xonvert to Tkinter-compatible image
    filteredTK = ImageTk.PhotoImage(filtered_pil)
    #update the label widget
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK
    
    return 


def boxFilterManual(image):
    dimension = combo.get()

    if dimension == '5x5':
        dimension = 5
    if dimension == '3x3':
        dimension = 3
    
    #convert TKimage to a PIL Image
    image = ImageTk.getimage(image)
    #xonvert to numpy array
    imageNP = np.array(image)
    #convert color backl
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

    #get image dimensions
    height, width, channels = imageNP.shape

    #create an empty image to store the filtered result
    filteredImage = np.zeros_like(imageNP, dtype=np.uint8)

    #define the kernel (each element is 1 / (kernel_size * kernel_size))
    kernel = np.ones((dimension, dimension), dtype=np.float32) / (dimension * dimension)

    #compute the padding size
    pad = dimension // 2

    #pad the image to when we are on the corners it dosent turn up an error for it having no data
    paddedImage = cv2.copyMakeBorder(imageNP, pad, pad, pad, pad, cv2.BORDER_REFLECT)

    #box filter summation
    for y in range(height):
        for x in range(width):
            #channels repersent each color so we can go color by color (3)
            for c in range(channels):
                #get kernel window for average Y:Y gets from the current pixel to the kernel size
                window = paddedImage[y:y + dimension, x:x + dimension, c]
                # Compute the mean value for the pixel by using sum of the window with the kernel
                filteredImage[y, x, c] = np.sum(window * kernel)

    #convert to Tkinter-compatible image
    filteredImage = cv2.cvtColor(filteredImage, cv2.COLOR_BGR2RGB)
    filteredTK = ImageTk.PhotoImage(Image.fromarray(filteredImage))
    #update image
    imageBottom.config(image=filteredTK)
    imageBottom.image = filteredTK

    return


def reset():
    imageLeft = cv2.imread('Assignment2/dog.bmp')
    imageRight = cv2.imread('Assignment2/bicycle.bmp')
    heightL, widthL, _ = imageLeft.shape
    heightR, widthR, _ = imageRight.shape

    #resize hieght of right image
    imageRight = cv2.resize(imageRight, (int(widthR * (heightL / heightR)), heightL))

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
imageTop.pack(padx=10)
imageBottom = tk.Label(root, image=photo2)
imageBottom.pack(padx=10)

#filter functoin
def applyFilter():
    selectedFilter = filterCombo.get()
    if selectedFilter == "Box Filter (Manual)":
        boxFilterManual(photo2)
    elif selectedFilter == "Box Filter":
        boxFilter(photo2)
    elif selectedFilter == "Sobel X Filter (Manual)":
        sobelFilterXManual(photo2)
    elif selectedFilter == "Sobel Y Filter (Manual)":
        sobelFilterYManual(photo2)
    elif selectedFilter == "Sobel X Filter":
        sobelFilterX(photo2)
    elif selectedFilter == "Sobel Y Filter":
        sobelFilterY(photo2)
    elif selectedFilter == "Sobel XY Filter (Manual)":
        sobelFilterXYManual(photo2)
    elif selectedFilter == "Sobel XY Filter":
        sobelFilterXY(photo2)
    elif selectedFilter == "Guassian Filter":
        guassianFilter(photo2)

#create a dropdown menu for filter selection
filterCombo = ttk.Combobox(root, values=[
    "Box Filter (Manual)",
    "Box Filter",
    "Sobel X Filter (Manual)",
    "Sobel Y Filter (Manual)",
    "Sobel X Filter",
    "Sobel Y Filter",
    "Sobel XY Filter (Manual)",
    "Sobel XY Filter",
    "Guassian Filter"
], state="readonly")

filterCombo.set("Box Filter")
filterCombo.pack(side=tk.LEFT, pady=10)

#dropdown for filter dimension
combo = ttk.Combobox(root, values=['3x3', '5x5'], state="readonly")
combo.set('3x3')  # default value
combo.pack(side = tk.LEFT,pady=10)

#Apply button
applyButton = tk.Button(root, text="Apply", command=applyFilter)
applyButton.pack(side=tk.LEFT, pady=10)

#Buttons
closeButton = tk.Button(root, text="Close", command=root.quit)
closeButton.pack(side = tk.LEFT, pady=10)
resetButton = tk.Button(root, text="Reset", command=reset)
resetButton.pack(side = tk.LEFT, pady=10)
# Run the Tkinter window
root.mainloop()
