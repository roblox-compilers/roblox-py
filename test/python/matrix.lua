--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local list = builtin.list
local range = builtin.range
local len = builtin.len
local int = builtin.int

-----------------------------------------------------------------------------
local X = list {list {12, 7}, list {4, 5}, list {3, 8}}
local result = list {list {0, 0, 0}, list {0, 0, 0}}
for i in range(len(X)) do
    for j in range(len(X[0])) do
        result[j][i] = X[i][j]
    end
end
for r in result do
    print(r)
end