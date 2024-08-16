import http.server
import urllib.parse
from http.server import HTTPServer,BaseHTTPRequestHandler

class Operator(BaseHTTPRequestHandler):
    
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html('index.html')

    def do_POST(self):
        pass

    def send_html(self,filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb',) as file:
            self.wfile.write(file.read())

def run_server():
    adress = ('localhost', 8080)
    http.server = HTTPServer(adress, Operator)
    try:
        http.server.serve_forever()
    except KeyboardInterrupt:
        http.server.shutdown()



if __name__ == '__main__':
    run_server()