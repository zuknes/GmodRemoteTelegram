"""Webrequest routines"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
import time


class Serv(BaseHTTPRequestHandler):
    """Class Serv"""

    def do_GET(self):
        """Handle Get Requests"""

        client = self.client_address[0]
        if client not in self.server.srvhandler.servers:
            response = "you fool"
            self._send_response(response)
            print("WARNING! Refused connection from " + client)
            return
        if self.path == "/load":
            response = self.server.srvhandler.get_header()
            self._send_response(response)
            return

        self.server.srvhandler.set_server_time(client, time.time())

        queue = self.server.srvhandler.servers[client]
        queue_author = self.server.srvhandler.queue_author[client]
        if len(queue) > 0 and len(queue_author) > 0:

            data = queue[0]
            cmd, arg = data

            queue_author = self.server.srvhandler.queue_author[client][0]

            if cmd == "/rcon":
                arg = "game.ConsoleCommand[[" + arg + "\n]]"
            sent_header = self.server.srvhandler.get_sent_header()
            arg = sent_header.replace("{USERID}", str(queue_author)) + arg
            arg = arg + "\nprint('Message recieved')\n"

            print(str(client) + " << " + cmd + " " + arg)

            response = arg
            print(self.server.srvhandler.queue_author[client])
            try:
                self.server.srvhandler.queue_author[client].pop(0)
                self.server.srvhandler.servers[client].pop(0)
            except Exception as e:
                print(str(e))
        else:
            response = "local x = nil"
        self._send_response(response)

    def do_POST(self):
        """Handle POST Requests"""
        client = self.client_address[0]
        if client not in self.server.srvhandler.servers:
            print("WARNING! Refused POST connection from " + client)
        else:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = parse_qs(post_data.decode())
            try:
                if params['message'][0]:
                    try:
                        if params['uid'][0]:
                            self.server.tg.send(
                                params['uid'][0],
                                str(client) + " >> " + params['message'][0])
                    except Exception:
                        print("No client ID, reciveing to main\n")
                    print(str(client) + " >> " + params['message'][0])
                else:
                    print("Invalid postdata from " + str(client))
            except Exception:
                print("[exception] Invalid postdata from " + str(client))
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass
    """Suspend connetion logs"""

    def _send_response(self, response):
        """Send response"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def __init__(self, server_address, handler, handler_class=Serv):
        super().__init__(server_address, handler_class)
        self.srvhandler = handler

    def init_tg(self, handler):
        self.tg = handler
