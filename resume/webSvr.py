#! /usr/bin/python3

"""
Very simple HTTP server in python.

Usage::
    python3 webSvr.py [<port>]

Send a GET request::
    curl http://localhost:7412?foo=bar

Send a HEAD request::
    curl -I http://localhost:7412

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost:7412

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import sys

from condition import Condition
from finder import Finder
from reporter import Reporter


class WebSvr(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        path = parse.urlparse(self.path[2:]).path
        path = parse.unquote_plus(path)
        entries = {}
        for entry in path.split('&'):
            a = entry.split('=')
            entries[a[0]] = a[1] if not a[1].isdecimal() else int(a[1])
        # message = '<html><body><h1>' + str(entries) + '</h1></body></html>'
        conditions = Condition.create_conditions(entries)
        documents = Finder.find(Finder.get_collection('localhost', 27017, 'shoulie', 'resumes'), conditions)
        message = Reporter.to_html(documents)
        self.wfile.write(bytes(message, 'utf8'))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
        message = '<html><body><h1>Not support POST yet</h1></body></html>'
        self.wfile.write(bytes(message, 'utf8'))

    @staticmethod
    def run(port=7412):
        server_address = ('', port)
        httpd = HTTPServer(server_address, WebSvr)
        print('Starting httpd at :{:d} ...'.format(port))
        httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        WebSvr.run(int(sys.argv[1]))
    else:
        WebSvr.run()
