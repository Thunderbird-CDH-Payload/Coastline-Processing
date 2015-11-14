import numpy as np
import matplotlib.pyplot as plt
import PIL
import scipy
import cv2

from PIL import Image
from scipy import ndimage as ndi
from skimage import feature
from optparse import OptionParser

## Command-Line Parser
parser = OptionParser()
parser.add_option("-I", "--image", dest="image",
                  help="Image to be parsed", metavar="IMAGE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

## Read Image
originalImg = cv2.imread(options.image)

## Color Filter
# Min/Max For Color Filter
BLUE_MIN = np.array([75, 60, 0],np.uint8)
BLUE_MAX = np.array([165, 255, 255],np.uint8)

#Convert from RGB to HSV
hsv_img = cv2.cvtColor(originalImg, cv2.COLOR_BGR2HSV)

#Apply Color Filter
colorFilterImg = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)

## Bilateral Filter
bilateralFilterImg = cv2.bilateralFilter(originalImg,9,75,75)

## Bilateral Filter With Color Filter
bilateralFilterColorFilterImg = cv2.bilateralFilter(colorFilterImg,9,75,75)

## Image Denoising With Bilateral Filter And Color Filter
imageDenoisingBilateralFilterColorFilterImg = cv2.fastNlMeansDenoising(bilateralFilterColorFilterImg, h=200)

## Canny Edge With Bilateral And Color Filter
cannyEdgeBilateralFilterColorFilterImg = feature.canny(bilateralFilterColorFilterImg)

## Canny Edge With Image Denoising And Bilateral And Color Filter
arrayImageDenoisingBilateralFilterColorFilterImg = np.asarray(imageDenoisingBilateralFilterColorFilterImg)
cannyEdgeImageDenoisingBilateralFilterColorFilterImg = feature.canny(arrayImageDenoisingBilateralFilterColorFilterImg)

## Write Desired Image to File
scipy.misc.imsave('CoastlineRecognition_With_BilateralFilter.jpg', cannyEdgeImageDenoisingBilateralFilterColorFilterImg)

## Display results
fig, (img0, img1, img2) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))
fig, (img3, img4) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))

img0.imshow(originalImg, cmap=plt.cm.gray)
img0.axis('off')
img0.set_title('Original', fontsize=20)

img1.imshow(colorFilterImg, cmap=plt.cm.gray)
img1.axis('off')
img1.set_title('Colour Filter', fontsize=20)

img2.imshow(bilateralFilterColorFilterImg, cmap=plt.cm.gray)
img2.axis('off')
img2.set_title('Bilateral Filter + Color Filter', fontsize=20)

img3.imshow(imageDenoisingBilateralFilterColorFilterImg, cmap=plt.cm.gray)
img3.axis('off')
img3.set_title('Image Denoising + Bilateral Filter + Color Filter', fontsize=20)

img4.imshow(cannyEdgeImageDenoisingBilateralFilterColorFilterImg, cmap=plt.cm.gray)
img4.axis('off')
img4.set_title('Canny Filter + Image Denoising + Bilateral Filter + Color Filter, $\sigma=1$', fontsize=20)

fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                    bottom=0.02, left=0.02, right=0.98)

plt.show()


