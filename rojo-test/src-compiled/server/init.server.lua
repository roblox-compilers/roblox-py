--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = _G.pyc.py

local id = builtin.id
local int = builtin.int

-----------------------------------------------------------------------------
local Fluids = import("shared.Hello", "FluidCalculation")
local newFluid = Fluids(10, 10, 10, 10, 10)
newFluid.step(10)
print(newFluid.width, newFluid.height, newFluid.depth, newFluid.viscosity, newFluid.density, newFluid.velocity, newFluid.pressure)