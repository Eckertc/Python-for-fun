import math
import numpy

##Point Class
class Point:
   x = 0.0
   y = 0.0
   z = 0.0

   def __init__(self, x, y, z):
       self.x = x
       self.y = y
       self.z = z
##Edge Class
class Edge:
    start = None
    end = None
    done = False

    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

    def finish(self, p):
        if self.done: return
        self.end = p
        self.done = True
##Triangle Class
class Triangle:
    def __init__(self, a, b, c):
        self.ptA=a
        self.ptB=b
        self.ptC=c
        self.edgeA=Edge(self.ptA)
        self.edgeA.finish(self.ptB)
        self.edgeB=Edge(self.ptA)
        self.edgeB.finish(self.ptC)
        self.edgeC=Edge(self.ptB)
        self.edgeC.finish(self.ptC)

##DT Class
class DT:
                    #####CONSTRUCTOR#####
    def __init__(self, vertices, CSIZE):
        # speed up by presorting initially to reduce bad triangles
        # for x and y coords then determines which metric has the largest average
        # distance between points and uses it for DT calculation
        self.sorted_x_vertices = sorted(vertices, key=lambda xSet: xSet.x)
        self.sorted_y_vertices = sorted(vertices, key=lambda ySet: ySet.y)
        self.count = 0
        self.range = 0

        # checkout x set
        for i in range(1, len(vertices) - 1):
            self.count +=1
            self.range += self.PointDistance(self.sorted_x_vertices[i], self.sorted_x_vertices[i - 1])
        self.xAvg = float(self.range)/float(self.count)
        self.range = 0
        self.count = 0
        # checkout y set
        for i in range(1, len(vertices) - 1):
            self.count +=1
            self.range += self.PointDistance(self.sorted_y_vertices[i], self.sorted_y_vertices[i - 1])
        self.yAvg = float(self.range)/float(self.count)

        # intialize our vertex list
        if(self.yAvg > self.xAvg):
            self.vertices = self.sorted_y_vertices
        else:
            self.vertices = self.sorted_x_vertices

        del self.sorted_x_vertices
        del self.sorted_y_vertices
        del self.count
        del self.range
        del self.yAvg
        del self.xAvg

        self.triangles=[]
        self.R_triangles=[]
        self.circumcircles=[]
        self.edges=[]
        ##Create super triangle
        self.s0 = Point(-CSIZE * 999, -CSIZE * 999, 0)
        self.s1 = Point(CSIZE * 999, -CSIZE * 999, 0)
        self.s2 = Point(0, CSIZE * 999, 0)
        # add super triangle verts to Vertices
        self.vertices.append(self.s0)
        self.vertices.append(self.s1)
        self.vertices.append(self.s2)
        superTri=Triangle(self.s0, self.s1, self.s2)
        self.triangles.append(superTri)

                    #####HELPER FUNCS#####
##Check orientation of triangle points
    def CCW(self, v0, v1, v2):
        return (v1.x - v0.x) * (v2.y - v0.y) - (v2.x - v0.x) * (v1.y - v0.y) > 0

##Check if point p is in circumcircle of a triangle t
    def InCircum(self, t, p):
        # matrix determinant for circumcircle test
        matrix = [[t.ptA.x, t.ptA.y, (t.ptA.x ** 2) + (t.ptA.y ** 2), 1], \
        [t.ptB.x, t.ptB.y, (t.ptB.x ** 2) + (t.ptB.y ** 2), 1], \
        [t.ptC.x, t.ptC.y, (t.ptC.x ** 2) + (t.ptC.y ** 2), 1], \
        [p.x, p.y, (p.x ** 2) + (p.y ** 2), 1]]

        # checks if p is in circumcircle
        result = numpy.linalg.det(matrix)

        if self.CCW(t.ptA, t.ptB, t.ptC) == True and result >= 0:
            return True
        elif self.CCW(t.ptA, t.ptB, t.ptC) == False and result > 0:
            return False
        elif self.CCW(t.ptA, t.ptB, t.ptC) == True and result <= 0:
            return False
        else:
            return True

##Calculate distance between two points
    def PointDistance(self, p1, p2):
        return math.sqrt((p2.x -  p1.x) * (p2.x -  p1.x) + (p2.y -  p1.y) * (p2.y -  p1.y))

##Triangulate the Delauney Triangulation
    def triangulate(self):
        """Compute Delaunay Triangulation from a list of Vertices and
        screen_radius. Returns a List of triangles. Does not take into
        account for degenerate cases or close floating point values
        in circumcircle calculations.
        """
        # iterate through vertex list
        for v in self.vertices:
            # clear edge list each pass
            self.edges.clear()
            # create buffer for Triangles to del
            Tri_to_rm = []

            # iterate through triangle list
            # check for bad triangles
            for i in range(0, len(self.triangles)):
                # if it's a bad triangle
                if self.InCircum(self.triangles[i], v):
                    # add 3 edges to edge list and rm bad triangle
                    self.edges.append(self.triangles[i].edgeA)
                    self.edges.append(self.triangles[i].edgeB)
                    self.edges.append(self.triangles[i].edgeC)
                    #self.triangles.remove(self.trianle[i])
                    # store bad triangles in buffer to be removed
                    Tri_to_rm.append(self.triangles[i])

            for triangle_rm in Tri_to_rm:
                self.triangles.remove(triangle_rm)

            # edges list will be scanned linearly and on each itteration
            # check if in hashmap, null edge, else, add to hashmap and continue
            #create a hashmap
            dict = {}

            for edgeL in self.edges:
                if (hash(((edgeL.start.x, edgeL.start.y),(edgeL.end.x, edgeL.end.y))) in dict.keys()):
                    del dict[hash(((edgeL.start.x, edgeL.start.y),(edgeL.end.x, edgeL.end.y)))]

                    if (hash(((edgeL.end.x, edgeL.end.y),(edgeL.start.x, edgeL.start.y))) in dict.keys()):
                        del dict[hash(((edgeL.end.x, edgeL.end.y),(edgeL.start.x, edgeL.start.y)))]
                else:
                    dict[hash(((edgeL.start.x, edgeL.start.y),(edgeL.end.x, edgeL.end.y)))] = \
                    ((edgeL.start.x, edgeL.start.y),(edgeL.end.x, edgeL.end.y))
                    dict[hash(((edgeL.end.x, edgeL.end.y),(edgeL.start.x, edgeL.start.y)))] = \
                    ((edgeL.end.x, edgeL.end.y),(edgeL.start.x, edgeL.start.y))

            # add to all new triangles formed with the Edges
            # boundary and vertex
            for e in self.edges:
                if not(hash(((e.end.x, e.end.y),(e.start.x, e.start.y))) in dict.keys()):
                    continue
                if(self.CCW(e.start, e.end, v)):
                    tri=Triangle(e.start, e.end, v)
                    self.triangles.append(tri)
                else:
                    tri=Triangle(v, e.end, e.start)
                    self.triangles.append(tri)
            del dict

        # get rid of super triangle reliant triangles
        # by only adding valid to R_triangles
        for t in self.triangles:
            if ((t.ptA.x == self.s0.x and t.ptA.y == self.s0.y) or \
            (t.ptA.x == self.s1.x and t.ptA.y == self.s1.y) or     \
            (t.ptA.x == self.s2.x and t.ptA.y == self.s2.y)):
                continue
            elif ((t.ptB.x == self.s0.x and t.ptB.y == self.s0.y) or \
            (t.ptB.x == self.s1.x and t.ptB.y == self.s1.y) or       \
            (t.ptB.x == self.s2.x and t.ptB.y == self.s2.y)):
                continue
            elif ((t.ptC.x == self.s0.x and t.ptC.y == self.s0.y) or \
            (t.ptC.x == self.s1.x and t.ptC.y == self.s1.y) or       \
            (t.ptC.x == self.s2.x and t.ptC.y == self.s2.y)):
                continue
            else:
                self.R_triangles.append(t)
        self.vertices.remove(self.s0)
        self.vertices.remove(self.s1)
        self.vertices.remove(self.s2)

    def get_output_edges(self):
        edges=[]
        for t in self.R_triangles:
            edges.append(t.edgeA)
            edges.append(t.edgeB)
            edges.append(t.edgeC)
        return edges

    def get_output_triangles(self):
        return self.R_triangles
