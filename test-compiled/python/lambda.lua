--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = _G.pyc.py

local int = builtin.int

-----------------------------------------------------------------------------
local x = function(a) return (bit32.bxor((bit32.bxor((a + 10), 2)), a)) end
print(x(5))