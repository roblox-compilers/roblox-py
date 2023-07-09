
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local dict = builtin.dict
local str = builtin.str
local operator_in = builtin.operator_in
local int = builtin.int

-----------------------------------------------------------------------------
local table = dict {[stringmeta "a"] = stringmeta "b", [stringmeta "c"] = stringmeta "d"}
if (operator_in(stringmeta "a", table)) then
    print(stringmeta "a is present in table")
end