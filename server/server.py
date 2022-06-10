from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
import os
from os import unlink
import time
import json
import ask_siri
import requests
import base64

load_dotenv()

hostName = os.getenv('HOST')
serverPort = int(os.getenv('PORT'))

class MyServer(BaseHTTPRequestHandler):
	lambdaUrl = ''
	# isRunning = False
	deviceId = os.getenv('DEVICE_NAME')
	# excelIds = []

	def do_POST(self):
		self.send_response(200)

		content_len = int(self.headers.get('Content-Length'))
		post_body = self.rfile.read(content_len)
		try:
			jsonStr = post_body.decode("utf-8")
			data = json.loads(jsonStr)

			if self.path == "/start":
				self.send_header("Content-type", "text/html")
				self.end_headers()
				self.wfile.write(bytes("Not supported for now", "utf-8"))
				# self.processQueue(data['url'], data['excelId'])
				return
			elif self.path  == "/process":
				self.send_header("Content-type", "application/json")
				self.end_headers()
				excelId = data['excelId']
				key = data['key']
				query = data['query']

				result = self.processQuery(excelId, key, query)
				self.wfile.write(bytes(json.dumps(result), "utf-8"))
				return
			else:
				self.send_header("Content-type", "text/html")
				self.end_headers()
				
		except Exception as e:
			print(e)
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

	# def processQueue(self, url, excelId):
	# 	print("START %s - %s" % (url, excelId))

	# 	if excelId in self.excelIds:
	# 		print("Already exist excel ID")
	# 	else:
	# 		self.excelIds.append(excelId)

	# 	if self.isRunning:
	# 		return
	# 	if url == None:
	# 		return
	# 	self.lambdaUrl = url
	# 	self.isRunning = True
	# 	self.requestNewTask()

	# def requestNewTask(self):
	# 	if self.excelIds.__len__() == 0:
	# 		self.isRunning = False
	# 		return

	# 	excelId = self.excelIds[0]
	# 	url = "%s/getSiriTask?excelId=%s&deviceId=%s" % (self.lambdaUrl, excelId, self.deviceId)
	# 	r = requests.get(url = url)
	# 	task = r.json()
	# 	print("New Task - %s" % excelId)
	# 	print(task)
	# 	if (task['success'] == False):
	# 		print("Task %s is done" % excelId)
	# 		self.excelIds.pop(0)
	# 		self.requestNewTask()
	# 		return

	# 	# task: {excelId, key, query}
	# 	excelId = task['excelId']
	# 	key = task['key']
	# 	query = task['query']
	# 	uniqueId = "%s-%s" % (excelId, key)
	# 	siriResponse, siriImageFilename = ask_siri.ask_siri(query, uniqueId)
	# 	requestData = {
	# 		'excelId': excelId,
	# 		'key': key,
	# 		'text': siriResponse,
	# 	}
	# 	url = "%s/uploadSiriResult" % self.lambdaUrl

	# 	files = {}
	# 	if (siriImageFilename != None):
	# 		files = {
	# 			'imageFile': open(siriImageFilename, 'rb')
	# 		}
	# 	requests.post(url = url, data = requestData, files = files)
	# 	if (siriImageFilename != None):
	# 		unlink(siriImageFilename)

	# 	self.requestNewTask()

	def processQuery(self, excelId, key, query):
		uniqueId = "%s-%s" % (excelId, key)
		siriResponse, siriImageFilename = ask_siri.ask_siri(query, uniqueId)
		# siriResponse = "This is siri result"
		# siriImageFilename = "images/result.jpg"
		siriImageBase64 = ""

		if (siriImageFilename != None):
			imageFile = open(siriImageFilename, "rb")
			siriImageBase64 = base64.b64encode(imageFile.read()).decode("utf-8")
			imageFile.close()
			unlink(siriImageFilename)
		
		return {
			"text": siriResponse,
			"image": siriImageBase64
		}

def start_server():
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))
	return webServer