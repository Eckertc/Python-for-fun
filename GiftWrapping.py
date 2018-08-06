#################################################################################
##  GiftWrapping.py - Algorithm Implementation for Calculating Convex Hull     ##
##  Craig Eckert 2018                                                          ##
##  Three points which are colinear behavior is undefined                      ##
#################################################################################

"""
================================
== Convex Hull                 =
================================
== Simple GiftWrapping Impl    =
================================
== Finds a Convex Hull Given   =
== Some Set of Points. Makes   =
== Use of Left Test to Compute =
== in O(nh) Time Complexity.   =
================================
"""
def PointIsLeft(vi, vf, point):
    """Returns True for Left, False for Right, and None for colinearself.
    """
    DetPIL =  (point[0] - vi[0])*(vf[1] - vi[1]) - (point[1] - vi[1])*(vf[0] - vi[0])
    if DetPIL < 0 :
        return True
    elif DetPIL > 0 :
        return False
    else :
        return None

def GiftWrap(inData):

    # if less than a triangle
    if len(inData) < 3:
        return outData

    mainP = inData[0]
    outData = []
    #find left most point
    for p in inData:
        if (p[0] < mainP[0]):
            mainP = p

    # start itterative Scan
    for i in range(0, len(inData)):
        outData.append(mainP)
        endP = inData[0]
        for j in range(1, len(inData)):
            if (endP == mainP) or PointIsLeft(outData[i], endP, inData[j]):
                endP = inData[j]
        mainP = endP
        if endP == outData[0]:
            break

    return outData




# NOTE: OUTPUT SHOULD BE: (OR SOME EQUIVILANT CHAIN)
# [(-9, 0), (-7, 7), (0, 9), (7, 7), (9, 0), (7, -7), (0, -9), (-7, -7)]
points_list = [(7, 7), (7, -7), (-7, -7), (-7, 7), (9, 0), (-9, 0),
               (0, 9), (0, -9), (0, 0), (1, 2), (-2, 1), (-1, -1),
               (3, 4), (4, 3), (-5, 4), (6, 5)]

print(GiftWrap(points_list))
