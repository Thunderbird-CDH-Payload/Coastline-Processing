import shapefile
import matplotlib.pyplot as plt
import numpy as np
import math



#The point class
class Point:
    #create a point from an array with two elements
    def __init__(self,shpPoint):
        self.lat = shpPoint[1]
        self.long = shpPoint[0]
        

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
def filterLocations(locations, northWest, southEast):
    filteredLocations = []
    for location in locations:
        if (location.lat < northWest.lat and 
           location.long < northWest.long and
           location.lat > southEast.lat and
           location.lat > southEast.lat):
            filteredLocations.append(location)
            
    return filteredLocations

#for now, just switch out this file path for the path to your own coastline data
pathToCoastLineData = '/Users/curtishuebner/documents/development/CDHImageProccessing/coastlineData'

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
    sf = shapefile.Reader(fileLocation)
    shapeList.append(sf.shapes())
    
#Build a list of points
locations = []
counter = 0
for shapes in shapeList:
    for shape in shapes:
        for point in shape.points:
            locations.append(Point(point))
            if (counter % 10000 == 0):
                pass#print(point)
            counter += 1

print(counter)
            


#print a 2D representation of the coastline between two points.
def renderImage(locations,northWest,southEast):
    xLength = 500
    yLength = 500
    xWidth = northWest.lat - southEast.lat
    yWidth = southEast.long - northWest.long
    outputArray = np.zeros((xLength,yLength))
    
    for location in locations:
        if (inRange(northWest.lat,southEast.lat,location.lat) and
           inRange(northWest.long,southEast.long,location.long)):
               
            normedX = (location.lat - northWest.lat) * xLength / (xWidth)
            normedY = (location.long - southEast.long) * yLength / (yWidth)
            print(xWidth)
            print(yWidth)
            print(normedX)
            print(normedY)
            xCoord = math.floor(normedX)
            yCoord = math.floor(normedY)
            outputArray[xCoord,yCoord] = 1
            
    return outputArray
            
upPoint = Point([8.951111,4.239595])
downPoint = Point([9.629517,3.798484])


plt.imshow(renderImage(locations,upPoint,downPoint))
plt.show()



    