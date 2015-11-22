import shapefile
import matplotlib.pyplot as plt
import numpy as np
import math
import argparse
import array

#The point class
class Point:
    #create a point from an array with two elements
    def __init__(self,shpPoint):
        self.lat = shpPoint[1]
        self.long = shpPoint[0]

parser = argparse.ArgumentParser(description="Enter file path to NOAA Data")
parser.add_argument('path',metavar='path',nargs='?')
args = parser.parse_args();

upPoint = Point([8.951111,4.239595])
downPoint = Point([9.629517,3.798484])

if (args.path == None):
    pathToCoastLineData = '/Users/curtishuebner/documents/development/CDHImageProccessing/coastlineData'
else:
    pathToCoastLineData = args.path;
        

#Check to see if a point falls within a given range.
def inRange(a,b,x):
    if a > b:
        if a > x and x > b:
            return True
    if b > a:
        if b > x and x > a:
            return True
    
    if a == x or b == x:
        return True
        
    return False

#filters out locations that are not in the rectangle specified by topRight and bottomLeft
def isInArea(location, northWest, southEast):
        if (inRange(northWest.lat,southEast.lat,location.lat) and
           inRange(northWest.long,southEast.long,location.long)):
            return True
        else:
            return False

#Generate the file location array
fileLocations = []
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/c/GSHHS_c_L1.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/c/GSHHS_c_L2.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/c/GSHHS_c_L3.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/c/GSHHS_c_L5.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/c/GSHHS_c_L6.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/f/GSHHS_f_L1.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/f/GSHHS_f_L2.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/f/GSHHS_f_L3.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/f/GSHHS_f_L4.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/f/GSHHS_f_L5.shp')
fileLocations.append('/gshhg-shp-2.3.4/GSHHS_shp/f/GSHHS_f_L6.shp')


#Build a list of list of shapes
shapeList = []
for fileLocation in fileLocations:
    sf = shapefile.Reader(pathToCoastLineData + fileLocation)
    shapeList.append(sf.shapes())
    
#Build a list of points
locations = []
counter = 0
for shapes in shapeList:
    for shape in shapes:
        for point in shape.points:
            if (isInArea(Point(point),upPoint,downPoint)):
                locations.append(Point(point))
            if (counter % 10000 == 0):
                print(counter)
            counter += 1

print(counter)
            


def renderImage2(locations,northWest):
    pass

#print a 2D representation of the coastline between two points.
def renderImage(locations,northWest,southEast):
    size = 500
    xWidth = northWest.lat - southEast.lat
    yWidth = southEast.long - northWest.long
    xLength = size * xWidth
    yLength = size * yWidth
    outputArray = np.zeros((math.ceil(xLength),math.ceil(yLength)))
    
    for location in locations:
        if (isInArea(location,upPoint,downPoint)):
               
            normedX = (northWest.lat - location.lat) * xLength / (xWidth)
            normedY = (location.long - southEast.long) * yLength / (yWidth)
            print(xWidth)
            print(yWidth)
            print(normedX)
            print(normedY)
            xCoord = math.floor(normedX)
            yCoord = math.floor(normedY)
            outputArray[xCoord,yCoord] = 1
            
    return outputArray
            


plt.imshow(renderImage(locations,upPoint,downPoint))
plt.show()



    