"""Server command routines"""
from server_handler import ServerHandler


class ServerCommandHandler():
    """ServerCommandHandler"""

    def __init__(self, serverhandler):
        """Constructor"""
        self.srvhandler = ServerHandler()
        self.srvhandler = serverhandler

        self.commands = {
            '/luarun': self.command_luarun,
            '/rcon': self.command_rcon,
            '/sendfile': self.command_sendfile,
        }

    def init_tg(self, handler):
        self.tg = handler

    def queue_command(self, serverip, arg_type, arg_command, message_from):
        """Queue Server Command"""
        self.srvhandler.servers[serverip].append([arg_type, arg_command])
        self.srvhandler.set_queue_author(serverip, message_from)

    def command_luarun(self, arg_command, arg_input, message_from):
        """Luarun"""
        tosend = arg_input[len(arg_command) + 1:]
        self.queue_command(self.srvhandler.get_current_server(message_from),
                           arg_command, tosend, message_from)
        print("luarun " + tosend + ">>" + self.srvhandler.get_current_server(message_from))

    def command_rcon(self, arg_command, arg_input, message_from):
        """Rcon"""
        tosend = arg_input[len(arg_command) + 1:]
        self.queue_command(self.srvhandler.get_current_server(message_from),
                           arg_command, tosend, message_from)
        print("rcon " + tosend + ">>" + self.srvhandler.get_current_server(message_from))

    def command_sendfile(self, arg_command, arg_input, message_from):
        """SendFile"""
        tosend = arg_input[len(arg_command) + 1:]
        try:
            file_container = open('./includes/' + tosend + '.lua', 'r').read()
        except Exception:
            self.tg.send(
                message_from,
                "Error opening file: " + tosend + '.lua')
            print("Error opening file: " + tosend + '.lua')
            return
        self.queue_command(self.srvhandler.get_current_server(message_from),
                           'luarun', file_container, message_from)
        print("luarun " + tosend + ">>" + self.srvhandler.get_current_server(message_from))
