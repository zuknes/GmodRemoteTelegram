"""Telegram communication"""
import telebot
from telebot import types
import time
import os
from server_handler import ServerHandler
from server_cmd import ServerCommandHandler
import constants

class TelegramInputHandler():
    """Class TelegramInputHandler"""
    def __init__(self, serverhandler, servercmdhandler):
        """Constructor"""
        self.srvhandler = ServerHandler()
        self.srvhandler = serverhandler

        self.cmdhandler = ServerCommandHandler(serverhandler)
        self.cmdhandler = servercmdhandler

        self.bot = telebot.TeleBot(constants.TOKEN)

        @self.bot.message_handler(content_types=["text"])
        def _hook_messages(message):
            """Handle incoming messages"""
            if not self._check_auth(message.from_user.id):
                return
            self._handle_telegram_input(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            """Handle callback buttons"""
            if not self._check_auth(call.message.chat.id):
                return
            if call.message:
                if "/s/" in call.data:
                    _, key = call.data.split("/s/")
                    self.srvhandler.set_current_server(
                        key,
                        call.message.chat.id
                        )
                    self.bot.answer_callback_query(
                        callback_query_id=call.id,
                        show_alert=False,
                        text="Successfuly chosen"
                        )
                elif "/d/" in call.data:
                    _, key = call.data.split("/d/")
                    try:
                        self.srvhandler.remove_server(key)
                        self.bot.delete_message(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id
                            )
                        self.bot.answer_callback_query(
                            callback_query_id=call.id,
                            show_alert=False,
                            text="Successfully removed"
                            )
                    except Exception:
                        print("Invalid server removal!\n")

        @self.bot.message_handler(
            func=lambda message:
            message.document.mime_type == 'text/x-lua',
            content_types=['document'])
        def handle_text_doc(message):
            """Handle LUA File upload"""
            if not self._check_auth(message.from_user.id):
                return
            if self.srvhandler.get_current_server(message.from_user.id) == "nil":
                self.send(
                 message.chat.id, "No server selected. ",
                 "Select a server by using select [ip]",
                 self._keyboard()
                )
                return
            file_id = message.document.file_id
            file_info = self.bot.get_file(file_id)
            content = self.bot.download_file(file_info.file_path)
            self.cmdhandler.commands["/luarun"](
                "/luarun",
                "/luarun " + content.decode('UTF-8'),
                message.from_user.id)

    def start(self):
        self.bot.infinity_polling()

    def _keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.row('🌐 List', '❓ Help')
        return keyboard

    def _handle_telegram_input(self, message):
        """Main Input func. Todo: split"""

        if message.text == "❓ Help":
            self._msg_help(message)
            return

        if message.text == "🌐 List":
            self._msg_list(message)
            return

        if " " in message.text:
            cmd = message.text.split(" ", 1)
            command, arg = cmd
        else:
            self.send(
                message.from_user.id,
                "Wrong command syntax: " + message.text + ", read help"
                )
            return

        if command == "/addserver":
            self._add_server(message, arg)
            return

        if command == "/select":
            self._select_server(message, arg)
            return

        self._execute_command(message, command)
        return

    def _check_auth(self, id):
        if id not in constants.GODS:
            self.send(id, "I reject my humanity")
            return False
        else:
            return True

    def _msg_help(self, message):
        help_text = "You can get your serverlist by pressing List button.\n \
            /select [ip] - select server to operate\n \
            /addserver [ip] - add new server to operate\n \
            /luarun [code] - execute lua code on the server\n \
            /rcon [commands] - execute rcon commands on the server\n \
            /sendfile [filename] - send file from /includes dir to server"
        self.send(
                message.chat.id,
                help_text,
                self._keyboard())

    def _msg_list(self, message):
        for k in self.srvhandler.servers.keys():
            online = self.srvhandler.server_time[k]['curtime'] + \
                10 >= time.time()

            keyboard = types.InlineKeyboardMarkup()
            select_button = types.InlineKeyboardButton(
                text="Select server",
                callback_data="/s/"+str(k))
            keyboard.add(select_button)
            remove_button = types.InlineKeyboardButton(
                text="Remove server",
                callback_data="/d/"+str(k))
            keyboard.add(remove_button)

            online = "✅" if online else "❌"
            self.send(
                message.chat.id,
                k + " | Online: " + str(online),
                keyboard)

    def _add_server(self, message, arg):
        with open('server.list', 'a') as file:
            if os.stat("server.list").st_size == 0:
                file.write(arg)
            else:
                file.write('\n' + arg)
        self.srvhandler.servers[arg] = []
        self.srvhandler.queue_author[arg] = []
        self.srvhandler.set_server_time(arg, 0)
        self.send(
            message.chat.id,
            'Successful added ' + arg + ' to the list',
            self._keyboard()
            )

    def _select_server(self, message, arg):
        if arg not in self.srvhandler.servers:
            self.send(
                message.chat.id,
                "No such server found",
                self._keyboard()
                )
            return
        self.srvhandler.set_current_server(arg, message.from_user.id)
        self.send(
            message.chat.id, "Successfully selected server: " +
            self.srvhandler.get_current_server(message.from_user.id))

    def _execute_command(self, message, command):
        try:
            if self.cmdhandler.commands[command]:
                if self.srvhandler.get_current_server(message.from_user.id) == "nil":
                    self.send(
                        message.chat.id, "No server selected.",
                        self._keyboard()
                        )
                    return
                self.cmdhandler.commands[command](
                    command,
                    message.text,
                    message.from_user.id)
                return
        except KeyError:
            self.send(message.chat.id, "No such command: " + command)
            return
        except Exception:
            return

    def send(self, to, msg, reply_markup=None):
        self.bot.send_message(to, msg, reply_markup=reply_markup)
