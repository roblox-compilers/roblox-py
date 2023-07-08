--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import__, classlist, py  = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
--[[ 
XL.py (Stands for Extralarge)

A test script for the Roblox.py compiler that uses all of the python 3.13 features.
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