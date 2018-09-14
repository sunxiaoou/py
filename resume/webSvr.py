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
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import os
import pprint
import sys

from condition import Condition
from finder import Finder
from reporter import Reporter
from saver import Saver


class WebSvr(BaseHTTPRequestHandler):
    base_folder = ''

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
            for entry in path.split('&'):
                a = entry.split('=')
                entries[a[0]] = a[1] if not a[1].isdecimal() else int(a[1])
            conditions = Condition.create_conditions(entries)
            log = open('{}.txt'.format(datetime.now().strftime('%y%m%d_%H%M%S')), 'w')
            log.write(pprint.pformat(conditions) + '\n')
            log.close()

            documents = Finder.find(Finder.get_collection('localhost', 27017, 'shoulie', 'resumes'), conditions)
            message = Reporter.to_html(documents)
            html = open('{}.html'.format(datetime.now().strftime('%y%m%d_%H%M%S')), 'w')
            html.write(message)
            html.close()

            self.wfile.write(bytes(message, 'utf8'))
        elif self.path == '/' or self.path.endswith('.html'):
            path = parse.unquote(self.path.lstrip('/'))
            if not path:
                path = 'form.html'
            else:
                path = os.path.join(WebSvr.base_folder, path.split('_')[0], path)
            try:
                f = open(path)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: ' + path)
                return
            self.wfile.write(bytes(f.read(), 'utf8'))
        elif self.path.endswith('.docx'):
            path = parse.unquote(self.path.lstrip('/'))
            html = os.path.splitext(path)[0] + '.html'
            conditions = Condition.create_conditions({'file': html})
            documents = Finder.find(Finder.get_collection('localhost', 27017, 'shoulie', 'resumes'), conditions)
            """
            txt = open(path, 'w')
            txt.write(pprint.pformat(documents[0]) + '\n')
            # txt.write(str(documents[0]))
            txt.close()
            """
            Saver.to_doc(documents[0])
            message = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <style type="text/css">td, th {{ border: 1px solid black; }}</style>
    </head>
    <body>
        File "{}" generated
    </body>
</html>
'''
            self.wfile.write(bytes(message.format(path), "utf8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        message = '<html><body><h1>Not support POST yet</h1></body></html>'
        self.wfile.write(bytes(message, 'utf8'))

    @staticmethod
    def run(port=7412, folder='/home/xixisun/suzy/shoulie/resumes'):
        WebSvr.base_folder = folder
        print('Resumes are in {}'.format(folder))
        server_address = ('', port)
        httpd = HTTPServer(server_address, WebSvr)
        print('Httpd starting at {}:{:d} ...'.format('localhost', port))
        httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        WebSvr.run(int(sys.argv[1]), sys.argv[2])
    else:
        WebSvr.run()
