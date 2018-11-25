import sys
import json
import logging
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import http.server
from dataclasses import asdict

import base
import lib.http

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)



class ActualHandler:
    def get(self, req):
        return {'req': asdict(req), 'weather': 'nice', 'cows': 4, 'version': sys.version}


class handler(lib.http.GenericHandler):
    actual = ActualHandler()


def runner():
    httpd = http.server.HTTPServer(('', 7004), handler)
    httpd.serve_forever()

if __name__ == '__main__':
    runner()
