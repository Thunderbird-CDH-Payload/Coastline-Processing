from PIL import Image
from optparse import OptionParser

## Command-Line Parser
parser = OptionParser()
parser.add_option("-I", "--image", dest="image",
                  help="Image to be parsed", metavar="IMAGE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

## Open Image
im = Image.open(options.image)

## Convert to RGB
rgb_im = im.convert('RGB')

## Extract Pixel Values
coastlinePoints = []

for x in range(0, im.size[0]):
    for y in range(0, im.size[1]):
        r, g, b = rgb_im.getpixel((x, y))
        
        if((r ==255) and (b ==255) and (g ==255)):
            pixelPosition = []
            pixelPosition.append(x)
            pixelPosition.append(y)
            coastlinePoints.append(pixelPosition)
            
            print coastlinePoints

print im.size

