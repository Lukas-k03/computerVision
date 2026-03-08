import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def resizeImageToMatchWidth(tk_image, reference_cv_image):
    cv_image = ConvertTKINTERtoCV2(tk_image)
    target_width = 2 * reference_cv_image.shape[1]
    h, w = cv_image.shape[:2]
    aspect_ratio = h / w
    target_height = int(target_width * aspect_ratio)
    resized = cv2.resize(cv_image, (target_width, target_height))
    return ConvertCV2ToTKINTER(resized)

def ConvertCV2ToTKINTER(image):
    stackConvert = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(stackConvert))
    return photo

def ConvertTKINTERtoCV2(image):
    image = ImageTk.getimage(image)
    imageNP = np.array(image)
    imageNP = cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)
    return imageNP

def applySift():
    img1 = ConvertTKINTERtoCV2(imageLeft.image)
    img2 = ConvertTKINTERtoCV2(imageBottom.image)
    
    sift = cv2.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    
    print(des1)

    img1Extrema = img1.copy()

    for kp in kp1:
        x, y = kp.pt
        cv2.circle(img1Extrema, (int(x), int(y)), 2, (0, 0, 255), 2)
    imageRightPhoto = ConvertCV2ToTKINTER(img1Extrema)
    imageRight.config(image=imageRightPhoto)
    imageRight.image = imageRightPhoto  # Preserve reference

    img1Orientation = img1.copy()
    for kp in kp1:
        x, y = kp.pt
        angle = np.deg2rad(kp.angle)
        length = kp.size / 2
        x2 = int(x + length * np.cos(angle))
        y2 = int(y + length * np.sin(angle))
        cv2.arrowedLine(img1Orientation, (int(x), int(y)), (x2, y2), (0, 255, 0), 1, tipLength=0.3)

    imageRightMiddlePhoto = ConvertCV2ToTKINTER(img1Orientation)
    imageRightMiddle.config(image=imageRightMiddlePhoto)
    imageRightMiddle.image = imageRightMiddlePhoto 

    img1KeypointsScaled = img1.copy()
    for kp in kp1:
        x, y = kp.pt
        size = int(kp.size) 
        cv2.circle(img1KeypointsScaled, (int(x), int(y)), size, (0, 255, 255), 2)

    imageLeftMiddlePhoto = ConvertCV2ToTKINTER(img1KeypointsScaled)
    imageLeftMiddle.config(image=imageLeftMiddlePhoto)
    imageLeftMiddle.image = imageLeftMiddlePhoto

    kp2, des2 = sift.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    photo3 = ConvertCV2ToTKINTER(img3)

    imageBottom.config(image=photo3)
    imageBottom.image = photo3
    return

def changePIC():
    currentCombo = combo.get()

    if currentCombo == "testImage1":
        image3 = cv2.imread('Assignment4/testImage1.jpeg')
    if currentCombo == "testImage2":
        image3 = cv2.imread('Assignment4/testImage2.jpeg')
    if currentCombo == "testImage3":
        image3 = cv2.imread('Assignment4/testImage3.jpeg')

    photo3 = ConvertCV2ToTKINTER(image3)
    photo3 = resizeImageToMatchWidth(photo3,imageT)

    imageBottom.config(image=photo3)
    imageBottom.image = photo3

# MAINNNN

#create tkinter window
root = tk.Tk()
root.title("Assignment 4 App")

imageT = cv2.imread('Assignment4/image1.png')
image3 = cv2.imread('Assignment4/testImage1.jpeg')
photo1 = ConvertCV2ToTKINTER(imageT)
photo3 = ConvertCV2ToTKINTER(image3)

photo3 = resizeImageToMatchWidth(photo3,imageT)


topFrame = tk.Frame(root)
topFrame.pack(side=tk.TOP)

middleFrame = tk.Frame(root)
middleFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(root)
bottomFrame.pack(side=tk.TOP, fill=tk.BOTH)

imageLeft = tk.Label(topFrame, image=photo1)
imageLeft.pack(side=tk.LEFT,fill=tk.BOTH)
imageRight = tk.Label(topFrame, image=photo1)
imageRight.pack(side=tk.LEFT,fill=tk.BOTH)

imageBottom = tk.Label(bottomFrame, image=photo3)
imageBottom.pack(fill=tk.BOTH, expand=True)

imageLeftMiddle = tk.Label(middleFrame, image=photo1)
imageLeftMiddle.pack(side=tk.LEFT, fill=tk.BOTH) 
imageRightMiddle = tk.Label(middleFrame, image=photo1)
imageRightMiddle.pack(side=tk.LEFT, fill=tk.BOTH)
imageRight.image = photo1
imageLeft.image = photo1
imageBottom.image = photo3
imageLeftMiddle.image = photo1
imageRightMiddle.image = photo1

combo = ttk.Combobox(root, values=['testImage1', 'testImage2' ,'testImage3'], state="readonly")
combo.set('testImage1')
combo.pack(side = tk.LEFT,pady=10)
combo.bind("<<ComboboxSelected>>", lambda event: changePIC())

applyButton = tk.Button(root, text="Apply", command=applySift)
applyButton.pack(side=tk.LEFT, pady=10)
resetButton = tk.Button(root, text="Reset", command=changePIC)
resetButton.pack(side = tk.LEFT, pady=10)
closeButton = tk.Button(root, text="Close", command=root.quit)
closeButton.pack(side = tk.LEFT, pady=10)

#run the Tkinter window
root.mainloop()
