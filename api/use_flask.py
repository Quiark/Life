import http.server
from http.server import BaseHTTPRequestHandler
from wsgiref.simple_server import WSGIRequestHandler
from rest import app




class handler(WSGIRequestHandler):
    def __init__(self, request, client_address, server):
        server.get_app = lambda: app
        server.base_environ = self.setup_environ()
        WSGIRequestHandler.__init__(self, request, client_address, server)

    def setup_environ(self):
        # Set up base environment
        env = {}
        env['SERVER_NAME'] = 'FAKE WSGI server'
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = 1234
        env['REMOTE_HOST']=''
        env['CONTENT_LENGTH']=''
        env['SCRIPT_NAME'] = ''
        return env

def runner():
    httpd = http.server.HTTPServer(('', 7004), handler)
    httpd.serve_forever()

if __name__ == '__main__':
    runner()
