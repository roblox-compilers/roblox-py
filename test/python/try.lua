
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local all = builtin.all
local stringmeta = builtin.stringmeta
local str = builtin.str

-----------------------------------------------------------------------------
local success, result = pcall(function()
    error(stringmeta "Some error")
end)