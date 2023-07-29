--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local match = builtin.match
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local x = "10"
match(x, {
[10] = function()
    print("x is 10")
end,
[20] = function()
    print("x is 20")
end,
["default"] = function()
    print("x is not 10 or 20")
end,
})

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

