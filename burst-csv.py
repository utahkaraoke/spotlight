import csv
import re

def squishSpaces(text):
  return re.sub(' +', ' ', text)

def removePrefix(text, prefix):
  if text.startswith(prefix):
    text = re.sub('^' + re.escape(prefix), '', text).strip()
  return text

def readCsv(file):
  artists = {}
  with open(file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
      title = squishSpaces(row[0]).strip()
      artist = squishSpaces(row[1]).strip()
      title = removePrefix(title, artist + ' - ')
      title = removePrefix(title, artist + ' ')
      if len(artist) > 0 and len(title) > 0:
        if not artist in artists:
          artists[artist] = []
        if not title in artists[artist]:
          artists[artist].append(title)
  return artists

def dumpArtists(file):
  artists = readCsv(file)
  print "{0} artists".format(len(artists))

  for artist in artists:
    print "Artist: {0}".format(artist)
    for title in artists[artist]:
      print "    {0}".format(title)

dumpArtists('spotlight.csv')
