--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local list = builtin.list
local str = builtin.str
local id = builtin.id
local int = builtin.int
local operator_in = builtin.operator_in
local min = builtin.min

-----------------------------------------------------------------------------
local examplelibrary = import("example")
local newSignal = import(signal., newSignal)
local ValidPlayers = list {stringmeta "builderman"}
local function onTouch(touch)
    print(stringmeta "Spawn has been touched by", touch.Name)
end
onTouch = py.Workspace.Spawn.Touched(onTouch)
local function onPlrAdd(plr)
    if (operator_in(plr.Name, ValidPlayers)) then
        print(stringmeta "Admin", plr.Name, stringmeta "has joined the game!!")
    end
end
onPlrAdd = py.Players.PlayerAdded(onPlrAdd)
examplelibrary()
local function onSignal()
    print(stringmeta "Signal received!")
end
onSignal = newSignal(onSignal)
onSignal.Fire()