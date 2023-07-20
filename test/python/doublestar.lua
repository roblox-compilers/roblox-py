--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local dict = builtin.dict
local str = builtin.str

-----------------------------------------------------------------------------
local x = dict {[stringmeta "a"] = stringmeta "b", [stringmeta "c"] = stringmeta "d"}
local a = stringmeta "Hello, World!"
a.b()