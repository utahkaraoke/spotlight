import csv
import re

def squishSpaces(text):
  return re.sub(' +', ' ', text)

def removePrefix(text, prefix):
  if text.startswith(prefix):
    text = re.sub('^' + re.escape(prefix), '', text).strip()
  return text

def readCatalog(file):
  catalog = {}
  with open(file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
      title = squishSpaces(row[0]).strip()
      artist = squishSpaces(row[1]).strip()
      title = removePrefix(title, artist + ' - ')
      title = removePrefix(title, artist + ' ')
      if len(artist) > 0 and len(title) > 0:
        if not artist in catalog:
          catalog[artist] = []
        if not title in catalog[artist]:
          catalog[artist].append(title)
  return catalog

def dumpArtists(catalog):
  print "{0} artists".format(len(catalog))

  for artist in catalog:
    print "Artist: {0}".format(artist)
    for title in catalog[artist]:
      print "    {0}".format(title)

catalog = readCatalog('spotlight.csv')
dumpArtists(catalog)
