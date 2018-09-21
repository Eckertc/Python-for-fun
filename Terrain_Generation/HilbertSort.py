# Hilbert sorting recursive algorithm
# Takes in a List of Point and max <TRCorner>
# positive x and y from (0,0) <BLCorner>

import random

RANDOM_COUNT = 100000

class Point:
   x = 0.0
   y = 0.0
   z = 0.0

   def __init__(self, x, y, z):
       self.x = x
       self.y = y
       self.z = z
       self.rgb = [0,0,0]

class HilbertSort:
    def __init__(self, vertices, max):
        # vertices is a list of cordinate tupples
        self.vertices = vertices
        # returns a list of keys for verticies
        self.returnList = []
        self.max = max

    def sort(self):
        originalVerticies = self.vertices
        #build dictionary
        buildDict = {}
        for i in range(0, len(self.vertices)):
            buildDict[i] = self.vertices[i]
        self.sortRec(buildDict, self.max)
        # match return keys to returning list of points
        output = []
        for i in self.returnList:
            output.append(i)
        return output

    def sortRec(self,points, s):

        # base cases
        if len(points) == 0:
            return
        if len(points) == 1:
            for key, l in points.items():
                self.returnList.append(int(key))
            return

        lowerLeft  = {}
        upperLeft  = {}
        upperRight = {}
        lowerRight = {}
        s = s/2

        for key, p in points.items():
            if  (p.x < s and p.y <= s):
                lowerLeft[key] = p
            elif(p.x <= s and p.y > s):
                upperLeft[key] = p
            elif(p.x > s and p.y >= s):
                upperRight[key] = p
            else:
                lowerRight[key] = p

        # perform transformations on each quad
        for key, p in lowerLeft.items():
            p.x, p.y = p.y, p.x
        for key, p in upperLeft.items():
            p.y -= s
        for key, p in upperRight.items():
            p.x -= s
            p.y -= s
        for key, p in lowerRight.items():
            p.x = s - p.y
            p.y = (s*2) - p.x

        self.sortRec(lowerLeft,  s)
        self.sortRec(upperLeft,  s)
        self.sortRec(upperRight, s)
        self.sortRec(lowerRight, s)

def getRandomCord():
    return (random.random() * 2.0) - 1



# TESTING

data = []
indexData = []
#generate data
for i in range(0, RANDOM_COUNT):
    xData = getRandomCord() + 1
    yData = getRandomCord() + 1
    data.append(Point(xData,yData,0))
    indexData.append(Point(xData,yData,0))
#    print("Generated Point: (" + str(xData) + "," + str(yData) + ")")

print("sorting...")
newThing = HilbertSort(data, 2)
results = newThing.sort()

print("Results:")
#print results
for i in results:
    print(str(indexData[i].x) + " " + str(indexData[i].y))
