--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local format = builtin.format
local formatmod = builtin.formatmod
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local text = (formatmod("%s is my name", "John"))
print(text)

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------
