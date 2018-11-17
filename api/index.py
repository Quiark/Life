import sys
import json
import logging
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import http.server

import base

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)


class x_handler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(str("version: {}".format(sys.version)).encode())
		return


class ActualHandler:
	def get(self):
		pass


class handler(BaseHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		self.a = ActualHandler()
		# must be last for some reason
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)


	def do_GET(self):
		try:
			res = self.a.get()
			logging.info('path=' + self.path)
			logging.info('requestline=' + self.requestline)

			url = urlparse(self.path)
			logging.info('url={}'.format(url))

			qs = parse_qs(url.query, strict_parsing=True)
			logging.info('qs={}'.format(qs))

			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps(res).encode())
		except RuntimeError as ex:
			logging.exception('when handling request')


def runner():
	httpd = http.server.HTTPServer(('', 7004), handler)
	httpd.serve_forever()

if __name__ == '__main__':
	runner()
