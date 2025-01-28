import cv2
import numpy as np

WINDOWNAME = "Assignment 1 App (press q to exit s to save)"

lastBright = None
lastConst = None
adjusted = None

def generateScaledHistogram(image):
    #convert the image to grayscale for histogram calculation
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
    #normalize the histogram to fit it in the image window
    hist = hist / hist.max()  
    
    #create a blanck histogram so we can fill it with the data
    histheight = image.shape[0]
    histwidth = 256 
    histimage = np.zeros((histheight, histwidth, 3), dtype=np.uint8)
    
    #draw
    for i in range(1, 256):
        cv2.line(histimage,(i-1, histheight - int(hist[i-1] * histheight)),(i, histheight - int(hist[i] * histheight)),(255, 255, 255), 1)
    
    #resize the histogram image to the same size as the original image
    scaled = cv2.resize(histimage, (image.shape[1], image.shape[0]))
    
    return scaled

def adjust_brightness(val):
    global lastConst
    global lastBright
    global adjusted

    lastBright = (val - 128)

    adjusted = cv2.convertScaleAbs(imageLeft, alpha= lastConst, beta = lastBright)
    stacked = np.hstack((imageLeft, adjusted))
    
    #generate scaled histograms for original and adjusted images
    histleft = generateScaledHistogram(imageLeft)
    histadjusted = generateScaledHistogram(adjusted)
    
    #stack the images and histograms
    stacked = np.vstack((stacked, np.hstack((histleft, histadjusted))))
    
    cv2.imshow(WINDOWNAME, stacked)

def adjust_contrast(val):
    global lastBright
    global lastConst
    global adjusted


    lastConst = val / 100

    #adjust contrast
    adjusted = cv2.convertScaleAbs(imageLeft,alpha = lastConst , beta= lastBright )
    stacked = np.hstack((imageLeft, adjusted))
    
    #generate scaled histograms for original and adjusted images
    histleft = generateScaledHistogram(imageLeft)
    histadjusted = generateScaledHistogram(adjusted)
    
    #stack the images and histograms
    stacked = np.vstack((stacked, np.hstack((histleft, histadjusted))))
    
    cv2.imshow(WINDOWNAME, stacked)



imageLeft = cv2.imread('Assigment1/dog.bmp')
adjusted = imageLeft.copy()

#make window
cv2.namedWindow(WINDOWNAME)

#show default image
stacked = np.hstack((imageLeft, adjusted))

lastConst = 1
lastBright = 0

#generate scaled histograms for the original image
histleft = generateScaledHistogram(imageLeft)
histadjusted = generateScaledHistogram(adjusted)

#stack the images and histograms initially
stacked = np.vstack((stacked, np.hstack((histleft, histadjusted))))

#show the stacked image with histograms
cv2.imshow(WINDOWNAME, stacked)

#create sliderbar for brightness and contrast
cv2.createTrackbar('Brightness', WINDOWNAME, 127, 255, adjust_brightness)
cv2.createTrackbar('Contrast', WINDOWNAME, 100, 300, adjust_contrast)

#this loop keeps the window open until you hit 'q'
while True:
    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(1) == ord('s'):
        cv2.imwrite('Assigment1/dog-modified.bmp', adjusted)
        
        #reload the saved image as the new 'imageLeft' for further adjustments
        imageLeft = cv2.imread('Assigment1/dog-modified.bmp')
        adjusted = imageLeft.copy()
        
        stacked = np.hstack((imageLeft, adjusted))
        hist_left = generateScaledHistogram(imageLeft)
        hist_adjusted = generateScaledHistogram(adjusted)
        stacked_with_hist = np.vstack((stacked, np.hstack((hist_left, hist_adjusted))))
        cv2.imshow(WINDOWNAME, stacked_with_hist)

cv2.destroyAllWindows()