#! /usr/bin/env python3
# lucky.py opens tabs of the first couple search results via command line

import sys
import requests
import webbrowser
import bs4

print('Googling...')
res = requests.get('http://www.google.com/search?q=' + ' '.join(sys.argv[1:]))
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')

linkElems = soup.select('.r a')

numOpen = min(5, len(linkElems))
for i in range(numOpen):
    webbrowser.open('http://google.com' + linkElems[i].get('href'))



