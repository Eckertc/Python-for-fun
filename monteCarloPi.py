## monteCarloPi.py calculates the value of PI by
## using a simple implementation of the monte carlo
## method.

import random
import math
from decimal import *

ITTERATIONS = 10000
counter = 0

getcontext().prec = 11

for i in range(0, ITTERATIONS) :
    check = math.sqrt( math.pow(random.random() - float(0.5), 2) + math.pow(random.random() - float(0.5), 2))
    if check <= 0.5 :
        counter = counter + 1

# A = PI * r^2 area of a circle
# counter/itter = A
# here r = 0.5
# so, A * 4 = PI

print("caluclated value : " + str(Decimal(counter/ITTERATIONS * 4)))
print("compared against : " + str(math.pi))
