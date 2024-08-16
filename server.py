import http.server
import urllib.parse
import mimetypes
import logging
from pathlib import Path
import json
from http.server import HTTPServer,BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path() #це маршрут
JIN = Environment(loader=FileSystemLoader(''))


class Operator(BaseHTTPRequestHandler):
    #функція для обробки гет запросів 
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
        urllib.parse.data = urllib.parse.unquote_plus(data.decode())

        try:
            parse_deict = {key: value for key,value in [el.split('=')for el in urllib.parse.data.split('&')]}
            print(parse_deict)
            with open('data.json', 'w') as file:
                json.dump(parse_deict, file, ensure_ascii=False,indent=4)
        except ValueError as err:
            logging.error(err)
        except OSError as err:
            logging.error(err)

        self.send_response(302) 
        self.send_header('Location', '/')
        self.end_headers()

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


    """
    це код з відео він не потрібен в цьому дз
    але я хочу щоб він був тут!!!!!!!!!!!!!!!

    def render_templates(self,filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open('storage/data.json', 'r', encoding="utf8") as file:
            data = json.load(file)

        template = JIN.get_template(filename)
        html = template.render(blog=data)
        self.wfile.write(html.encode())
    """

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