--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)


-----------------------------------------------------------------------------
local examplelib = import("examplelib")
local submodule = import("examplelib.submodule")
local mysubsubmodule = import("examplelib.submodule.subsubmodule")
local submodule = import("examplefromlib", "submodule")
local mysubsubmodule = import("examplefromlib.submodule", "mysubsubmodule")
local mysubmodule2 = import("examplefromlib", "submodule")
local mysubsubmodule3 = import("examplefromlib.submodule", "subsubmodule")