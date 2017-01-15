from grip import GripPipeline
p = GripPipeline()

import cv2
cam = cv2.VideoCapture(0)
res, image = cam.read()
p.process(image)
cv2.imwrite('image-raw.jpg', image)
cv2.drawContours(image, p.filter_contours_output, -1, (0,255,0), 3)
print(p.filter_contours_output)
cv2.imwrite('image-contours.jpg', image)