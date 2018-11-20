import sys
import csv
import plotly
import plotly.graph_objs as go
import WikiUtils

city = "Berkeley, California"
scale = 5
color = "rgb(255, 0, 0)"
num_visits = [500, 1000, 5000]
num_topics = [500, 1000, 5000]

def bubble_plot(filename, v, t):
    base_lat, base_lon = WikiUtils.get_coordinates(city)

    data = get_data(filename)
    layout = go.Layout(
                title="{0} {1},{2}".format(city, v, t),
                geo=dict(
                    resolution = 50,
                    scope = "north america", 
                    showframe = False,
                    showcoastlines = True,
                    coastlinecolor = 'rgb(255, 255, 255)',
                    countrycolor = 'rgb(255, 255, 255)',
                    projection = dict(
                        type='mercator',
                        scale=300
                    ),
                    center=dict(
                         lon=base_lon,
                         lat=base_lat
                    ),
                    showland=True,
                    landcolor="rgb(249, 240, 222)",
                    showocean=True,
                    oceancolor="rgb(128, 176, 252)",
                    showrivers = True,
                    showsubunits = False,
                    domain = dict(
                        x = [0, 1],
                        y = [0, 1]
                    )
                ),
            )

    figure = {'data': data, 'layout': layout}
    filename = filename[14:-4]
    plotly.offline.plot(figure, filename='plots/'+filename+'.html', image='png', image_filename=filename, auto_open=True)

def get_data(filename):
    lons = []
    lats = []
    text = []
    scores = []
    colors = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for _ in range(100):
            row = next(reader)
            print(row)
            location, score = row[0], int(row[1])
            lat, lon = WikiUtils.get_coordinates(location)
            lats.append(lat)
            lons.append(lon)
            text.append(location)
            scores.append(score / scale)
            colors.append(color)

    data = dict(
                type='scattergeo',
                mode="markers+text",
                lat=lats,
                lon=lons,
                text=text[:10],
                hovertext=text,
                marker=dict(
                    size=scores,
                    color=colors,
                    line=dict(width=0)
                )
            )

    return [data]

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        v, t = int(args[1]), int(args[2])
        filename = "data/PageRank/{0}_{1}_{2}.csv".format(city.replace(' ', ''), v, t)
        bubble_plot(filename, v, t)
    else:
        for v in num_visits:
            for t in num_topics:
                filename = "data/PageRank/{0}_{1}_{2}.csv".format(city.replace(' ', ''), v, t)
                bubble_plot(filename, v, t)

