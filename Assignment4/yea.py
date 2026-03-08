import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Convert from OpenCV BGR to Tkinter-compatible image
def ConvertCV2ToTKINTER(image, max_width=None, max_height=None):
    h, w = image.shape[:2]
    if max_width and w > max_width:
        scale = max_width / w
        w = int(w * scale)
        h = int(h * scale)
    if max_height and h > max_height:
        scale = max_height / h
        w = int(w * scale)
        h = int(h * scale)
    image = cv2.resize(image, (w, h))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return ImageTk.PhotoImage(Image.fromarray(image_rgb))

# Convert from Tkinter image to OpenCV format
def ConvertTKINTERtoCV2(image):
    image = ImageTk.getimage(image)
    imageNP = np.array(image)
    return cv2.cvtColor(imageNP, cv2.COLOR_RGB2BGR)

def applySift():
    img1 = ConvertTKINTERtoCV2(imageLeft.image)
    img2 = ConvertTKINTERtoCV2(imageBottom.image)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)

    img1Extrema = img1.copy()
    for kp in kp1:
        x, y = kp.pt
        cv2.circle(img1Extrema, (int(x), int(y)), 4, (0, 0, 255), 2)
    photoRight = ConvertCV2ToTKINTER(img1Extrema, max_width=350, max_height=200)
    imageRight.config(image=photoRight)
    imageRight.image = photoRight

    img1Orientation = img1.copy()
    for kp in kp1:
        x, y = kp.pt
        angle = np.deg2rad(kp.angle)
        length = kp.size / 2
        x2 = int(x + length * np.cos(angle))
        y2 = int(y + length * np.sin(angle))
        cv2.arrowedLine(img1Orientation, (int(x), int(y)), (x2, y2), (0, 255, 0), 1, tipLength=0.3)
    photoRightMiddle = ConvertCV2ToTKINTER(img1Orientation, max_width=350, max_height=200)
    imageRightMiddle.config(image=photoRightMiddle)
    imageRightMiddle.image = photoRightMiddle

    img1KeypointsScaled = img1.copy()
    for kp in kp1:
        x, y = kp.pt
        size = int(kp.size)
        cv2.circle(img1KeypointsScaled, (int(x), int(y)), size // 2, (0, 255, 255), 2)
    photoLeftMiddle = ConvertCV2ToTKINTER(img1KeypointsScaled, max_width=350, max_height=200)
    imageLeftMiddle.config(image=photoLeftMiddle)
    imageLeftMiddle.image = photoLeftMiddle

    kp2, des2 = sift.detectAndCompute(img2, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    photo3 = ConvertCV2ToTKINTER(img3, max_width=700)
    imageBottom.config(image=photo3)
    imageBottom.image = photo3

def changePIC():
    currentCombo = combo.get()
    if currentCombo == "testImage1":
        image = cv2.imread('Assignment4/gingerTest1.jpeg')
    elif currentCombo == "testImage2":
        image = cv2.imread('Assignment4/gingerTest2.png')
    elif currentCombo == "testImage3":
        image = cv2.imread('Assignment4/gingerTest3.jpeg')
    else:
        return

    photo = ConvertCV2ToTKINTER(image, max_width=700)
    imageBottom.config(image=photo)
    imageBottom.image = photo

# ==== MAIN TKINTER UI ====
root = tk.Tk()
root.title("SIFT Keypoint Viewer")
root.geometry("800x600")

# Load images
imageRef = cv2.imread('Assignment4/gingerRef.jpeg')
imageTest = cv2.imread('Assignment4/gingerTest1.jpeg')
photoRef = ConvertCV2ToTKINTER(imageRef, max_width=350, max_height=200)
photoTest = ConvertCV2ToTKINTER(imageTest, max_width=700)

# Frames
topFrame = tk.Frame(root)
topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

middleFrame = tk.Frame(root)
middleFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

controlsFrame = tk.Frame(root)
controlsFrame.pack(side=tk.BOTTOM, fill=tk.X)

# Top row (extrema + reference)
imageLeft = tk.Label(topFrame, image=photoRef)
imageLeft.pack(side=tk.LEFT, expand=True)
imageRight = tk.Label(topFrame, image=photoRef)
imageRight.pack(side=tk.LEFT, expand=True)

# Middle row (arrows + keypoint size)
imageLeftMiddle = tk.Label(middleFrame, image=photoRef)
imageLeftMiddle.pack(side=tk.LEFT, expand=True)
imageRightMiddle = tk.Label(middleFrame, image=photoRef)
imageRightMiddle.pack(side=tk.LEFT, expand=True)

# Controls
combo = ttk.Combobox(controlsFrame, values=["testImage1", "testImage2", "testImage3"], state="readonly")
combo.set("testImage1")
combo.pack(side=tk.LEFT, padx=10, pady=5)
combo.bind("<<ComboboxSelected>>", lambda event: changePIC())

applyButton = tk.Button(controlsFrame, text="Apply", command=applySift)
applyButton.pack(side=tk.LEFT, padx=10, pady=5)

resetButton = tk.Button(controlsFrame, text="Reset", command=changePIC)
resetButton.pack(side=tk.LEFT, padx=10, pady=5)

closeButton = tk.Button(controlsFrame, text="Close", command=root.quit)
closeButton.pack(side=tk.LEFT, padx=10, pady=5)

# Bottom image in a new window
bottomWindow = tk.Toplevel(root)
bottomWindow.title("Matches View")
imageBottom = tk.Label(bottomWindow, image=photoTest)
imageBottom.pack(fill=tk.BOTH, expand=True)

# Save initial images
imageLeft.image = photoRef
imageRight.image = photoRef
imageLeftMiddle.image = photoRef
imageRightMiddle.image = photoRef
imageBottom.image = photoTest

# Run
root.mainloop()