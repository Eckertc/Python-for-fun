##  GrahamScan.py - Algorithm Implementation for Calculating Convex Hull       ##
##  Craig Eckert 2018                                                          ##
#################################################################################

import numpy as np

"""
================================
== Convex Hull                 =
================================
== Simple Graham Scan Implm    =
================================
== Finds a Convex Hull Given   =
== Some Set of Points          =
== for Inputs                  =
================================
"""

## helper functions
def CCW(v0, v1, v2):
    """Checks counter clockwise orientation of points.
    """
    return (v1[0] - v0[0]) * (v2[1] - v0[1]) - (v2[0] - v0[0]) * (v1[1] - v0[1]) > 0

def SlopeCalc(v0, v1):
    """Calculates and returns the slope of two Vertices.
       Returns None for duplicate inputs.
    """
    if v0 == v1 :
        return None
    elif v1[1] == v0[1] :
        # sign determines +/- colinear orrentation
        return v1[0] - v0[0]
    else:
        return (v1[0] - v0[0]) / (v1[1] - v0[1])


# NOTE: CORRECT RESULTS FOR BELLOW: (0, -9) (7, -7) (9, 0) (7, 7) (0, 9) (-7, 7) (-9, 0) (-7, -7)
points_list = [(7, 7), (7, -7), (-7, -7), (-7, 7), (9, 0), (-9, 0),
               (0, 9), (0, -9), (0, 0), (1, 2), (-2, 1), (-1, -1),
               (3, 4), (4, 3), (-5, 4), (6, 5)]
inital_point = points_list[0]
horizontal_initial_points = []
return_stack = []

# finds -y max value
for p in points_list:
    if p[1] < inital_point[1] :
        inital_point = p
    elif p[1] == inital_point[1] and p[0] < inital_point[0]:
        inital_point = p

# finds and stores degenerate points. Think this can be optimized better
for q in points_list:
    if p[1] == inital_point[1]:
        horizontal_initial_points.append(p)

# remove initial point from list prior to sort
points_list.remove(inital_point)

# TinSorts by slopes to initial point & horizontal degeneracies have been accounted for
points_sorted = sorted(points_list, key=lambda points: -1 * SlopeCalc(inital_point, points))

# Only one should matter since colinear edges are ommitted regardless
if len(horizontal_initial_points) > 0:
    points_sorted.insert(0, max(horizontal_initial_points))

return_stack.append(inital_point)
return_stack.append(points_sorted[0])
return_stack.append(points_sorted[1])

# Begin the Scan
for i in range(2, len(points_sorted)):
    # needs functionality for colinear cases
    # will add later
    while CCW(return_stack[len(return_stack) - 2], return_stack[len(return_stack) - 1], points_sorted[i]) == False:
        return_stack.pop()
    return_stack.append(points_sorted[i])

print(return_stack)
