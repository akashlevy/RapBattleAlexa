import os, glob
from os import listdir
from os.path import isfile, join

def remove_short_sentences(fileA, name):
  lines = fileA.readlines()
  f = open(name,'w')
  import string
  exclude = set(string.punctuation)
  for line in lines:
    if(len(line.split(' ')) > 4):
      line = ''.join(ch for ch in line if ch not in exclude)
      line = ' '.join(line.split()) + '\n'
      f.write(line)
  f.close()

## **make sure theres not a \n in the end of your file name. you'll have to manually remove it **

## MOVE into cleanSongs directory to make work

path = '*'   
files=glob.glob(path)   
for file in files:
  name = file   
  text_file = open(file, 'r')
  remove_short_sentences(text_file, name)