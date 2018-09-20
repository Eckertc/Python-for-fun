import cv2
import random
import numpy as np

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

im_gray = cv2.imread("shadedCan.jpeg", cv2.IMREAD_GRAYSCALE)
im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)
SHOW_COLOR = False

height, width = im_gray.shape

print(height/2)
print(width/2)

print(im_color[int(height - 1)][int(width - 1)])
# # map unit square coords to an approiximate bit
# # do this by using x and y from unit sqaure as
# # a percentage from the origin
# x_cord = int((random.random()*2 - 1) * width/2)
# y_cord = int((random.random()*2 - 1) * height/2)
#
# print(str(x_cord) + ' ' + str(y_cord))
# print('color: ' + str(im_color[x_cord][y_cord]))
# red = im_color[x_cord][y_cord][0] * 256 * 256
# green = im_color[x_cord][y_cord][1] * 256
# blue = im_color[x_cord][y_cord][2]
#
# totalHex = red + green + blue
#
# # normalize totalHex
# totalHex = totalHex / 16777215
#
# print(totalHex)
#
# print(str(red) + str(green) + str(blue))

while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    if k == 116:
        if SHOW_COLOR == True:
            SHOW_COLOR = False
        else:
            SHOW_COLOR = True
    elif SHOW_COLOR == False:
        cv2.imshow('Displaying: COLORMAP_JET',im_gray)
    else:
        cv2.imshow('Displaying: COLORMAP_JET',im_color)

cv2.destroyAllWindows()
