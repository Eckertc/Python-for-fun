# server application for handling mouse clicks
# and calculating APM

import socket
import sys
import time
import math

print('=======================================================')
print('= Mouse clicks are now ready to recv!                 =')
print('= Click in the top left corner of our screen to exit. =')
print('=======================================================')

clicks = 0
# convert to minutes
timeStart = time.time() / float(60)
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    # listen for clicks
    data, address = sock.recvfrom(4096)

    if(data == b'EXIT'):
        exit(0)

    clicks = clicks + 1

    # calculate APM based on runtime
    timeCur = time.time()  / float(60)
    timeRun = timeCur - timeStart
    APM = math.floor(clicks/timeRun)

    print('APM for session is: ' + str(APM))
