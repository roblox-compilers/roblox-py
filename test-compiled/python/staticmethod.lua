--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local int = builtin.int
local format = builtin.format
local exec = builtin.exec
local formatmod = builtin.formatmod
local print = builtin.print
local staticmethod = builtin.staticmethod
local class = builtin.class

-----------------------------------------------------------------------------
local function foo(x)
    print((formatmod("executing foo(%s)", x)))
end
foo = staticmethod(foo)
local A = class(function(A)
    A.foo = foo
    return A
end, {})
local a = A()
a.foo("hi")

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

