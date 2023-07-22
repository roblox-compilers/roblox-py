--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = _G.pyc.py

local id = builtin.id
local class = builtin.class
local list = builtin.list
local range = builtin.range

-----------------------------------------------------------------------------
--[[ 
Simple fluid simulation 3d, based on the Navier-Stokes equations.
 ]]
local profiles = import("", "metadata")
local FluidCalculation = class(function(FluidCalculation)
    function FluidCalculation.__init__(self, width, height, depth, viscosity, density)
        self.width = (width or profiles.default.width)
        self.height = (height or profiles.default.height)
        self.depth = (depth or profiles.default.depth)
        self.viscosity = (viscosity or profiles.default.viscosity)
        self.density = (density or profiles.default.density)
        self.velocity = (function() local result = list {} for x in range(width) do result.append((function() local result = list {} for y in range(height) do result.append((function() local result = list {} for z in range(depth) do result.append(0.0) end return result end)()) end return result end)()) end return result end)()
        self.pressure = (function() local result = list {} for x in range(width) do result.append((function() local result = list {} for y in range(height) do result.append((function() local result = list {} for z in range(depth) do result.append(0.0) end return result end)()) end return result end)()) end return result end)()
    end
    function FluidCalculation.step(self, dt)
        for x in range(1, (self.width - 1)) do
            for y in range(1, (self.height - 1)) do
                for z in range(1, (self.depth - 1)) do
                    local u = self.velocity[x][y][z][0]
                    local v = self.velocity[x][y][z][1]
                    local w = self.velocity[x][y][z][2]
                    u = (u + (dt * ((((-u * (u - self.velocity[(x - 1)][y][z][0])) - (v * (u - self.velocity[x][(y - 1)][z][0]))) - (w * (u - self.velocity[x][y][(z - 1)][0]))) + (self.viscosity * ((((((self.velocity[(x + 1)][y][z][0] + self.velocity[(x - 1)][y][z][0]) + self.velocity[x][(y + 1)][z][0]) + self.velocity[x][(y - 1)][z][0]) + self.velocity[x][y][(z + 1)][0]) + self.velocity[x][y][(z - 1)][0]) - (6 * u))))))
                    v = (v + (dt * ((((-u * (v - self.velocity[(x - 1)][y][z][1])) - (v * (v - self.velocity[x][(y - 1)][z][1]))) - (w * (v - self.velocity[x][y][(z - 1)][1]))) + (self.viscosity * ((((((self.velocity[(x + 1)][y][z][1] + self.velocity[(x - 1)][y][z][1]) + self.velocity[x][(y + 1)][z][1]) + self.velocity[x][(y - 1)][z][1]) + self.velocity[x][y][(z + 1)][1]) + self.velocity[x][y][(z - 1)][1]) - (6 * v))))))
                    w = (w + (dt * ((((-u * (w - self.velocity[(x - 1)][y][z][2])) - (v * (w - self.velocity[x][(y - 1)][z][2]))) - (w * (w - self.velocity[x][y][(z - 1)][2]))) + (self.viscosity * ((((((self.velocity[(x + 1)][y][z][2] + self.velocity[(x - 1)][y][z][2]) + self.velocity[x][(y + 1)][z][2]) + self.velocity[x][(y - 1)][z][2]) + self.velocity[x][y][(z + 1)][2]) + self.velocity[x][y][(z - 1)][2]) - (6 * w))))))
                    self.velocity[x][y][z][0] = u
                    self.velocity[x][y][z][1] = v
                    self.velocity[x][y][z][2] = w
                end
            end
        end
        for i in range(20) do
            for x in range(1, (self.width - 1)) do
                for y in range(1, (self.height - 1)) do
                    for z in range(1, (self.depth - 1)) do
                        self.pressure[x][y][z] = (((((((self.pressure[(x + 1)][y][z] + self.pressure[(x - 1)][y][z]) + self.pressure[x][(y + 1)][z]) + self.pressure[x][(y - 1)][z]) + self.pressure[x][y][(z + 1)]) + self.pressure[x][y][(z - 1)]) + (self.density * (((((self.velocity[x][y][z][0] - self.velocity[(x - 1)][y][z][0]) + self.velocity[x][y][z][1]) - self.velocity[x][(y - 1)][z][1]) + self.velocity[x][y][z][2]) - self.velocity[x][y][(z - 1)][2]))) / 6.0)
                    end
                end
            end
        end
        for x in range(1, (self.width - 1)) do
            for y in range(1, (self.height - 1)) do
                for z in range(1, (self.depth - 1)) do
                    self.velocity[x][y][z][0] = (self.velocity[x][y][z][0] - ((dt * (self.pressure[(x + 1)][y][z] - self.pressure[(x - 1)][y][z])) / (2.0 * self.density)))
                    self.velocity[x][y][z][1] = (self.velocity[x][y][z][1] - ((dt * (self.pressure[x][(y + 1)][z] - self.pressure[x][(y - 1)][z])) / (2.0 * self.density)))
                    self.velocity[x][y][z][2] = (self.velocity[x][y][z][2] - ((dt * (self.pressure[x][y][(z + 1)] - self.pressure[x][y][(z - 1)])) / (2.0 * self.density)))
                end
            end
        end
    end
    return FluidCalculation
end, {})