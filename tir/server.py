import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

from tir.templates import TemplateLoader


class TirServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.tpl = TemplateLoader(layout_directory=os.path.join(os.getcwd(), 'layout', 'default'))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        response = ''
        if self.path == '/':
            posts = [file for file in os.scandir(os.path.join(os.getcwd(), 'content', 'posts'))]
            self.wfile.write(self.tpl.env.get_template('server/index.html').render(posts=posts).encode('utf8'))
        elif self.path == '/write':
            self.wfile.write(self.tpl.env.get_template('server/index.html').render().encode('utf8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=TirServer, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    webbrowser.open(f'{addr}:{port}')

    print(f"Starting httpd server on {addr}:{port}")

    httpd.serve_forever()
