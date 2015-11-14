import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image
from scipy import ndimage as ndi
import scipy
import cv2
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

## Gaussian Blur 
gaussianBlurImage = cv2.GaussianBlur(originalImg,(5,5),0)

## Gaussian Blur With Color Filter
gaussianBlurColorFilterImg = cv2.GaussianBlur(colorFilterImg,(5,5),0)

## Image Denoising With Gaussian Blur And Color Filter
imageDenoisingGaussianBlurColorFilterImg = cv2.fastNlMeansDenoising(gaussianBlurColorFilterImg, h=200)

## Canny Edge Detector With Gaussian Blur And Color Filter
#arrayGaussianBlurColorFilterImg = np.array(gaussianBlurColorFilterImg,0)
arrayGaussianBlurColorFilterImg = np.asarray(gaussianBlurColorFilterImg)
cannyEdgeGaussianBlurColorFilterImg = feature.canny(arrayGaussianBlurColorFilterImg)

## Canny Edge Detector With Image Denoising And Gaussian Blur And Color Filter
arrayImageDenoisingGaussianBlurColorFilterImg = np.asarray(gaussianBlurColorFilterImg)
cannyEdgeImageDenoisingGaussianBlurColorFilterImg = feature.canny(arrayImageDenoisingGaussianBlurColorFilterImg)

## Write Desired Image to File
scipy.misc.imsave('CoastlineRecognition_With_GaussianBlur.jpg', cannyEdgeImageDenoisingGaussianBlurColorFilterImg)


## Display results
fig, (img0, img1, img2) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))
fig, (img3, img4) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))

img0.imshow(originalImg, cmap=plt.cm.gray)
img0.axis('off')
img0.set_title('Original', fontsize=20)

img1.imshow(colorFilterImg, cmap=plt.cm.gray)
img1.axis('off')
img1.set_title('Colour Filter', fontsize=20)

img2.imshow(gaussianBlurColorFilterImg, cmap=plt.cm.gray)
img2.axis('off')
img2.set_title('Gaussian Blur + Color Filter', fontsize=20)

img3.imshow(imageDenoisingGaussianBlurColorFilterImg, cmap=plt.cm.gray)
img3.axis('off')
img3.set_title('Image Denoising + Gaussian Blur + Color Filter', fontsize=20)

img4.imshow(cannyEdgeImageDenoisingGaussianBlurColorFilterImg, cmap=plt.cm.gray)
img4.axis('off')
img4.set_title('Canny Edge Detection + Image Denoising + Gaussian Blur + Color Filter, $\sigma=1$', fontsize=20)

fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                    bottom=0.02, left=0.02, right=0.98)

plt.show()
