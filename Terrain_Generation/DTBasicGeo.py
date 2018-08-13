import pygame
import random
import time
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from BowWatDT import *


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

def main():
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

    for i in range(0, int(sys.argv[1])):
        Sites.append(Point(getRandomCord(), getRandomCord(), getRandomZ()))

    startTime = time.time()
    dt=DT(Sites, CSIZE)
    dt.triangulate()
    CalculatedTriangles=dt.get_output_triangles()
    del dt
    endTime = time.time()

    print(str(len(CalculatedTriangles)) +" many triangles in DT")
    print("Calculated in: " + str(endTime - startTime) + " Seconds")

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
                    startTime = time.time()
                    dt=DT(Sites, CSIZE)
                    dt.triangulate()
                    CalculatedTriangles=dt.get_output_triangles()
                    del dt
                    endTime = time.time()

                    print(str(len(CalculatedTriangles)) +" many triangles in DT")
                    print("Calculated in: " + str(endTime - startTime) + " Seconds")

                    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
                    glEnable(GL_DEPTH_TEST)
                    glEnable(GL_CULL_FACE)

                    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)

                    glTranslatef(0.0,0.0, -3.5)
                    glRotatef(40.0, -3, -1, -1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 0, -1)

        if TOGGLEWIRE == True:
            TriangleMesh(CalculatedTriangles)
        TriangleFaces(CalculatedTriangles)
        pygame.display.flip()
        pygame.time.wait(10)



if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Random Point Count Argument Missing")
        print("Example Usage: Python3 DTBasicGeo.py 500")
        exit()
    main()
