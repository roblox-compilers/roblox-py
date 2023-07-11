
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local int = builtin.int

-----------------------------------------------------------------------------
local x = function(a) return (bit32.bxor((bit32.bxor((a + 10), 2)), a)) end
print(x(5))