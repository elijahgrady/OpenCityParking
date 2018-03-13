#!/usr/bin/python

import csv
from itertools import groupby
import datetime


PARKING_METER_LOCATION_DATA_FILE = "data/treas_parking_meters_loc_datasd.csv"
PARKING_METER_TRANSACTION_DATA_FILE = "data/treas_parking_payments_2017_datasd-gaslamp.csv"


class ParkingMeterLocations:

	@classmethod
	def getLocations(cls):
		if not hasattr(cls, 'locations'):
			locations = []

			with open(PARKING_METER_LOCATION_DATA_FILE, 'r') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					row['lat'] = float(row['latitude'])
					row['long'] = float(row['longitude'])
					locations += [row]
						
			cls.locations = locations
			
		return cls.locations


	@classmethod
	def getPoleLocation(cls, pole):
		if not hasattr(cls, 'poles'):
			locations = cls.getLocations()	# make sure locations are loaded
			poles = {x['pole'] : x for x in locations}
			cls.poles = poles

		return cls.poles[pole] if pole in cls.poles else None
		
		
	@classmethod
	def getLocationsInRegion(cls, topLeft, bottomRight):
		locations = cls.getLocations()
		return list(filter(lambda l: l['lat'] <= topLeft['lat'] and l['lat'] >= bottomRight['lat'] and
								 	 l['long'] >= topLeft['long'] and l['long'] <= bottomRight['long'], locations))




class ParkingMeterTransaction:

	@classmethod
	def getTransactions(cls):
		if not hasattr(cls, 'transactions'):
			transactions = []
			with open(PARKING_METER_TRANSACTION_DATA_FILE, 'r') as csvfile:
				reader = csv.DictReader(csvfile)
				transactions = [row for row in reader]

			cls.transactions = transactions
			
		return cls.transactions


	@classmethod
	def getTransactionsForDay(cls, day):
		if not hasattr(cls, 'transactionsByDay'):
			transactions = cls.getTransactions()
			byDay = groupby(transactions, lambda t: t['trans_start'][:10])
			cls.transactionsByDay = dict((k, list(g)) for k, g in byDay)
		
		key = (datetime.datetime(2017, 1, 1) + datetime.timedelta(day - 1)).strftime('%Y-%m-%d')

		return cls.transactionsByDay[key] if key in cls.transactionsByDay else []
		
