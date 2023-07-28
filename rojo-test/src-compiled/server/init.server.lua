--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local id = builtin.id
local shared = builtin.shared
local int = builtin.int
local print = builtin.print
local os = builtin.os

-----------------------------------------------------------------------------
local Fluids = import("shared.Hello", "FluidCalculation")
local newFluid = Fluids(10, 10, 10, 10, 10)
newFluid.step(10)
print(newFluid.width, newFluid.height, newFluid.depth, newFluid.viscosity, newFluid.density, newFluid.velocity, newFluid.pressure)

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

