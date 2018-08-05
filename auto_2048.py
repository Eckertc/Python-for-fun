# auto_2048.py - automatically plays 2048 in a firefox browser

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Firefox()
browser.get('https://gabrielecirulli.github.io/2048/')

elem = browser.find_element_by_tag_name('html')

highScore = 0
finCount = 0
while finCount < 4:
    elem.send_keys(Keys.UP)
    elem.send_keys(Keys.RIGHT)
    elem.send_keys(Keys.DOWN)
    elem.send_keys(Keys.LEFT)

    try:
        reElem = browser.find_element_by_class_name('retry-button')
        reElem.click()
        finCount += 1
        score = browser.find_element_by_class_name('scores-container')

        if highScore < int((score.text).replace('0 ', '')):
            highScore = int((score.text).replace('0 ', ''))
            print('New High Score! ' + str(highScore))
    except:
        time.sleep(.001)

browser.quit()
