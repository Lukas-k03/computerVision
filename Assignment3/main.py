import cv2
import numpy as np
import matplotlib as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#from skimage import util for image_as_ubyte and mutil thresehold otsu
from skimage import util   
from skimage.filters import threshold_multiotsu

def ConvertCV2ToTKINTER(image):
    stackConvert = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(stackConvert))
    return photo

def ConverTKINTERtoCV2(image):
    image = ImageTk.getimage(image)
    imageNP = np.array(image)
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)
    return imageNP

def otsu2Classes(image):
    
    imageNP = ConverTKINTERtoCV2(image)
    gray = cv2.cvtColor(imageNP, cv2.COLOR_BGR2GRAY)

    #this function automatically applies and calculates the threshold using cv2 methods
    #the threeshold variable stores the actual value of the threshold
    threshold, filteredImage = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #convert back to CV2
    filteredImage = ConvertCV2ToTKINTER(filteredImage)

    #update display and image
    imageBottom.config(image=filteredImage)
    imageBottom.image = filteredImage

    return

def otsuManyClasses(image):

    imageNP = ConverTKINTERtoCV2(image)
    
    #make image gray
    gray = cv2.cvtColor(imageNP, cv2.COLOR_BGR2GRAY)

    #we can change the class count here
    classes = int(classCombo.get())

    #qpply Multi-Otsu Thresholding
    thresholds = threshold_multiotsu(gray, classes=classes)

    #assign labels to different regions
    regions = np.digitize(gray, bins=thresholds)

    #convert regions fomr 64 bit to 8 bit for tkinter
    regions = util.img_as_ubyte(regions)

    #generate a colormap based on matplots preset tab10 colorset, so the colors are always distincly different
    #than normalize those color values to scale to grey scale
    colormap = np.array([plt.cm.get_cmap("tab10")(i)[:3] for i in range(classes)]) * 255
    
    #empty image to cast colors to
    color = np.zeros((*gray.shape, 3), dtype=np.uint8)

    #apply colors to each of the regions in the range
    for i in range(classes):
        color[regions == i] = colormap[i]

    #convert back to Tkinter format
    filteredImage = ConvertCV2ToTKINTER(color)

    #update the Tkinter image label
    imageBottom.config(image=filteredImage)

    #keep image reference
    imageBottom.image = filteredImage

    return

def meanShift(image):
    imageNP = ConverTKINTERtoCV2(image)

    """
    sp: Spatial window radius (controls window size).
    sr: Color range radius (controls how similar colors are grouped)
    this line applies meanshift method with the specified permatetors abve
    """
    segmented = cv2.pyrMeanShiftFiltering(imageNP, sp=3, sr=40)

    #update image
    filteredImage = ConvertCV2ToTKINTER(segmented)
    imageBottom.config(image=filteredImage)
    imageBottom.image = filteredImage
    return

def updateGUI():
    #this function is to add the classes slection box if using otsu many classes
    selectedFilter = filterCombo.get()
    if selectedFilter == "Otsu Method (Many Classes)":
        classCombo.pack(side=tk.LEFT, pady=10)
    else:
        classCombo.pack_forget() 
    return

#filter functoin
def applyFilter():
    selectedFilter = filterCombo.get()
    if selectedFilter == "Otsu Method (2 Classes)":
        otsu2Classes(imageBottom.image)
    elif selectedFilter == "Otsu Method (Many Classes)":
        otsuManyClasses(imageBottom.image)
    elif selectedFilter == "Mean Shift Method":
        meanShift(imageBottom.image)

def changePIC():

    currentCombo = combo.get()

    if currentCombo == "Image1":
        image1 = cv2.imread('Assignment3/Image1.png')
        image2 = image1.copy()
    if currentCombo == "Image2":
        image1 = cv2.imread('Assignment3/Image2.png')
        image2 = image1.copy()
    if currentCombo == "Image3":
        image1 = cv2.imread('Assignment3/Image3.png')
        image2 = image1.copy()
    
    photo1 = ConvertCV2ToTKINTER(image1)
    photo2 = ConvertCV2ToTKINTER(image2)

    # Update the image label
    imageTop.config(image=photo1)
    imageBottom.config(image=photo2)

    #keeps image refernec so scope dosent destroy it
    imageTop.image = photo1
    imageBottom.image = photo2

# MAINNNN

#create tkinter window
root = tk.Tk()
root.title("Assignment 3 App")

imageT = imageB = cv2.imread('Assignment3/Image1.png')
photo1 = ConvertCV2ToTKINTER(imageT)
photo2 = ConvertCV2ToTKINTER(imageB)

#label to display image
imageTop = tk.Label(root, image=photo1)
imageTop.pack(padx=10)
imageBottom = tk.Label(root, image=photo2)
imageBottom.pack(padx=10)

#keeps image refernec so scope dosent destroy it
imageBottom.image = photo2
imageTop.image = photo1

#create a dropdown menu for filter selection
filterCombo = ttk.Combobox(root, values=[
    "Otsu Method (2 Classes)",
    "Otsu Method (Many Classes)",
    "Mean Shift Method"
], state="readonly")

filterCombo.set("Otsu Method (2 Classes)")
filterCombo.pack(side=tk.LEFT, pady=10)
#bind filter selection event
filterCombo.bind("<<ComboboxSelected>>", lambda event: updateGUI())

#dropdown for number of classes (Initially hidden)
classCombo = ttk.Combobox(root, values=[str(i) for i in range(3, 11)], state="readonly")
classCombo.set("3")  # Default to 3 classes

#dropdown for filter dimension
combo = ttk.Combobox(root, values=['Image1', 'Image2' ,'Image3'], state="readonly")
combo.set('Image1')
combo.pack(side = tk.LEFT,pady=10)
combo.bind("<<ComboboxSelected>>", lambda event: changePIC())


#Buttons
applyButton = tk.Button(root, text="Apply", command=applyFilter)
applyButton.pack(side=tk.LEFT, pady=10)
resetButton = tk.Button(root, text="Reset", command=changePIC)
resetButton.pack(side = tk.LEFT, pady=10)
closeButton = tk.Button(root, text="Close", command=root.quit)
closeButton.pack(side = tk.LEFT, pady=10)

#run the Tkinter window
root.mainloop()


#orignally i tried to do the otsu method on the whole image, but than i realized we need to apply the local operator to actually get regions of the image which is waht we want
#when applying the 