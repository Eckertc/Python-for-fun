# TODO:
# [] add toggle for scipy algorithm vs bowWat
# [] larger area of generation
# [] ability to scroll around and look at terrain
# [] properly take advantage of OPENGL to reduce lag
# [] refactor and organize
# [] add extra small hills/valleys option for more realism
# [] define vertical scope
# [] proper color variation in HEIGHT

import pygame
import random
import time
import math
import sys
import numpy as np
from scipy.spatial import Delaunay
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from HashBowWatDT import *
#from BowWatDT import *


def TriangleMesh(TriangleList):
    glBegin(GL_LINES)
    for i in TriangleList:
        glVertex3fv((i.ptA.x, i.ptA.y, i.ptA.z))
        glVertex3fv((i.ptB.x, i.ptB.y, i.ptB.z))
        glVertex3fv((i.ptB.x, i.ptB.y, i.ptB.z))
        glVertex3fv((i.ptC.x, i.ptC.y, i.ptC.z))
        glVertex3fv((i.ptC.x, i.ptC.y, i.ptC.z))
        glVertex3fv((i.ptA.x, i.ptA.y, i.ptA.z))
    glEnd()

def TriangleFaces(TriangleList):
    glBegin(GL_TRIANGLES)
    for i in TriangleList:
        glColor3fv(getHeightRGB(i.ptA))
        glVertex3fv((i.ptA.x, i.ptA.y, i.ptA.z))
        glColor3fv(getHeightRGB(i.ptB))
        glVertex3fv((i.ptB.x, i.ptB.y, i.ptB.z))
        glColor3fv(getHeightRGB(i.ptC))
        glVertex3fv((i.ptC.x, i.ptC.y, i.ptC.z))
    glEnd()


def getRandomCord():
    return (random.random() * 2) - 1

def getRandomZ():
    return random.random() / float(1.0)

def getHeightRGB(Height):
    return (1 * Height.x, 1 * Height.z, 0.7)

def runCalculation(characterTraits):
        CSIZE = 10000
        Sites = []
        # build a aproximate outline
        Sites.append(Point(1,1,0))
        Sites.append(Point(1,-1,0))
        Sites.append(Point(-1,-1,0))
        Sites.append(Point(-1,1,0))
        Sites.append(Point(1,0,0))
        Sites.append(Point(0,1,0))
        Sites.append(Point(-1,0,0))
        Sites.append(Point(0,-1,0))

        #Build hill and valley attribute lists
        IsVallyList = []
        MountainSpreadListX = []
        MountainSpreadListY = []
        MountainCenterListX = []
        MountainCenterListY = []

        # fill in the mountain data
        for i in range(0, characterTraits):
            if random.random() > 0.55:
                IsVallyList.append(False)
            else:
                IsVallyList.append(True)
            MountainSpreadListX.append(random.random() * 8)
            MountainSpreadListY.append(MountainSpreadListX[i])
            MountainCenterListX.append(random.random() * 2 - 1)
            MountainCenterListY.append(random.random() * 2 - 1)

        for i in range(0, int(sys.argv[1])):
            # RANDOM HEIGHT METHOD HERE
            SiteXCord = getRandomCord()
            SiteYCord = getRandomCord()
            SiteZCord = 0
            # Itterate through all the hills and sum the Z component
            for j in range(0, characterTraits):
                SiteZCord += ((-1) ** IsVallyList[j]) * math.e ** ((-1) * MountainSpreadListX[j] * \
                (((SiteXCord - MountainCenterListX[j]) ** 2)) - MountainSpreadListY[j] * \
                (((SiteYCord - MountainCenterListY[j]) ** 2)))
            Sites.append(Point(SiteXCord, SiteYCord, SiteZCord))

        startTime = time.time()
        dt=DT(Sites, CSIZE)
        dt.triangulate()
        CalculatedTriangles=dt.get_output_triangles()
        del dt
        endTime = time.time()

        print(str(len(CalculatedTriangles)) +" many triangles in DT")
        print("Calculated in: " + str(endTime - startTime) + " Seconds")

        return CalculatedTriangles


def main():
    CalculatedTriangles = runCalculation(int(sys.argv[2]))

    pygame.init()
    display = (1280,720)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)

    glTranslatef(0.0,0.0, -3.5)
    glRotatef(40.0, -3, -1, -1)

    TOGGLEWIRE = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if TOGGLEWIRE == False:
                        TOGGLEWIRE = True
                    else:
                        TOGGLEWIRE = False
                if event.key == pygame.K_r:
                    # randomize points
                    CalculatedTriangles = runCalculation(int(sys.argv[2]))
                    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
                    glEnable(GL_DEPTH_TEST)
                    glEnable(GL_CULL_FACE)

                    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)

                    glTranslatef(0.0,0.0, -3.5)
                    glRotatef(40.0, -3, -1, -1)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 0, -1)

        if TOGGLEWIRE == True:
            TriangleMesh(CalculatedTriangles)
        else:
            TriangleFaces(CalculatedTriangles)
        pygame.display.flip()
        #pygame.time.wait(10)



if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Random Point Count Argument Missing")
        print("Example Usage: Python3 DTBasicGeo.py [plotCount] [characterTraits]")
        exit()
    main()
