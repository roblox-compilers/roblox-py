--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
-----------------------------------------------------------------------------
local X = list {list {12, 7}, list {4, 5}, list {3, 8}}
local result = list {list {0, 0, 0}, list {0, 0, 0}}
for i in range(len(X)) do
    for j in range(len(X[0])) do
        local result[j][i] = X[i][j]
    end
end
for r in result do
    print(r)
end