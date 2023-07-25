--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local sum = builtin.sum
local safeadd = builtin.safeadd
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local function sum_numbers(a, b)
    return (safeadd(a, b))
end
print(sum_numbers(10, 5))
print(sum_numbers(10.3, 5))
print(sum_numbers("Bob", "Mark"))

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

