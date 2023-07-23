--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = _G.pyc.py

local asynchronousfunction = builtin.asynchronousfunction
local stringmeta = builtin.stringmeta
local str = builtin.str
local open = builtin.open
local int = builtin.int

-----------------------------------------------------------------------------
local async_with = asynchronousfunction(function()
    do
        local f = open(stringmeta "test.txt")
        local contents = coroutine.yield(f.read())
        print(contents)
    end
end)