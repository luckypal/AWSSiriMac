from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import os
from os import unlink
import time
import json
# import ask_siri
import requests

load_dotenv()

hostName = os.getenv('HOST')
serverPort = int(os.getenv('PORT'))

class MyServer(BaseHTTPRequestHandler):
	lambdaUrl = ''
	isRunning = False
	deviceId = os.getenv('DEVICE_NAME')

	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

		content_len = int(self.headers.get('Content-Length'))
		post_body = self.rfile.read(content_len)
		jsonStr = post_body.decode("utf-8")
		data = json.loads(jsonStr)

		if self.path == "/start":
			self.processQueue(self, data.url)
			return

	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>%s</title></head>" % self.deviceId, "utf-8"))
		
		self.wfile.write(bytes("<body>", "utf-8"))
		runningStr = 'Running'
		if self.isRunning == False:
			runningStr = 'Rest'

		self.wfile.write(bytes("<h1>Device: %s</h2>" % self.deviceId, "utf-8"))
		self.wfile.write(bytes("<h2>Status: %s</h2>" % runningStr, "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))

	def processQueue(self, url):
		if self.isRunning:
			return
		if url == None:
			return
		self.lambdaUrl = url
		self.isRunning = True
		self.requestNewTask(self)

	def requestNewTask(self):
		url = "%s/getSiriTask/%s" % self.lambdaUrl % self.deviceId
		r = requests.get(url = url)
		task = r.json()
		if (task.success == False):
			self.isRunning = False
			return

		# task: {excelId, key, query}
		uniqueId = "%s-%s" % task.excelId % task.key
		# siriResponse, siriImageFilename = ask_siri.ask_siri(task.query, uniqueId)
		# requestData = {
		# 	'excelId': task.excelId,
		# 	'key': task.key,
		# 	'text': siriResponse,
		# }
		# url = "%s/uploadSiriResult" % self.lambdaUrl

		# files = {}
		# if (siriImageFilename != None):
		# 	files = {
		# 		'imageFile': open(siriImageFilename, 'rb')
		# 	}
		# requests.post(url = url, data = requestData, files = files)
		# if (siriImageFilename != None):
		# 	unlink(siriImageFilename)

		# self.requestNewTask(self)

def start_server():
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))
	return webServer