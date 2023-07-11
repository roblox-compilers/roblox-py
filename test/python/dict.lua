
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local dict = builtin.dict
local stringmeta = builtin.stringmeta
local str = builtin.str
local int = builtin.int

-----------------------------------------------------------------------------
local newdict = dict {}
newdict[stringmeta "one"] = 1
newdict[stringmeta "two"] = 2
newdict[stringmeta "three"] = 3
newdict[stringmeta "four"] = 4
for key in newdict do
    print(key, newdict[key])
end