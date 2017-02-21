#!/usr/bin/python3

from grip import GripPipeline
p = GripPipeline()

import cv2
import time
import math
import os
import statistics
print("Completed Imports")

FOVTangent = math.tan(math.radians(26))
focalLength = 320/FOVTangent

def initCamera():
	os.system("v4l2-ctl -c exposure_auto=1 -c exposure_absolute=5")
	global capture
	capture = cv2.VideoCapture(0)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
	print("Initialized Camera")

from networktables import NetworkTables
NetworkTables.initialize(server='roborio-467-frc.local')
gyroTable = NetworkTables.getTable('Sensors on Pi')
#NetworkTables.initialize(server='10.0.1.18') #Nathan's IP Address
table = NetworkTables.getTable('SmartDashboard')
time.sleep(1.0) # Give it time to start working
table.putNumber("gyro", 0.0)
print("Initialized Table")

# f = open('dataFile', 'r+')
capture = None
initCamera()
last_time = time.time()*1000
print("Starting Loop")
while True:
	time.sleep(1.0/30)
	gyro = gyroTable.getNumber("Y-Axis Angle") # reading at image (before latency)
	res, image = capture.read()
	p.process(image)
	contours = p.filter_contours_output
	table.putBoolean("seeTwo", len(contours) == 2)
	if len(contours) == 2:
		x1,y1,w1,h1 = cv2.boundingRect(contours[0])
		x2,y2,w2,h2 = cv2.boundingRect(contours[1])
		x = statistics.mean([x1,x2])
		y = statistics.mean([y1,y2])
		w = statistics.mean([w1,w2])
		h = statistics.mean([h1,h2])
		center = x + w/2
# 		angle = (center - 640)*26/640
		angle = math.degrees(math.atan((center - 320) / focalLength))
		table.putNumber("x", x)
		table.putNumber("y", y)
		table.putNumber("w", w)
		table.putNumber("h", h)
		table.putNumber("angle", gyro + angle)
	#print("Number of contours: {}".format(len(contours)))
# 	f.write('STEP: ' + str(p.find_contours_output) + '\n')
	now = time.time()*1000
# 	print(now-last_time)
	last_time = now
	
# print(f.read())
