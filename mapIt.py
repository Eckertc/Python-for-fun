# mapIt.py - Launches a map in the browser using an address from the command line or clipboard

import sys
import webbrowser
import pyperclip
#from webbrowser import pyperclip
if len(sys.argv) > 1:
    #grab address from command line
    address = ' '.join(sys.argv[1:])
else:
    #grab address from keeb
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address)
