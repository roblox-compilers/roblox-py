--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import__  = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
local newdict = dict {}
local newdict[stringmeta "one"] = 1
local newdict[stringmeta "two"] = 2
local newdict[stringmeta "three"] = 3
local newdict[stringmeta "four"] = 4
for key in newdict do
    print(key, newdict[key])
end