--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local safeadd = builtin.safeadd
local bit32 = builtin.bit32
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local x = function(a) return (bit32.bxor((bit32.bxor((safeadd(a, 10)), 2)), a)) end
print(x(5))

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

