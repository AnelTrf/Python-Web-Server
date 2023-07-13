import http.server
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'mywebpage.html'
            try:
                file = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))
        elif self.path == '/contra.html':
            try:
                file = open('templates/contra.html').read()
                self.send_response(200)
            except:
                file = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run():
    address = ('', 8000)
    httpd = HTTPServer(address, MyHttpRequestHandler)
    print('Server running on localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
