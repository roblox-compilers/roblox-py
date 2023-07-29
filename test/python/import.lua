--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py


-----------------------------------------------------------------------------
local examplelib = import("examplelib")
local submodule = import("examplelib.submodule")
local mysubsubmodule = import("examplelib.submodule.subsubmodule")
local submodule = import("examplefromlib", "submodule")
local mysubsubmodule = import("examplefromlib.submodule", "mysubsubmodule")
local mysubmodule2 = import("examplefromlib", "submodule")
local mysubsubmodule3 = import("examplefromlib.submodule", "subsubmodule")

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

