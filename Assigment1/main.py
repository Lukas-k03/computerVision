import cv2
import numpy as np

WINDOWNAME = "Assignment 1 App (press q to exit s to save)"

lastBright = None
lastConst = None
adjusted = None

def generateScaledHistogram(image):
    #convert the image to grayscale for histogram calculation
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #calculate histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
    # Normalize the histogram to fit it in the image window
    hist = hist / hist.max()  # Normalize to the maximum value for scaling
    
    #Create a blank image to draw the histogram
    hist_height = image.shape[0]
    hist_width = 256 
    hist_image = np.zeros((hist_height, hist_width, 3), dtype=np.uint8)
    
    #Draw the histogram on the blank image
    for i in range(1, 256):
        cv2.line(
            hist_image,
            (i-1, hist_height - int(hist[i-1] * hist_height)),
            (i, hist_height - int(hist[i] * hist_height)),
            (255, 255, 255), 1
        )
    
    #Resize the histogram image to the same size as the original image
    scaled = cv2.resize(hist_image, (image.shape[1], image.shape[0]))
    
    return scaled

def adjust_brightness(val):
    global lastConst
    global lastBright
    global adjusted

    lastBright = (val / 128)

    adjusted = cv2.convertScaleAbs(imageLeft, alpha= lastBright, beta = lastConst)
    stacked = np.hstack((imageLeft, adjusted))
    
    # Generate scaled histograms for original and adjusted images
    hist_left = generateScaledHistogram(imageLeft)
    hist_adjusted = generateScaledHistogram(adjusted)
    
    # Stack the images and histograms
    stacked_with_hist = np.vstack((stacked, np.hstack((hist_left, hist_adjusted))))
    
    cv2.imshow(WINDOWNAME, stacked_with_hist)

def adjust_contrast(val):
    global lastBright
    global lastConst
    global adjusted


    lastConst = val - 128

    # Adjust contrast
    adjusted = cv2.convertScaleAbs(imageLeft,alpha = lastBright , beta= lastConst )
    stacked = np.hstack((imageLeft, adjusted))
    
    # Generate scaled histograms for original and adjusted images
    hist_left = generateScaledHistogram(imageLeft)
    hist_adjusted = generateScaledHistogram(adjusted)
    
    # Stack the images and histograms
    stacked_with_hist = np.vstack((stacked, np.hstack((hist_left, hist_adjusted))))
    
    cv2.imshow(WINDOWNAME, stacked_with_hist)



imageLeft = cv2.imread('Assigment1/dog.bmp')
adjusted = imageLeft.copy()

#make window
cv2.namedWindow(WINDOWNAME)

#show default image
stacked = np.hstack((imageLeft, adjusted))

#generate scaled histograms for the original image
hist_left = generateScaledHistogram(imageLeft)
hist_adjusted = generateScaledHistogram(adjusted)

#stack the images and histograms initially
stacked = np.vstack((stacked, np.hstack((hist_left, hist_adjusted))))

#show the stacked image with histograms
cv2.imshow(WINDOWNAME, stacked)

#create sliderbar for brightness and contrast
cv2.createTrackbar('Brightness', WINDOWNAME, 128, 255, adjust_brightness)
cv2.createTrackbar('Contrast', WINDOWNAME, 128, 255, adjust_contrast)

# This loop keeps the window open until you hit 'q'
while True:
    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(1) == ord('s'):
        # Save the adjusted image
        cv2.imwrite('Assigment1/dog-modified.bmp', adjusted)
        
        # Reload the saved image as the new 'imageLeft' for further adjustments
        imageLeft = cv2.imread('Assigment1/dog-modified.bmp')
        adjusted = imageLeft.copy()  # Update the adjusted image to match the new left image
        
        # Update the display
        stacked = np.hstack((imageLeft, adjusted))
        hist_left = generateScaledHistogram(imageLeft)
        hist_adjusted = generateScaledHistogram(adjusted)
        stacked_with_hist = np.vstack((stacked, np.hstack((hist_left, hist_adjusted))))
        cv2.imshow(WINDOWNAME, stacked_with_hist)

# Cleanup
cv2.destroyAllWindows()