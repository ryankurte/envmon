#!/usr/bin/env python

from Adafruit_BME280 import *
import time
import datetime
import urllib, httplib
import socket
import os

# Setup constants
server = os.environ['ENVMON_SERVER']
pk = os.environ['ENVMON_PUBKEY']
sk = os.environ['ENVMON_PRIKEY']

fields = ["temperature", "pressure", "humidity"]


# Connect to sensor
sensor = BME280(mode=BME280_OSAMPLE_8)
hostname = socket.gethostname();


while 1:
	# Fetch sensor data
	degrees = sensor.read_temperature()
	pascals = sensor.read_pressure()
	hectopascals = pascals / 100
	humidity = sensor.read_humidity()

	print 'Timestamp = {0:0.3f}'.format(sensor.t_fine)
	print 'Temp      = {0:0.3f} deg C'.format(degrees)
	print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
	print 'Humidity  = {0:0.2f} %'.format(humidity)

	# Build data object
	data = {}
	data[fields[0]] = '{0:0.3f}'.format(degrees)
	data[fields[1]] = '{0:0.3f}'.format(hectopascals)
	data[fields[2]] = '{0:0.2f}'.format(humidity)

	# Encode URL to HTTP params
	params = urllib.urlencode(data)

	# Build headers
	headers = {}
	headers["Content-Type"] = "application/x-www-form-urlencoded"
	headers["Connection"] = "Close"
	headers["Content-Length"] = len(params)
	headers["Phant-Private-Key"] = sk

	# Create connection
	c = httplib.HTTPConnection(server)
	c.request("POST", "/input/" + pk + ".txt", params, headers)
	r = c.getresponse()
	print r.status, r.reason
	
	time.sleep(10 * 60)


