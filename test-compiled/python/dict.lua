--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local dict = builtin.dict
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local newdict = dict {}
newdict["one"] = 1
newdict["two"] = 2
newdict["three"] = 3
newdict["four"] = 4
for key in newdict do
    print(key, newdict[key])
end

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

