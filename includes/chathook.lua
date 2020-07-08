local tosend = ""

local dname, sname = '%s', '%s(%s)'


hook.Add( 'PlayerSay', 'memes', function( v, say )
	tosend = tosend .. '['.. v:UserID() .. ']' .. (v:SteamName() and sname:format( v:GetName(), v:SteamName() ) or dname:format( v:GetName() ) ) ..': ' .. say .. '\n'
	timer.Create( "sendchat", 1, 1, function() print(tosend) tosend = "" end )
end)