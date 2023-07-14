--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local all = builtin.all
local compile = builtin.compile
local range = builtin.range
local int = builtin.int
local stringmeta = builtin.stringmeta
local str = builtin.str
local open = builtin.open
local id = builtin.id
local asynchronousfunction = builtin.asynchronousfunction
local dict = builtin.dict
local class = builtin.class
local staticmethod = builtin.staticmethod
local operator_in = builtin.operator_in

-----------------------------------------------------------------------------
--[[ 
XL.py (Stands for Extralarge)

A test script for the roblox-pyc compiler that uses all of the python 3.13 features.
 ]]
local y = require "x"
local SSS = py.services.ServerScriptService
for i in range(10) do
    print(i)
end
while true do
    print(stringmeta "This is an infinite loop")
    break
end
do
    local f = open(stringmeta "test.txt", stringmeta "w")
    f.write(stringmeta "This is a test file")
end
local function test()
    print(stringmeta "This is a function, ran inside of the async function")
end
local async_test = asynchronousfunction(function()
    print(stringmeta "This is an async function")
    coroutine.yield(test())
end)
async_test()
local data = dict {[stringmeta "test"] = stringmeta "This is a test"}
for i in data do
    print(i)
end
local Test = class(function(Test)
    function Test.__init__(self)
        print(stringmeta "This is a class")
    end
    function Test.test(self)
        print(stringmeta "This is a class method")
    end
    function Test.static_test()
        print(stringmeta "This is a static method")
    end
    Test.static_test = staticmethod(Test.static_test)
    function Test.class_test(cls)
        print(stringmeta "This is a class method")
    end
    Test.class_test = classmethod(Test.class_test)
    return Test
end, {})
local new_test = Test()
new_test.test()
new_test.static_test()
new_test.class_test()
local string = stringmeta "This"
local string2 = stringmeta "This is a test string"
if (not operator_in(string1, string2)) then
    print(stringmeta "x is not in y")
else
    print(stringmeta "x is in y")
end