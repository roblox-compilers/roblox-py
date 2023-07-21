--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local list = builtin.list
local int = builtin.int

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