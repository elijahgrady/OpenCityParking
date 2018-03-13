#!/usr/bin/python


# STEP 1: BASIC BOKEH
'''
from random import randint

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Circle

# data souce is what bokeh uses to plot points
# put things in a bracket in python to generate a list

data = ColumnDataSource(
	data=dict(
		x = [randint(0, 10) for x in range(10)],
		y = [randint(0, 10) for x in range(10)],
	)
)

attrs = { 'x' : 'x',
 		  'y' : 'y',
		  'size' : 10,
		  'fill_color' : 'blue',
		  'fill_alpha' : 0.8,
		  'line_color' : None }

# renders any nummber of circle on the screen
circle = Circle(**attrs)

fig = figure(title = "Random X, Y")
fig.add_glyph(data, circle)

#renders to htmml and opens in your broswer path
show(fig)




# STEP 2: CSV DATA

import csv

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Circle

SAMPLE_XY_FILE = 'data/random-xy.csv'


csvdata = []
with open(SAMPLE_XY_FILE, 'r') as csvfile:
	reader = csv.reader(csvfile)
	csvdata = [row for row in reader]


data = ColumnDataSource(
	data=dict(
		x = [int(x[0]) for x in csvdata],
		y = [int(y[1]) for y in csvdata]
	)
)

attrs = { 'x' : 'x',
 		  'y' : 'y',
		  'size' : 10,
		  'fill_color' : 'blue',
		  'fill_alpha' : 0.8,
		  'line_color' : None }

circle = Circle(**attrs)

fig = figure(title = "Random X, Y")
fig.add_glyph(data, circle)

show(fig)




# STEP 3: GOOGLE MAPS

from bokeh.io import show
from bokeh.models import GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d


# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
GOOGLE_MAPS_API_KEY = "AIzaSyA-nZCJSy1Fy66bTpsk0IZvsz6XBmci-bk"
SAN_DIEGO_COORDINATE = (32.712, -117.1611)
DEFAULT_ZOOM = 16


lat = SAN_DIEGO_COORDINATE[0]
long = SAN_DIEGO_COORDINATE[1]

map_options = GMapOptions(lat=lat, lng=long, map_type="roadmap", zoom=DEFAULT_ZOOM)


plot = GMapPlot(api_key = GOOGLE_MAPS_API_KEY,
				x_range = Range1d(),
				y_range = Range1d(),
				map_options = map_options,
				width = 1000,
				height = 600,
				toolbar_location = "above")

show(plot)
'''



# STEP 4: PLOTTING MAP POINTS

import csv

from bokeh.io import show
from bokeh.models import GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d


PARKING_METER_LOCATION_DATA_FILE = "data/treas_parking_meters_loc_datasd.csv"

GOOGLE_MAPS_API_KEY = "AIzaSyCrLhP6CVJ-t33LZ5jPLBAmi5ThXmUgTgo"
SAN_DIEGO_COORDINATE = (32.716, -117.1611)
DEFAULT_ZOOM = 15


# Data Preparation

locations = []
with open(PARKING_METER_LOCATION_DATA_FILE, 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	locations = [row for row in reader]

#import json
#print(json.dumps(locations, indent=4, sort_keys=True))

locations = list(filter(lambda x: float(x['latitude']) != 0 and float(x['longitude']) != 0, locations))

#print(json.dumps(locations, indent=4, sort_keys=True))


data = ColumnDataSource(
	data=dict(
		lat = [float(loc['latitude']) for loc in locations],
		long = [float(loc['longitude']) for loc in locations]
	)
)


# Plotting Setup

map_options = GMapOptions(lat=SAN_DIEGO_COORDINATE[0],
						  lng=SAN_DIEGO_COORDINATE[1],
						  map_type="roadmap",
						  zoom=DEFAULT_ZOOM)

plot = GMapPlot(api_key = GOOGLE_MAPS_API_KEY,
				x_range = Range1d(),
				y_range = Range1d(),
				map_options = map_options,
				width = 1000,
				height = 600,
				toolbar_location = "above")


attrs = { 'x' : 'long',
 		  'y' : 'lat',
		  'size' : 3,
		  'fill_color' : 'blue',
		  'fill_alpha' : 0.8,
		  'line_color' : None }

circle = Circle(**attrs)


plot.add_glyph(data, circle)

show(plot)



# bokeh serve start.py 
# STEP 5: REFACTOR

from gmapplot import GoogleMapPlot
from parking import ParkingMeterLocations


SAN_DIEGO_COORDINATE = (32.712, -117.1611)
DEFAULT_ZOOM = 16
BOUNDS_TOP_LEFT = (32.716, -117.164)
BOUNDS_BOTTOM_RIGHT = (32.705749, -117.157)


# Our main program when executed at command line
plot = GoogleMapPlot(SAN_DIEGO_COORDINATE[0], SAN_DIEGO_COORDINATE[1], DEFAULT_ZOOM)

poles = ParkingMeterLocations.getLocationsInRegion({ 'lat': BOUNDS_TOP_LEFT[0],
													 'long': BOUNDS_TOP_LEFT[1] },
												   { 'lat': BOUNDS_BOTTOM_RIGHT[0],
													 'long': BOUNDS_BOTTOM_RIGHT[1] })

drawnXY = [(x['lat'], x['long']) for x in poles]

plot.drawPointsWithCircles(drawnXY, { 'fill_color' : 'blue',
									  'size' : 3 })

plot.show()



'''
# STEP 6: INTERACTION

from gmapplot import GoogleMapPlot
from parking import ParkingMeterLocations, ParkingMeterTransaction


SAN_DIEGO_COORDINATE = (32.712, -117.1611)
DEFAULT_ZOOM = 16
BOUNDS_TOP_LEFT = (32.716, -117.164)
BOUNDS_BOTTOM_RIGHT = (32.705749, -117.157)


# Our main program when executed at command line
plot = GoogleMapPlot(SAN_DIEGO_COORDINATE[0], SAN_DIEGO_COORDINATE[1], DEFAULT_ZOOM)

# Load the parking meter transactions before we start
ParkingMeterTransaction.getTransactions()

poles = ParkingMeterLocations.getLocationsInRegion({ 'lat': BOUNDS_TOP_LEFT[0],
													 'long': BOUNDS_TOP_LEFT[1] },
												   { 'lat': BOUNDS_BOTTOM_RIGHT[0],
													 'long': BOUNDS_BOTTOM_RIGHT[1] })
drawnXY = [(x['lat'], x['long']) for x in poles]

datasource = plot.drawPointsWithCircles(drawnXY, { 'fill_color' : 'blue',
							  					   'size' : 3 })



def updatePlot(day):
	transactions = set(map(lambda t: t['pole_id'], ParkingMeterTransaction.getTransactionsForDay(day)))

	drawnPoles = filter(lambda p: p['pole'] in transactions, poles)
	drawnXY = [(x['lat'], x['long']) for x in drawnPoles]

	plot.updateDataSource(datasource, drawnXY)

	#import datetime
	#print((datetime.datetime(2017, 1, 1) + datetime.timedelta(day - 1)).strftime('%A'))


plot.addSlider(1, 365, 1, 1, "Day", updatePlot)

plot.show()
'''

'''

# STEP 7: HEATMAP W/ INTERACTION

from gmapplot import GoogleMapPlot
from parking import ParkingMeterLocations, ParkingMeterTransaction
from itertools import groupby
from functools import reduce
from math import floor, ceil
import operator
import colorsys


SAN_DIEGO_COORDINATE = (32.712, -117.1611)
DEFAULT_ZOOM = 16
BOUNDS_TOP_LEFT = (32.716, -117.164)
BOUNDS_BOTTOM_RIGHT = (32.705749, -117.157)
MAX_OCCUPIED_HOURS = 10  # 8AM - 6PM
HEATMAP_GRANULARITY = 10
HEATMAP_SCALING = 3
PRICE_PER_HOUR = 1.25



def generateColorMap(count):
	def rgbToHex(red, green, blue):
		return '#{:02X}{:02X}{:02X}'.format(red, green, blue)

	dHue = .33 / float(count - 1)
	colorMap = []
	for i in range(count):
		colorMap += [rgbToHex(*map(lambda v: int(255 * v), colorsys.hls_to_rgb(.33 - (dHue * float(i)), .5, 1)))]

	return colorMap


def transactionDuration(tran):
	amt = float(tran['trans_amt']) / 100
	return amt / PRICE_PER_HOUR



# Our main program when executed at command line
plot = GoogleMapPlot(SAN_DIEGO_COORDINATE[0], SAN_DIEGO_COORDINATE[1], DEFAULT_ZOOM)

# Load the parking meter transactions before we start
ParkingMeterTransaction.getTransactions()

poles = ParkingMeterLocations.getLocationsInRegion({ 'lat': BOUNDS_TOP_LEFT[0],
													 'long': BOUNDS_TOP_LEFT[1] },
												   { 'lat': BOUNDS_BOTTOM_RIGHT[0],
													 'long': BOUNDS_BOTTOM_RIGHT[1] })

colorMap = generateColorMap(HEATMAP_GRANULARITY)

datasources = [plot.drawPointsWithCircles([], { 'fill_color' : colorMap[i],
							  					'size' : 4 }) for i in range(HEATMAP_GRANULARITY)]
print(colorMap)

def updatePlot(day):
	transactions = ParkingMeterTransaction.getTransactionsForDay(day)

	polesByHeat = [[] for i in range(HEATMAP_GRANULARITY)]
	for k, g in groupby(transactions, lambda t: t['pole_id']):
		hours = reduce(operator.add, map(lambda t: transactionDuration(t), g), 0)
		i = min(floor(HEATMAP_SCALING * hours / MAX_OCCUPIED_HOURS * HEATMAP_GRANULARITY), HEATMAP_GRANULARITY - 1)
		polesByHeat[i] += [k]

	for i in range(HEATMAP_GRANULARITY):
		drawnPoles = filter(lambda p: p['pole'] in polesByHeat[i], poles)
		drawnXY = [(x['lat'], x['long']) for x in drawnPoles]
		plot.updateDataSource(datasources[i], drawnXY)


plot.addSlider(1, 365, 1, 1, "Day", updatePlot)

plot.show()
'''

# REACHED END OF FILE
