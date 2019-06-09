#! /usr/bin/python3

"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost:38253?foo=bar

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse


class VoteSvr(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path.startswith('/?'):
            path = parse.urlparse(self.path[2:]).path
            path = parse.unquote_plus(path)
            entries = {}
            extras = []
            for entry in path.split('&'):
                a = entry.split('=')
                if a[0] == 'extras[]':
                    extras.append(int(a[1]))
                    entries[a[0]] = extras
                else:
                    entries[a[0]] = a[1]
            tmp = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        {}<br>
        <a href="{}"title={}>{}</a><br>
    </body>
</html>'''
            message = tmp.format(str(entries), 'example_中文.html', 'example.html', 'example')
            self.wfile.write(bytes(message, 'utf8'))
        elif self.path.endswith('.html'):
            path = parse.unquote(self.path)
            try:
                f = open(os.getcwd() + path)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: ' + path)
                return
            self.wfile.write(bytes(f.read(), 'utf8'))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        message = '<html><body><h1>POST!</h1></body></html>'
        self.wfile.write(bytes(message, 'utf8'))

    @staticmethod
    def run(port=38253):
        server_address = ('', port)
        httpd = HTTPServer(server_address, VoteSvr)
        print('Httpd starting at {}:{:d} ...'.format('localhost', port))
        httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        VoteSvr.run(int(sys.argv[1]))
    else:
        VoteSvr.run()
