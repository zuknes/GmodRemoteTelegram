local toprint = ''

local function append(str)
	toprint = toprint .. str .. '\n'
end

local function addstr(key, str)
	append( key .. ':\t' .. str )
end

addstr( 'Hostname', GetHostName() )
addstr( 'Online', #player.GetAll() )
addstr( 'Map', game.GetMap() )
append( string.rep( '=', 54 ) )

local dname, sname = '%s', '%s(%s)'

for k,v in pairs( player.GetAll() ) do
	addstr( '[' .. tostring(v:EntIndex()).. '] ' .. (v:SteamName() and sname:format( v:GetName(), v:SteamName() ) or dname:format( v:GetName() ) ), v:GetUserGroup() )
end

print(toprint)