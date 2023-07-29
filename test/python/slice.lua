--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local str = builtin.str
local string = builtin.string
local int = builtin.int
local slice = builtin.slice
local print = builtin.print

-----------------------------------------------------------------------------
local string = "Hello World"
print(slice(string, 0, 5))

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

