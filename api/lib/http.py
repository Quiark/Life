import sys
import json
import logging
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass


@dataclass
class Request:
    path: str
    query: dict


class GenericHandler(BaseHTTPRequestHandler):
    actual = None

    def __init__(self, request, client_address, server):
        # must be last for some reason
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_any(self):
        try:
            logging.info('path=' + self.path)
            logging.info('requestline=' + self.requestline)

            url = urlparse(self.path)
            logging.info('url={}'.format(url))

            qs = None
            if url.query != '':
                qs = parse_qs(url.query, strict_parsing=True)
                logging.info('qs={}'.format(qs))
                qs = {k: v[0] for k, v in qs}

            # -- run --

            request = Request(url.path, qs)
            res = self.actual.get(request)

            # -- respond --
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
        except RuntimeError as ex:
            logging.exception('when handling request')

    def do_GET(self):
        return self.do_any('GET')

    def do_POST(self):
        return self.do_any('POST')

    def do_PUT(self):
        return self.do_any('PUT')

    def do_DELETE(self):
        return self.do_any('DELETE')
