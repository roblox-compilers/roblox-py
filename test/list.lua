--// Compiled using Roblox.py \\--
		
		
------------------------------------ BUILT IN -------------------------------
local stringmeta, list, dict, staticmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice = unpack(require(game.ReplicatedStorage["Roblox.py"])(script))
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