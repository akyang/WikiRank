import wikipediaapi
import requests

wiki_wiki = wikipediaapi.Wikipedia('en')
S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

# Returns a list of the titles of all locations in the vicinity of a city
def getLocations(city):
    latitude, longitude = get_coordinates(city)
    COORDS = str(latitude) + '|' + str(longitude)

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

def get_coordinates(city):
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

    latitude = coordinates[0]
    longitude = coordinates[1]
    return latitude, longitude

# Returns a city's links in the form of a list
def getLinks(city):
    page = wiki_wiki.page(city)
    return sorted(page.links.keys())


