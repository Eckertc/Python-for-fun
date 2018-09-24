# client application for detecting mouse clicks
# dependent on pynput, install with: pip3 install pynputs

import sys
import socket
from pynput import mouse

def on_click(x, y, button, pressed):
    ## spun off thread
    if pressed:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = ('localhost', 10000)
        if(x < 0.5 and y < 0.5):
            # send exit packet
            message = b'EXIT'
        else:
            message = b'Click Detected'

        try:
            # Send data
            print('Click Detected')
            sent = sock.sendto(message, server_address)
        finally:
            sock.close()
            if(x < 0.5 and y < 0.5):
                exit(0)


# Collect events until released
with mouse.Listener(on_click=on_click) as listener:
    print('=======================================================')
    print('= Mouse clicks are now being recorded!                =')
    print('= Click in the top left corner of our screen to exit. =')
    print('=======================================================')
    listener.join()
