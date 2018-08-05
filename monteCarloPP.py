 #################################################################################
 ##  monteCarloPP.py - Algorithm Implementation for Calculating Polygon Area    ##
 ##  Craig Eckert 2018                                                          ##
 #################################################################################

import random
import time

"""
 ================================
 ================================
 == Area of a Polygon           =
 ================================
 == Uses Monte Carlo Method     =
 == and Ray Testing             =
 ================================
 ================================
"""
def CCW(v0, v1, v2):
    """Checks counter clockwise orientation of points.
    """
    return (v1[0] - v0[0]) * (v2[1] - v0[1]) - (v2[0] - v0[0]) * (v1[1] - v0[1]) > 0

def PosMax_X(Edge_list) :
    """Given an edge list, the maximum +X direction
       Value is calculated and returned.
    """
    max_value = 0

    for Edge in Edge_list :
        if Edge[0][0] > max_value :
            max_value = Edge[0][0]
        if Edge[1][0] > max_value :
            max_value = Edge[1][0]
    return max_value

def PosMax_Y(Edge_list) :
    """Given an edge list, the maximum +Y direction
       Value is calculated and returned.
    """
    max_value = 0

    for Edge in Edge_list :
        if Edge[0][1] > max_value :
            max_value = Edge[0][1]
        if Edge[1][1] > max_value :
            max_value = Edge[1][1]
    return max_value

def NegMax_X(Edge_list) :
    """Given an edge list, the maximum -X direction
       Value is calculated and returned.
    """
    max_value = 0

    for Edge in Edge_list :
        if Edge[0][0] < max_value :
            max_value = Edge[0][0]
        if Edge[1][0] < max_value :
            max_value = Edge[1][0]
    return max_value

def NegMax_Y(Edge_list) :
    """Given an edge list, the maximum -Y direction
       Value is calculated and returned.
    """
    max_value = 0

    for Edge in Edge_list :
        if Edge[0][1] < max_value :
            max_value = Edge[0][1]
        if Edge[1][1] < max_value :
            max_value = Edge[1][1]
    return max_value

def IsCrossing(Edge1, Edge2) :
    """Given two Edges, Edges are checked for
       intersection. Returns True if so. Does not account
       for colinear cases.
    """
    return CCW(Edge1[0],Edge2[0],Edge2[1]) != CCW(Edge1[1],Edge2[0],Edge2[1]) and CCW(Edge1[0],Edge1[1],Edge2[0]) != CCW(Edge1[0],Edge1[1],Edge2[1])

def CreateRay(Point, PosMaximumX) :
    return [Point, [(PosMaximumX + 2), Point[1]]]

## SET DATA HERE Edge List of Convex Hull
PolygonEdgeList = [[(0,0),(0,11)], [(11,11),(0,11)], [(11,11),(0,0)]]
TESTSCOUNT = 1000000

hit_count = 0
xMax = PosMax_X(PolygonEdgeList) + 5
yMax = PosMax_Y(PolygonEdgeList) + 5
xMin = NegMax_X(PolygonEdgeList) - 5
yMin = NegMax_Y(PolygonEdgeList) - 5
maxArea = (xMax - xMin) * (yMax - yMin)
startTime = time.time()

print("working...")

for i in range(0, TESTSCOUNT) :
    cross_count = 0
    randPoint = [random.uniform(xMin, xMax), random.uniform(xMin, xMax)]
    randRay = CreateRay(randPoint, xMax)

    # check if random point is within polygon
    for Edge in PolygonEdgeList :
        if IsCrossing(Edge, randRay) :
            cross_count = cross_count + 1
    if cross_count % 2 != 0 :
        hit_count = hit_count + 1

endTime = time.time()
areaPercent = hit_count/TESTSCOUNT

print("Aproximate Polygonal Area: " + str(areaPercent * maxArea))
print("Number of Polygonal Edges: " + str(len(PolygonEdgeList)))
print("Tested with " + str(TESTSCOUNT) + " random points.")
print("Finished in " + str(endTime - startTime) + " seconds")
