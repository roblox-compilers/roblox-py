--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local str = builtin.str
local format = builtin.format
local formatmod = builtin.formatmod
local int = builtin.int

-----------------------------------------------------------------------------
local text = (formatmod(stringmeta "%s is my name", stringmeta "John"))
print(text)