--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local list = builtin.list
local int = builtin.int
local print = builtin.print

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

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

