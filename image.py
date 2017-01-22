from grip import GripPipeline
p = GripPipeline()

import cv2
cam = cv2.VideoCapture(0)
res, image = cam.read()
res, image = cam.read()
res, image = cam.read()
res, image = cam.read()
p.process(image)
cv2.imwrite('image-raw.jpg', image)
cv2.drawContours(image, p.filter_contours_output, -1, (0,255,0), 3)
for contour in p.filter_contours_output:
	x,y,w,h = cv2.boundingRect(contour)
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
	center = x + w/2
	angle = (center - 320)*26/320
	print(angle)
print(p.filter_contours_output)
cv2.imwrite('image-contours.jpg', image)