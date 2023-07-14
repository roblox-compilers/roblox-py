--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local str = builtin.str
local int = builtin.int

-----------------------------------------------------------------------------
local string = stringmeta "Hello World"
print(string["SLICE!(0, 5)"])