import tkinter as tk

class Window(tk.Frame):

    def __init__(self, GeoAlg):
        super().__init__()
        self.GeoAlg = GeoAlg
        self.points_list = []
        self.MAX_WIDTH = 1280
        self.MAX_HEIGHT = 720
        self.LINE_COLOR = "#32bf28"
        self.POINT_COLOR = "#031402"
        self.AXIS_COLOR = "#b2d8af"
        self.initUI()

    def initUI(self):
        self.master.title("Drawing Convex Hull")
        self.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(self)
        self.DrawAxis()
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.myButton = tk.Button(text="Clear", command=self.clearPoints)
        self.myButton.pack()

    def clearPoints(self):
        self.canvas.delete("all")
        self.DrawAxis()
        self.points_list.clear()

    def DrawAxis(self):
        # draw axis
        self.canvas.create_line(0, self.MAX_HEIGHT/2, self.MAX_WIDTH, self.MAX_HEIGHT/2, fill = self.AXIS_COLOR)
        self.canvas.create_line(self.MAX_WIDTH/2, 0, self.MAX_WIDTH/2, self.MAX_HEIGHT, fill = self.AXIS_COLOR)

    def DrawPoint(self, ovalPoint):
        self.canvas.create_oval(ovalPoint[0]+1, ovalPoint[1]+1, ovalPoint[0]-1, ovalPoint[1]-1, fill = self.POINT_COLOR)

    def DrawLine(self, p1, p2):
        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill = self.LINE_COLOR)

    def DrawObj(self, event):
        self.canvas.delete("all")
        self.DrawAxis()

        # add point on click event to list and plot point before calculation
        self.points_list.append((event.x, event.y))
        self.DrawPoint((event.x, event.y))

        self.PointList = self.GeoAlg(self.points_list)
        self.DrawAxis()

        # Draw points in points_list
        for p in self.points_list:
            self.DrawPoint(p)

        last_point = self.PointList[len(self.PointList) - 1]
        # draw all the edges
        for i in range(0, len(self.PointList)):
            current_point = self.PointList[i]
            self.DrawLine(current_point, last_point)
            self.canvas.pack(fill=tk.BOTH, expand=1)
            last_point = current_point

        self.canvas.pack(fill=tk.BOTH, expand=1)

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
        return inData

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

def main():
    root = tk.Tk()
    DrawingWindow = Window(GiftWrap)
    root.geometry(str(DrawingWindow.MAX_WIDTH) + "x" + str(DrawingWindow.MAX_HEIGHT))
    DrawingWindow.canvas.bind("<Button>", DrawingWindow.DrawObj)
    root.mainloop()


if __name__ == '__main__':
    main()
