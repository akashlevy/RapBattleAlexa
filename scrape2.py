import re, sys
import requests
import nltk
from bs4 import BeautifulSoup

f = open('textTest123','w')

text_file = open("testRapperList.txt", "r")
lines = text_file.readlines()
print lines
for line in lines:
    url = 'http://www.lyrics.com/' + line
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    gdata = soup.find_all('div',{'class':'row'})

    eminemLyrics = []

    for item in gdata:
        title = item.find_all('a',{'itemprop':'name'})[0].text
        lyricsdotcom = 'http://www.lyrics.com'
        for link in item('a'):
            try:
                lyriclink = lyricsdotcom+link.get('href')
                req = requests.get(lyriclink)
                lyricsoup = BeautifulSoup(req.content, "lxml")
                lyricdata = lyricsoup.find_all('div',{'id':re.compile('lyric_space|lyrics')})[0].text
                if "name will be printed as part of the credit" not in lyricdata:
                    lyricdata = lyricdata[:-28]
                    f.write(lyricdata)
            except:
                pass
    # titles = [i[0] for i in eminemLyrics]
    # print titles
f.close()