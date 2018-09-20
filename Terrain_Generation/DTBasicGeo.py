# TODO:
# [] add toggle for scipy algorithm vs bowWat
# [] larger area of generation (possible multi-thread applications)
# [] ability to scroll around and look at terrain
# [] properly take advantage of modern OPENGL and VBOs to reduce lag
# [] refactor and organize
# [] add extra small hills/valleys option for more realism in random mode
# [] define vertical scope
# [] stop drawing duplicate edges in wire mesh render
# [] maintain aspect ratio of image in render

import pygame
import random
import time
import math
import sys
import cv2
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from HashBowWatDT import *
#from BowWatDT import *

TOGGLE_RANDOM = sys.argv[3]
IN_FILE = "img/saltLake.jpg"
if (TOGGLE_RANDOM == "False"):
    im_gray = cv2.imread(IN_FILE, cv2.IMREAD_GRAYSCALE)
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)


def TriangleMesh(TriangleList):
    glBegin(GL_LINES)
    for i in TriangleList:
        glColor3fv(i.ptA.rgb)
        glVertex3fv((i.ptA.x, i.ptA.y, i.ptA.z))
        glColor3fv(i.ptB.rgb)
        glVertex3fv((i.ptB.x, i.ptB.y, i.ptB.z))
        glVertex3fv((i.ptB.x, i.ptB.y, i.ptB.z))
        glColor3fv(i.ptC.rgb)
        glVertex3fv((i.ptC.x, i.ptC.y, i.ptC.z))
        glVertex3fv((i.ptC.x, i.ptC.y, i.ptC.z))
        glColor3fv(i.ptA.rgb)
        glVertex3fv((i.ptA.x, i.ptA.y, i.ptA.z))
    glEnd()

def TriangleFaces(TriangleList):
    glBegin(GL_TRIANGLES)
    for i in TriangleList:
        glColor3fv(i.ptA.rgb)
        glVertex3fv((i.ptA.x, i.ptA.y, i.ptA.z))
        glColor3fv(i.ptB.rgb)
        glVertex3fv((i.ptB.x, i.ptB.y, i.ptB.z))
        glColor3fv(i.ptC.rgb)
        glVertex3fv((i.ptC.x, i.ptC.y, i.ptC.z))
    glEnd()


def getRandomCord():
    return (random.random() * 2.0) - 1

def getRandomZ():
    return random.random() / float(1.0)

def getHeightRGB(X, Z):
    return (1 * X, 1 * Z, 0.7)

def runCalculation(characterTraits):
        CSIZE = 10000
        Sites = []
        # build a outline
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
            SiteXCord = getRandomCord()
            SiteYCord = getRandomCord()
            SiteZCord = 0

            # Z component and color component either populated by random gausian or
            # from the image file loaded
            if TOGGLE_RANDOM == "True":
                for j in range(0, characterTraits):
                    SiteZCord += ((-1) ** IsVallyList[j]) * math.e ** ((-1) * MountainSpreadListX[j] * \
                    (((SiteXCord - MountainCenterListX[j]) ** 2)) - MountainSpreadListY[j] * \
                    (((SiteYCord - MountainCenterListY[j]) ** 2)))
                pointToAdd = Point(SiteXCord, SiteYCord, SiteZCord)
                pointToAdd.rgb = getHeightRGB(SiteXCord,SiteZCord)
            elif TOGGLE_RANDOM == "False":
                im_length, im_width, zzz = im_color.shape
                im_cord_x = math.floor(((SiteXCord) * math.floor((im_width - 1)/2)) + math.floor((im_width - 1)/2))
                im_cord_y = math.floor((((SiteYCord) * math.floor((im_length - 1)/2)) * (-1)) + math.floor((im_length - 1)/2))

                im_red = im_color[im_cord_y][im_cord_x][2]
                im_green = im_color[im_cord_y][im_cord_x][1]
                im_blue = im_color[im_cord_y][im_cord_x][0]
                SiteZCord = (((im_red<<16) + (im_green<<8) + im_blue) / 16777215) * (0.5)

                pointToAdd = Point(SiteXCord, SiteYCord, SiteZCord)
                pointToAdd.rgb = (float(im_color[im_cord_y][im_cord_x][2] / 256), \
                 float(im_color[im_cord_y][im_cord_x][1] / 256),                  \
                 float(im_color[im_cord_y][im_cord_x][0] / 256))
            else:
                print("IsRandom Argument Invalid! Use 'True' or 'False'")
                print("Note: False implies a file is present to be read")
                print("Example Usage: Python3 DTBasicGeo.py [plotCount] [characterTraits] [IsRandom]")
                exit(-1)
            Sites.append(pointToAdd)

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
    if(len(sys.argv) < 4):
        print("Argument Missing!")
        print("Example Usage: python3 DTBasicGeo.py [plotCount] [characterTraits] [IsRandom]")
        exit()
    main()
