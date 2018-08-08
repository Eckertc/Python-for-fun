## RuneScapeLogin.py logs a user into RuneScape once
## the app is open/in-focus and script is ran with login arguments
## Usage Example: RuneScapeLogin.py MyMail@gmail.net BigWombo192!

import pyautogui as pag
import sys
import time

USERBUTTON = 'Images/ExistingUserButton.png'
LOGINBUTTON = 'Images/LoginButton.png'
PLAYBUTTON = 'Images/PlayButton.png'
TRYAGAINBUTTON = 'Images/TryAgainButton.png'
CANCELBUTTON = 'Images/CancelButton.png'
LOGINBOX = 'Images/LoginBox.png'
PASSBOX = 'Images/PassBox.png'
WORLD301BOX = 'Images/World301.png'
WELCOMEMESSAGE = 'Images/WelcomeMessage.png'
BADREALMFLAG = 'Images/NeedMemberLoginFlag.png'
INVALIDLOGFLAG = 'Images/InvalidLogin.png'

RETINA = True

def FindImage(Display, IMGPATH):
    ImgCord = pag.locateOnScreen(IMGPATH)
    if ImgCord == None:
        return None
    elif Display == True:
        return [x/2 for x in ImgCord]
    else:
        return ImgCord

def LoginFunction():
    # first find and click existing user button
    ExistingUserButton = FindImage(RETINA, USERBUTTON)
    pag.click(pag.center(ExistingUserButton))

    # next input username and password
    LoginBox = FindImage(RETINA, LOGINBOX)
    pag.click([pag.center(LoginBox)[0] + 50, pag.center(LoginBox)[1]])
    # clear whatever was there
    for i in range(0, 35):
        pag.press('backspace')
    pag.typewrite(sys.argv[1], 0.12)

    # repeat for password
    PassBox = FindImage(RETINA, PASSBOX)
    pag.click([pag.center(PassBox)[0] + 50, pag.center(PassBox)[1]])
    # clear whatever was there
    for i in range(0, 35):
        pag.press('backspace')
    pag.typewrite(sys.argv[2], 0.12)

    # Attempt to login
    LoginButton = FindImage(RETINA, LOGINBUTTON)
    pag.click(pag.center(LoginButton))

    # see if we got in
    while True:
        # keep checking for the Welcome Message
        WelcomeMessage = FindImage(RETINA, WELCOMEMESSAGE)
        # keep checking for Invalid Realm
        BadRealmFlag = FindImage(RETINA, BADREALMFLAG)
        # keep checking for Invalid Login
        InvalidLogFlag = FindImage(RETINA, INVALIDLOGFLAG)

        # Select a non-member realm and attempt login
        if BadRealmFlag != None:
            pag.click([pag.center(LoginButton)[0] - 250, pag.center(LoginButton)[1] + 170])
            while True:
                World301 = FindImage(RETINA, WORLD301BOX)
                if World301 != None:
                    break
            pag.click(pag.center(World301))
            pag.click(pag.center(LoginButton))

        # Acknowledge Invalid Login and reset
        if InvalidLogFlag != None:
            TryAgainButton = FindImage(RETINA, TRYAGAINBUTTON)
            pag.click(pag.center(TryAgainButton))
            CancelButton = FindImage(RETINA, CANCELBUTTON)
            pag.click(pag.center(CancelButton))
            print("Wrong Username/Pass")
            print("Try Again")
            exit()

        # Enter Game: you in boii
        if WelcomeMessage != None:
            pag.click(pag.center(LoginButton))
            break

def main():
    if len(sys.argv) < 3:
        print("Username and password arguments required!")
        print("Usage Example: RuneScapeLogin.py MyMail@gmail.net GooDPaSS1!")
        exit()
    else:
        time.sleep(5)
    LoginFunction()

if __name__ == '__main__':
    main()
