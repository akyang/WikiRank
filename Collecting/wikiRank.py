import wikipediaapi
import requests
import random
import csv

CITY = "San Francisco"
NUM_VISITS_1 = 5000
NUM_VISITS_2 = 5000

wiki_wiki = wikipediaapi.Wikipedia('en')

# Returns a list of the titles of all locations in the vicinity of a city
def getLocations(city):
	S = requests.Session()

	URL = "https://en.wikipedia.org/w/api.php"

	TITLE = city

	PARAMS = {
	    'action':"query",
	    'prop':"coordinates",
	    'titles': TITLE,
	    'format':"json"
	}

	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()
	PAGES = DATA['query']['pages']

	coordinates = []
	for k, v in PAGES.items():
		coordinates.append(v['coordinates'][0]['lat'])
		coordinates.append(v['coordinates'][0]['lon'])

	lattitude = coordinates[0]
	longitude = coordinates[1]
	COORDS = str(lattitude) + '|' + str(longitude)

	S = requests.Session()

	URL = "https://en.wikipedia.org/w/api.php"

	PARAMS = {
		'action':"query",
		'list':"geosearch",
		'gscoord': COORDS,
		'gsradius':10000,
		'gslimit':500,
		'format':"json"
	}

	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()

	PLACES = DATA['query']['geosearch']

	locations = []
	for place in PLACES:
		locations.append(place['title'])
	return locations

# Returns a city's links in the form of a list
def getLinks(city):
	page = wiki_wiki.page(city)
	return sorted(page.links.keys())

locations = getLocations(CITY)
visits = {}
for location in locations:
	visits[location] = 0

for i in range(NUM_VISITS_1):
	print('Phase 1: ' + str(i))
	location = random.choice(locations)
	links = getLinks(location)
	locationLinks = [l for l in links if l in visits]
	if len(locationLinks) > 0:
		visit = random.choice(locationLinks)
		visits[visit] += 1

sortedLocationKeys = sorted(visits, key=visits.get, reverse=True)

locationsFileName = 'location_rankings_' + CITY + '_' + str(NUM_VISITS_1) + '_' + str(NUM_VISITS_2) + '.csv'
with open(locationsFileName, mode='w') as location_file:
	location_writer = csv.writer(location_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for key in sortedLocationKeys:
		location_writer.writerow([key, str(visits[key])])



weightedLocations = []

for location in visits:
	for i in range(visits[location]):
		weightedLocations.append(location)

topicVisits = {}

for i in range(NUM_VISITS_2):
	print('Phase 2: ' + str(i))
	location = random.choice(weightedLocations)
	links = getLinks(location)
	nonlocationLinks = [l for l in links if l not in visits]
	if len(nonlocationLinks) > 0:
		visit = random.choice(nonlocationLinks)
		if visit in topicVisits:
			topicVisits[visit] += 1
		else:
			topicVisits[visit] = 1

sortedTopicKeys = sorted(topicVisits, key=topicVisits.get, reverse=True)

topicsFileName = 'topic_rankings_' + CITY + '_' + str(NUM_VISITS_1) + '_' + str(NUM_VISITS_2) + '.csv'
with open(topicsFileName, mode='w') as topic_file:
	topic_writer = csv.writer(topic_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for key in sortedTopicKeys:
		topic_writer.writerow([key, str(topicVisits[key])])
