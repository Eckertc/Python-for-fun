import tkinter as tk

MAX_WIDTH = 1280
MAX_HEIGHT = 720

class Example(tk.Frame):

    def __init__(self, PointList):
        super().__init__()
        self.PointList = PointList
        self.initUI()

    def initUI(self):
        self.master.title("Drawing Convex Hull")
        self.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(self)

        # draw axis
        canvas.create_line(0, MAX_HEIGHT/2, MAX_WIDTH, MAX_HEIGHT/2, fill = "#b2d8af")
        canvas.create_line(MAX_WIDTH/2, 0, MAX_WIDTH/2, MAX_HEIGHT, fill = "#b2d8af")

        last_point = self.PointList[len(self.PointList) - 1]
        # draw all the edges
        for i in range(0, len(self.PointList)):
            current_point = self.PointList[i]
            # adjusted cordinates
            canvas.create_oval(current_point[0] + MAX_WIDTH/2 +1, (-1) * current_point[1] + MAX_HEIGHT/2 +1, current_point[0] + MAX_WIDTH/2 -1, (-1) * current_point[1] + MAX_HEIGHT/2 -1, fill = "#031402")
            canvas.create_line(current_point[0] + MAX_WIDTH/2, (-1) * current_point[1] + MAX_HEIGHT/2, last_point[0] + MAX_WIDTH/2, (-1) * last_point[1] + MAX_HEIGHT/2, fill = "#32bf28")
            canvas.pack(fill=tk.BOTH, expand=1)
            last_point = current_point

        canvas.pack(fill=tk.BOTH, expand=1)

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
    points_list = [(7, 7), (7, -7), (-7, -7), (-7, 7), (9, 0), (-9, 0),
               (0, 9), (0, -9), (0, 0), (1, 2), (-2, 1), (-1, -1),
               (3, 4), (4, 3), (-5, 4), (6, 5)]
    #points_list = [(100,100),(-66,-85),(11,-22)]

    root = tk.Tk()
    ex = Example(GiftWrap(points_list))
    print(ex.PointList)
    root.geometry(str(MAX_WIDTH) + "x" + str(MAX_HEIGHT))
    root.mainloop()


if __name__ == '__main__':
    main()
