import re, sys
import requests
import nltk
from bs4 import BeautifulSoup

text_file = open("rappers.txt", "r")
lines = text_file.readlines()

for line in lines:
    f = open(line,'w')
    url = 'http://www.lyrics.com/' + line
    r = requests.get(url)
    #gets all song names
    soup = BeautifulSoup(r.content, "lxml")
    gdata = soup.find_all('div',{'class':'row'})
    #for each song get lyrics
    for item in gdata:
        title = item.find_all('a',{'itemprop':'name'})[0].text
        lyricsdotcom = 'http://www.lyrics.com'
        for link in item('a'):
            try:
                lyriclink = lyricsdotcom+link.get('href')
                req = requests.get(lyriclink)
                lyricsoup = BeautifulSoup(req.content.decode('utf-8','ignore'))
                lyricdata = lyricsoup.find_all('div',{'id':re.compile('lyric_space|lyrics')})[0].get_text()
                #does not add song if no one has added the lyrics too it yet
                if "name will be printed as part of the credit" not in lyricdata:
                    ##removes "Submit lyrics text"
                    lyricdata = lyricdata[:-28]
                    f.write(lyricdata.encode("utf-8"))
            except:
                pass
    f.close()
