--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import__  = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
local Example = class(function(Example)
    function Example.__init__(self, name)
        self.name = name
    end
    function Example.print_name(self)
        print(self.name)
    end
    function Example.sethobby(self, hobby)
        self.hobby = hobby
    end
    function Example.printhobby(self)
        print(self.hobby)
    end
    function Example.setage(self, age)
        self.age = age
    end
    function Example.printage(self)
        print(self.age)
    end
    return Example
end, {})
local new = Example(stringmeta "John")
new.print_name()
new.sethobby(stringmeta "Roblox Game Development")
new.printhobby()