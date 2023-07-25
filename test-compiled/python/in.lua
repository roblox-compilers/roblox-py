--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local dict = builtin.dict
local table = builtin.table
local operator_in = builtin.operator_in
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local table = dict {["a"] = "b", ["c"] = "d"}
if (operator_in("a", table)) then
    print("a is present in table")
end

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

