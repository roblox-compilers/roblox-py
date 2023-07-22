from shared.Hello import FluidCalculation as Fluids

newFluid = Fluids(10, 10, 10, 10, 10)
newFluid.step(10)
print(newFluid.width, newFluid.height, newFluid.depth, newFluid.viscosity, newFluid.density, newFluid.velocity, newFluid.pressure)