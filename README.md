
# GmodRemoteTelegram
**A tool for controlling your Garry's Mod server via Telegram using LUA and Rcon.**

**Requirements:**
  *Python 3.4+
  Pip3*
 
 **How to install:**
  pip3 install -r requirements.txt
 
 ***You should edit constants.py before launching!***
 Example:
 

    TOKEN = "paste_telegram_bot_token_here" #telegram bot token here
    GODS = [] #your telegram id here ex [123456789, 987654321] - 2 admin accounts.
    PUBLIC_IP = "00.00.00.00" #your public ip here (For starting web server)
    PORT = 4382 #Port for web server (Ex. your server will be avalible at http://your_ip:port)

**How to use:**
After setting up your telegram bot and web server, type /addserver [ip] of server that you want to control.
That will create new server list and add your server to it.
After that, you should RUN this code on your Garry's Mod server:
 

     http.Fetch('http://webserver_ip:port/load', RunString)

That will make your Garry's mod server connect to your telegram bot.

Telegram commands:

    You can get your serverlist by pressing List button.
                /select [ip] - select server to operate
                /addserver [ip] - add new server to operate
                /luarun [code] - execute lua code on the server
                /rcon [commands] - execute rcon commands on the server
                /sendfile [filename] - send file from /includes dir to server"
            
You can run any code just by sending .lua file to your telegram bot.

/includes folder contains a few LUA files, which you can execute by default.

**Example commands:**

      /sendfile servinfo - that will display all server info inside your telegram bot.
      /sendfile chathook - that will send all incoming chat messages in-game to your telegram bot,
      /sendfile stopchat - kills chathook
      

Feel free to commit, have fun!
