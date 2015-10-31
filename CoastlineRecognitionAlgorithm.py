import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import cv2
from skimage import feature


# Read Image
img = cv2.imread('C:/Users/Jeffrey/DEVELOPMENT/ORBIT/TRAINING_SET/SpaceCoastFromSpaceStation.jpg')

## Color Filter
# Min/Max For Color Filter
BLUE_MIN = np.array([80, 110, 0],np.uint8)
BLUE_MAX = np.array([160, 255, 255],np.uint8)

#Convert from RGB to HSV
hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#Apply Color Filter
colorFilteredImg = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)       

## Canny Edge Detector
# Compute the Canny filter for two values of sigma
edges1 = feature.canny(guassianBlurredImage)
edges2 = feature.canny(guassianBlurredImage, sigma=2)
edges3 = feature.canny(guassianBlurredImage, sigma=3)

## Display results
fig, (img0, img1, img2, img3, img4, img5) = plt.subplots(nrows=1, ncols=6, figsize=(8, 3))

img0.imshow(img, cmap=plt.cm.gray)
img0.axis('off')
img0.set_title('Original', fontsize=20)

img1.imshow(filteredImg, cmap=plt.cm.gray)
img1.axis('off')
img1.set_title('Colour Filter', fontsize=20)

img2.imshow(edges1, cmap=plt.cm.gray)
img2.axis('off')
img2.set_title('Color Filter + Canny Filter, $\sigma=1$', fontsize=20)

img3.imshow(edges2, cmap=plt.cm.gray)
img3.set_title('Color Filter + Canny Filter, $\sigma=2$', fontsize=20)

img4.imshow(edges3, cmap=plt.cm.gray)
img4.axis('off')
img4.set_title('Color Filter + Canny Filter, $\sigma=3$', fontsize=20)

img5.imshow(gaussianBlurredImage, cmap=plt.cm.gray)
img5.axis('off')
img5.set_title('Color Filter + Gaussian Blur, fontsize=20)

fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                    bottom=0.02, left=0.02, right=0.98)

plt.show()


