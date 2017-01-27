from grip import GripPipeline
p = GripPipeline()

import cv2
import os
import math

FOVTangent = math.tan(math.radians(26))
focalLength = 320/FOVTangent

def initCamera():
	os.system("v4l2-ctl -c exposure_auto=1 -c exposure_absolute=5")
	global capture
	capture = cv2.VideoCapture(0)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

capture = None
initCamera()
res, image = capture.read()
res, image = capture.read()
res, image = capture.read()
res, image = capture.read()
p.process(image)
cv2.imwrite('image-raw.jpg', image)
cv2.drawContours(image, p.filter_contours_output, -1, (0,255,0), 3)
for contour in p.filter_contours_output:
	x,y,w,h = cv2.boundingRect(contour)
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
	center = x + w/2
	angle = math.degrees(math.atan((center - 320) / focalLength))
	print(angle)
print(p.filter_contours_output)
cv2.imwrite('image-contours.jpg', image)