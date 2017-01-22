from grip import GripPipeline
p = GripPipeline()

from networktables import NetworkTables
NetworkTables.initialize(server='10.0.1.2')
table = NetworkTables.getTable('SmartDashboard')

import cv2
cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_EXPOSURE, 0.1);

import time

# f = open('dataFile', 'r+')

last_time = time.time()*1000
for i in range(1000):
	time.sleep(1.0/30)
	res, image = cam.read()
	p.process(image)
	contours = p.filter_contours_output
	if len(contours) = 1:
		x,y,w,h = cv2.boundingRect(contours[0])
		center = x + w/2
		angle = (center - 640)*26/640
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