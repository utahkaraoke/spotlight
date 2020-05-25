import csv
import os
import re
import shutil

def squishSpaces(text):
  return re.sub(' +', ' ', text)

def removePrefix(text, prefix):
  if text.startswith(prefix):
    text = re.sub('^' + re.escape(prefix), '', text).strip()
  return text

def mergeTitles(catalog, artist, titleList):
  for title in titleList:
    if not title in catalog[artist]:
      catalog[artist].append(title)

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

def mergeArtists(catalog):
  for artist in catalog:
    if ', ' in artist:
      (lastName, firstName) = artist.split(', ', 1)
      otherArtist = firstName + ' ' + lastName
      if otherArtist in catalog:
        mergeTitles(catalog, artist, catalog[otherArtist])
        mergeTitles(catalog, otherArtist, catalog[artist])
  return catalog

def writeArtist(destDir, artist, catalog):
  for title in sorted(catalog[artist], key=str.lower):
    print "    {0}".format(title)

def dumpArtists(destDir, catalog):
  print "{0} artists".format(len(catalog))
  shutil.rmtree(destDir, True)
  os.mkdir(destDir)

  for artist in sorted(catalog.keys(), key=str.lower):
    print "{0}".format(artist)
    writeArtist(destDir, artist, catalog)

def keywordInContext(list):
  kwic = {}
  for item in list:
    index = 0
    itemWords = item.split(' ')
    for index in range(len(itemWords)):
      key = itemWords[index].lower()
      if not key in kwic:
        kwic[key] = []
      entry = [ ' '.join(itemWords[0:index-1]) if index > 0 else '', itemWords[index], ' '.join(itemWords[index+1:]) if index+1 < len(itemWords) else '' ]
      if not entry in kwic[key]:
        kwic[key].append(entry)
  return kwic

def printArtistKeywordIndex(kwic):
  for key in sorted(kwic.keys()):
    for entry in kwic[key]:
      print "{0:>32} {1} {2}".format(entry[0], entry[1], entry[2])

catalog = mergeArtists(readCatalog('spotlight.csv'))
destDir = 'C:/tmp/spotlight'
printArtistKeywordIndex(keywordInContext(sorted(catalog.keys(), key=str.lower)))
# dumpArtists(destDir, catalog)
