#!/usr/bin/python
'''
	orig author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''

from grip import GripPipeline
p = GripPipeline()
import cv2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time

capture=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print self.path
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			red = 255
			last_time = time.time()*1000
			while True:
				time.sleep(1.0/30)
				try:
					rc,img = capture.read()
					if not rc:
						continue
					p.process(img)
					cv2.drawContours(img, p.filter_contours_output, -1, (0,255,red), 3)
					print(len(p.filter_contours_output))
					red = (red+50)%256
					r, buf = cv2.imencode(".jpg",img)
					self.wfile.write("--jpgboundary\r\n")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(len(buf)))
					self.end_headers()
					self.wfile.write(bytearray(buf))
					self.wfile.write('\r\n')
					now = time.time()*1000
# 					print(now-last_time)
					last_time = now
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html') or self.path=="/":
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://kili.local:9090/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return

def main():
	global capture
	capture = cv2.VideoCapture(0)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640); 
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
	try:
		server = HTTPServer(('',9090),CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()