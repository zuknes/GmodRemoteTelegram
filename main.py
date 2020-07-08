"""Main Module"""
import threading
from server_handler import ServerHandler
from server_cmd import ServerCommandHandler
from request_handler import ThreadedHTTPServer, Serv
from telegram_handler import TelegramInputHandler
import constants


def main():
    """Main Function"""
    servhandler = ServerHandler()
    servcmd = ServerCommandHandler(servhandler)
    inputhandler = TelegramInputHandler(servhandler, servcmd)

    if servhandler.get_header() == "nil" or servhandler.get_sent_header() == "nil":
        return
    servhandler.load_servers()
    httpd = ThreadedHTTPServer(('', constants.PORT), servhandler, Serv)

    servcmd.init_tg(inputhandler)
    servhandler.init_tg(inputhandler)
    httpd.init_tg(inputhandler)

    print("GmodRemote 1.0: Ready()")
    print("Listening on port " + str(constants.PORT))

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    inputhandler.start()


if __name__ == "__main__":
    main()
