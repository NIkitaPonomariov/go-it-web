import http.server
import urllib.parse
import mimetypes
from pathlib import Path
from http.server import HTTPServer,BaseHTTPRequestHandler

BASE_DIR = Path() #це маршрут


class Operator(BaseHTTPRequestHandler):
    #функція для обробки гет запросів для відправки статичних файлів
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

    def do_POST(self):
        pass

    #функція відправки статичних файлів
    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-type', mime_type)
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb',) as file:
            self.wfile.write(file.read())

    #функція відправки html
    def send_html(self,filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb',) as file:
            self.wfile.write(file.read())


#функція запуску серверу
def run_server():
    adress = ('localhost', 3000)
    http.server = HTTPServer(adress, Operator)
    try:
        http.server.serve_forever()
    except KeyboardInterrupt:
        http.server.shutdown()



if __name__ == '__main__':
    run_server()