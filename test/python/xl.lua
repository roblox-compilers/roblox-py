--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local python = builtin.python
local all = builtin.all
local compile = builtin.compile
local script = builtin.script
local range = builtin.range
local int = builtin.int
local print = builtin.print
local open = builtin.open
local id = builtin.id
local asynchronousfunction = builtin.asynchronousfunction
local coroutine = builtin.coroutine
local dict = builtin.dict
local class = builtin.class
local staticmethod = builtin.staticmethod
local str = builtin.str
local string = builtin.string
local operator_in = builtin.operator_in

-----------------------------------------------------------------------------
--[[ 
XL.py (Stands for Extralarge)

A test script for the roblox-pyc compiler that uses all of the python 3.13 features.
 ]]
local y = import("x")
local SSS = py.services.ServerScriptService
for i in range(10) do
    print(i)
end
while true do
    print("This is an infinite loop")
    break
end
do
    local f = open("test.txt", "w")
    f.write("This is a test file")
end
local function test()
    print("This is a function, ran inside of the async function")
end
local async_test = asynchronousfunction(function()
    print("This is an async function")
    coroutine.yield(test())
end)
async_test()
local data = dict {["test"] = "This is a test"}
for i in data do
    print(i)
end
local Test = class(function(Test)
    function Test.__init__(self)
        print("This is a class")
    end
    function Test.test(self)
        print("This is a class method")
    end
    function Test.static_test()
        print("This is a static method")
    end
    Test.static_test = staticmethod(Test.static_test)
    function Test.class_test(cls)
        print("This is a class method")
    end
    Test.class_test = classmethod(Test.class_test)
    return Test
end, {})
local new_test = Test()
new_test.test()
new_test.static_test()
new_test.class_test()
local string = "This"
local string2 = "This is a test string"
if (not operator_in(string, string2)) then
    print("x is not in y")
else
    print("x is in y")
end

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

