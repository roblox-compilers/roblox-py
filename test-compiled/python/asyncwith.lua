--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local asynchronousfunction = builtin.asynchronousfunction
local open = builtin.open
local coroutine = builtin.coroutine
local int = builtin.int
local print = builtin.print

-----------------------------------------------------------------------------
local async_with = asynchronousfunction(function()
    do
        local f = open("test.txt")
        local contents = coroutine.yield(f.read())
        print(contents)
    end
end)

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

