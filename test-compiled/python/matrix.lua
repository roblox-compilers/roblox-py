--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local list = builtin.list
local range = builtin.range
local len = builtin.len
local int = builtin.int
local print = builtin.print

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

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------
