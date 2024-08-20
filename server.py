import http.server
import urllib.parse
import mimetypes
import logging
import threading
import socket
import json
import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
JIN = Environment(loader=FileSystemLoader(''))

class Operator(BaseHTTPRequestHandler):
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
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        parsed_data = urllib.parse.unquote_plus(data.decode())

        try:
            data_dict = {key: value for key, value in [el.split('=') for el in parsed_data.split('&')]}
            print(data_dict)

            # Відправка даних на Socket сервер
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(json.dumps(data_dict).encode(), ("localhost", 5000))
            sock.close()
        except ValueError as err:
            logging.error(err)
        except OSError as err:
            logging.error(err)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-type', mime_type)
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

def run_http_server():
    address = ('localhost', 3000)
    http_server = HTTPServer(address, Operator)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.shutdown()

def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 5000))

    if not BASE_DIR.joinpath('storage').exists():
        BASE_DIR.joinpath('storage').mkdir()

    while True:
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode())

        timestamp = datetime.datetime.now().isoformat()
        data_to_store = {timestamp: message}

        if BASE_DIR.joinpath('storage/data.json').exists():
            with open(BASE_DIR.joinpath('storage/data.json'), 'r', encoding="utf-8") as f:
                existing_data = json.load(f)
            existing_data.update(data_to_store)
        else:
            existing_data = data_to_store

        with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    threading.Thread(target=run_http_server).start()
    threading.Thread(target=run_socket_server).start()
