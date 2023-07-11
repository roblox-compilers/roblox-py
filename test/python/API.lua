
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local str = builtin.str
local int = builtin.int

-----------------------------------------------------------------------------
local function childAdded()
    print(stringmeta "Child added")
end
childAdded = py.Workspace.ChildAdded(childAdded)
local function childRemoved()
    print(stringmeta "Child removed")
end
childRemoved = py.Workspace.ChildRemoved(childRemoved)