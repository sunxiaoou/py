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
import sys

from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse

from vote import Keys
from dbClient import DBClient


class VoteSvr(BaseHTTPRequestHandler):
    client = None

    @staticmethod
    def get_counter():
        counter = {}
        for r in VoteSvr.client.find({}, {Keys._id: False, Keys.options: True}):
            if r:
                # print(r[Keys.options])
                for i in r[Keys.options]:
                    if i not in counter.keys():
                        counter[i] = 1
                    else:
                        counter[i] += 1

        lst = []
        for i in range(int(max(counter, key=int))):
            if i + 1 in counter.keys():
                lst.append(counter[i + 1])
            else:
                lst.append(0)
        return lst

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path.startswith('/?'):
            path = parse.urlparse(self.path[2:]).path
            path = parse.unquote_plus(path)
            options = []
            name = ''
            comments = ''
            for entry in path.split('&'):
                a = entry.split('=')
                if a[0] == Keys.name:
                    name = a[1]
                elif a[0] == 'extras[]':
                    options.append(int(a[1]))
                elif a[0] == 'comments':
                    comments = a[1]

            print('name: {}, options: {}, comments: {}'.format(name, options, comments))
            if VoteSvr.client.update_one({Keys.name: name}, {Keys.options: options, Keys.comments: comments,
                                                             Keys.timestamp: datetime.now()}) is None:
                self.send_error(403, 'Name Not Valid: ' + name)
                return

            buf = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Vote result:</h1>
        <p>
            Red (votes: )<br>
            Orange (votes: )<br>
            Yellow (votes: )<br>
            Green (votes: )<br>
            Blue (votes: )
        </p>
    </body>
</html>'''
            for i in VoteSvr.get_counter():
                buf = buf.replace('(votes: )', '(votes: ' + str(i) + ')', 1)
            self.wfile.write(bytes(buf, 'utf8'))

        elif self.path == '/' or self.path.endswith('.html'):
            html = parse.unquote(self.path)[1:]
            if not html:
                html = 'vote.html'
            try:
                f = open(html)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: ' + html)
                return
            buf = f.read()
            f.close()
            for i in VoteSvr.get_counter():
                buf = buf.replace('(votes: )', '(votes: ' + str(i) + ')', 1)
            self.wfile.write(bytes(buf, 'utf8'))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
        message = '<html><body><h1>Not support POST yet</h1></body></html>'
        self.wfile.write(bytes(message, 'utf8'))

    @staticmethod
    def run(port=38253):
        VoteSvr.client = DBClient('votes', 'example')
        server_address = ('', port)
        httpd = HTTPServer(server_address, VoteSvr)
        print('Httpd starting at {}:{:d} ...'.format('localhost', port))
        httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        VoteSvr.run(int(sys.argv[1]))
    else:
        VoteSvr.run()
