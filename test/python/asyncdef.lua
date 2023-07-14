--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local asynchronousfunction = builtin.asynchronousfunction
local stringmeta = builtin.stringmeta
local str = builtin.str
local int = builtin.int

-----------------------------------------------------------------------------
local hello = asynchronousfunction(function()
    print(stringmeta "Hello, world!")
end)