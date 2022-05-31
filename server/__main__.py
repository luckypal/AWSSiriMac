import sys, server

def main():
	args = sys.argv

	webServer = server.start_server()

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")

if __name__ == '__main__':
	main()
