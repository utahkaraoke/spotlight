import csv

artists = {}

i = 0
with open('spotlight.csv', 'r') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in reader:
	title = row[0]
	artist = row[1]
	if not artist in artists:
		artists[artist] = []
	artists[artist].append(title)

print "{0} artists".format(len(artists))
