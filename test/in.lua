--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
local table = dict {[stringmeta "a"] = stringmeta "b", [stringmeta "c"] = stringmeta "d"}
if (operator_in(stringmeta "a", table)) then
    print(stringmeta "a is present in table")
end