#!/usr/bin/python

from bokeh.io import show
from bokeh.layouts import widgetbox, column
from bokeh.models import GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d
from bokeh.models.widgets import Slider
from bokeh.plotting import curdoc


GOOGLE_MAPS_API_KEY = "AIzaSyCrLhP6CVJ-t33LZ5jPLBAmi5ThXmUgTgo"



class GoogleMapPlot:
	
	def __init__(self, lat, long, zoom):
		map_options = GMapOptions(lat=lat, lng=long, map_type="roadmap", zoom=zoom)

		# For GMaps to function, Google requires you obtain and enable an API key:
		#
		#     https://developers.google.com/maps/documentation/javascript/get-api-key
		#
		# Replace the value below with your personal API key:
		self.plot = GMapPlot(api_key = GOOGLE_MAPS_API_KEY,
							 x_range = Range1d(), 
							 y_range = Range1d(), 
							 map_options = map_options,
							 width = 1000,
							 height = 600,
							 toolbar_location = "above")

		self.layout = column(self.plot)		


	def show(self):
		curdoc().add_root(self.layout)


	def drawPointsWithCircles(self, data, attrs):
		data = ColumnDataSource(
			data=dict(
				lat = [x[0] for x in data],
				long = [x[1] for x in data],
			)
		)

		defaults = { 'x' : 'long',
					 'y' : 'lat',
					 'size' : 2,
					 'fill_color' : 'blue',
					 'fill_alpha' : 0.8,
					 'line_color' : None }
		defaults.update(attrs)

		circle = Circle(**defaults)

		self.plot.add_glyph(data, circle)
		
		return data


	def updateDataSource(self, source, data):
		source.data = dict(
							lat = [x[0] for x in data],
							long = [x[1] for x in data],
						)
		
		
	def addSlider(self, min, max, step, init, title, callback=None):
		slider = Slider(start=min, end=max, value=init, step=step, title=title)

		slider.on_change('value', self.slider_handler_callback)
		self.sliderCallback = callback
		
		self.layout = column(self.plot, widgetbox(slider))
		

	def slider_handler_callback(self, attr, old, new):
		if hasattr(self, 'sliderCallback') and self.sliderCallback is not None:
			self.sliderCallback(new)
					
		
		

	#plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
	#output_file("gmap_plot.html")

