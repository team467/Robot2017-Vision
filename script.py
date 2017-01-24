from grip import GripPipeline
p = GripPipeline()

from networktables import NetworkTables
NetworkTables.initialize(server='10.0.1.16')
table = NetworkTables.getTable('SmartDashboard')

import cv2
import time
import math
import os

FOVTangent = math.tan(math.radians(26))
focalLength = 360/FOVTangent

def initCamera():
	os.system("v4l2-ctl -c exposure_auto=1 -c exposure_absolute=5")
	global capture
	capture = cv2.VideoCapture(0)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

# f = open('dataFile', 'r+')
capture = None
initCamera()
last_time = time.time()*1000
for i in range(1000):
	time.sleep(1.0/30)
	res, image = capture.read()
	p.process(image)
	contours = p.filter_contours_output
	if len(contours) == 1:
		x,y,w,h = cv2.boundingRect(contours[0])
		center = x + w/2
# 		angle = (center - 640)*26/640
		angle = math.degrees(math.atan((center - 320) / focalLength))
		table.putNumber("x", x)
		table.putNumber("y", y)
		table.putNumber("w", w)
		table.putNumber("h", h)
		table.putNumber("angle", angle)
	print("Number of contours: {}".format(len(contours)))
# 	f.write('STEP: ' + str(p.find_contours_output) + '\n')
	now = time.time()*1000
# 	print(now-last_time)
	last_time = now
	
# print(f.read())