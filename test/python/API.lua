--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local list = builtin.list
local id = builtin.id
local int = builtin.int
local print = builtin.print
local Spawn = builtin.Spawn
local Workspace = builtin.Workspace
local operator_in = builtin.operator_in
local min = builtin.min
local game = builtin.game

-----------------------------------------------------------------------------
local examplelibrary = import("example")
local newSignal = import("signal", "new")
local ValidPlayers = list {"builderman"}
local function onTouch(touch)
    print("Spawn has been touched by", touch.Name)
end
onTouch = py.Workspace.Spawn.Touched(onTouch)
local function onPlrAdd(plr)
    if (operator_in(plr.Name, ValidPlayers)) then
        print("Admin", plr.Name, "has joined the game!!")
    end
end
onPlrAdd = py.Players.PlayerAdded(onPlrAdd)
examplelibrary()
local function onSignal()
    print("Signal received!")
end
onSignal = newSignal(onSignal)
onSignal.Fire()

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

