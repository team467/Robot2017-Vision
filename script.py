from grip import GripPipeline
p = GripPipeline()

import cv2
cam = cv2.VideoCapture(0)

import time

# f = open('dataFile', 'r+')

last_time = time.time()*1000
for i in range(1000):
	time.sleep(1.0/30)
	res, image = cam.read()
	p.process(image)
	contours = p.filter_contours_output
	for contour in contours:
# 		print(contour)
		x,y,w,h = cv2.boundingRect(contour)
		print(x + w/2)
	print("Number of contours: {0}".format(len(contours)))
# 	f.write('STEP: ' + str(p.find_contours_output) + '\n')
	now = time.time()*1000
# 	print(now-last_time)
	last_time = now
	
# print(f.read())