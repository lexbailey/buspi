#! /usr/bin/env python

import urllib2
import json
from AdafruitFourCharAlphanumeric import FourCharDisplay
import time
import serial
ser = serial.Serial('/dev/ttyAMA0', 9600)

stop_naptan = "32900009"
stop_name = "Plantation Drive Bus Stop"
url = "http://bitofahack.com/getbusdata.php?stop=" + stop_naptan
#url = "http://thewayitusedtobe.co.uk/getbusdata.php?stop=" + stop_naptan
print url
redDisplay = FourCharDisplay(0x71)
blueDisplay = FourCharDisplay(0x70)

#redefine character 16 to be 'in'
blueDisplay.ASCII_LOOKUP[16] = 0b0001000010010100
#This lets the word 'min' fit in two chars

# _ _     _
#| | | | | |
#
#----- -----
#Char1 Char2
# 'm'   'in'

while 1:

	try:

		jsonText = urllib2.urlopen(url).read()
		jsonInfo = json.loads(jsonText)
		if "error" in jsonInfo:
			print jsonInfo["error"]

			if jsonInfo["error"] == "no_error":

				redDisplay.write(str(jsonInfo['data'][0]['route']));
				est = jsonInfo['data'][0]['est']
				est2 = ''
				for c in est:
					#ignore colons, spaces, 's', 'i' and 'n'
					if (c != ' ') and (c != 's')  and (c != ':') and (c != 'i') and (c != 'n'):
						est2 = est2+c
					#Turn 'i' into our custom 'in' character
					if (c == 'i'):
						est2 = est2+chr(16)
				blueDisplay.write(est2);
				ser.write(stop_name)
				time.sleep(10)
				ser.write(stop_name)
				time.sleep(10)
				ser.write(stop_name)
				time.sleep(10)
			else:
				if jsonInfo["error"] == "no_busses_within_hour":
					redDisplay.write("No")
					blueDisplay.write("Bus")
				elif (jsonInfo["error"] == "empty_get") or (jsonInfo["error"] == "scrape_error"):
					redDisplay.write("ERR")
					blueDisplay.write("SERV")
				elif jsonInfo["error"] == "no_stop_specified":
					redDisplay.write("ERR")
					blueDisplay.write("USR")
				else:
					redDisplay.write("ERR")
					blueDisplay.write("????")

				ser.write("[!]")
				time.sleep(10)
				ser.write("[!]")
				time.sleep(10)
				ser.write("[!]")
				time.sleep(10)
				
	except:
		time.sleep(30)

