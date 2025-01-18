import cv2

# # Read an image
img = cv2.imread('test_image.png')

#  Check if image is loaded successfully
if img is None:
    print("Error: Image not loaded")
else:
     # Display the image
     cv2.imshow('Test Image', img)
     cv2.waitKey(0)
     cv2.destroyAllWindows()
 