
--// Compiled using Roblox.py \--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, classsmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import__, classlist, py  = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
local newlist = list {1, 2, 3, 4, 5}
newlist.append(6)
newlist.append(7)
newlist.append(8)
for item in newlist do
    print(item)
end
print(newlist[0])
print(newlist[1])
newlist.sort()
newlist.reverse()