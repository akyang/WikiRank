import sys
import random
import csv
import WikiUtils
import time

city = "Berkeley, California"
num_visits = [500, 1000, 5000]
num_topics = [500, 1000, 5000]

def crawl(city, n):
    locations = WikiUtils.getLocations(city)
    if city in locations:
        locations.remove(city)
    visits = {}
    for location in locations:
        visits[location] = 0
    ts1 = time.time()
    for i in range(n):
        location = random.choice(locations)
        links = WikiUtils.getLinks(location)
        locationLinks = [l for l in links if l in visits]
        if len(locationLinks) > 0:
            visit = random.choice(locationLinks)
            visits[visit] += 1
    ts2 = time.time()
    print("{0} {1}: PageRank took {2} seconds".format(city, n, ts2-ts1))
    return visits

def rank_topics(visits, n):
    weightedLocations = []
    for location in visits:
        for i in range(visits[location]):
            weightedLocations.append(location)

    topicVisits = {}
    ts1 = time.time()
    for i in range(n):
        location = random.choice(weightedLocations)
        links = WikiUtils.getLinks(location)
        nonlocationLinks = [l for l in links if l not in visits and ':' not in l and l != city]
        nonlocationLinks.remove("Geographic coordinate system")
        if len(nonlocationLinks) > 0:
            visit = random.choice(nonlocationLinks)
            if visit in topicVisits:
                topicVisits[visit] += 1
            else:
                topicVisits[visit] = 1
    ts2 = time.time()
    print("{0} {1}: Topic Rank took {2} seconds".format(city, n, ts2-ts1))
    return topicVisits

def to_csv(data, city, num_visits, num_topics, phase):
    sortedLocationKeys = sorted(data, key=data.get, reverse=True)
    locationsFileName = 'data/{0}/{1}_{2}_{3}.csv'.format(phase, city.replace(' ', ''), num_visits, num_topics)
    with open(locationsFileName, mode='w') as location_file:
        location_writer = csv.writer(location_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in sortedLocationKeys:
            location_writer.writerow([key, str(data[key])])

def run(city, v, t):
    t1 = time.time()
    print("Starting {0} {1} {2}...".format(city, v, t))
    visits = crawl(city, v)
    to_csv(visits, city, v, t, "PageRank")
    topic_visits = rank_topics(visits, t)
    to_csv(topic_visits, city, v, t, "Topics")
    print("Finished {0} {1} {2}.".format(city, v, t))
    t2 = time.time()
    print("TOTAL TIME: {} seconds\n".format(t2 - t1))

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        v = int(args[1])
        t = int(args[2])
        run(city, v, t)
    else:
        for v in num_visits:
            for t in num_topics:
                run(city, v, t)
