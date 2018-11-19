import wikipediaapi
import requests

CITY = "San Francisco"

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

print(getLocations(CITY))