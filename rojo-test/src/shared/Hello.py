"""
Simple fluid simulation 3d, based on the Navier-Stokes equations.
"""
from l import metadata as profiles
class FluidCalculation:
    def __init__(self, width, height, depth, viscosity, density):
        self.width = width or profiles.default.width
        self.height = height or profiles.default.height
        self.depth = depth or profiles.default.depth
        self.viscosity = viscosity or profiles.default.viscosity
        self.density = density or profiles.default.density
        self.velocity = [[[0.0 for z in range(depth)] for y in range(height)] for x in range(width)]
        self.pressure = [[[0.0 for z in range(depth)] for y in range(height)] for x in range(width)]

    def step(self, dt):
        # Calculate velocity
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                for z in range(1, self.depth - 1):
                    u = self.velocity[x][y][z][0]
                    v = self.velocity[x][y][z][1]
                    w = self.velocity[x][y][z][2]
                    u += dt * (-u * (u - self.velocity[x - 1][y][z][0]) -
                               v * (u - self.velocity[x][y - 1][z][0]) -
                               w * (u - self.velocity[x][y][z - 1][0]) +
                               self.viscosity * ((self.velocity[x + 1][y][z][0] +
                                                  self.velocity[x - 1][y][z][0] +
                                                  self.velocity[x][y + 1][z][0] +
                                                  self.velocity[x][y - 1][z][0] +
                                                  self.velocity[x][y][z + 1][0] +
                                                  self.velocity[x][y][z - 1][0]) -
                                                 6 * u))
                    v += dt * (-u * (v - self.velocity[x - 1][y][z][1]) -
                               v * (v - self.velocity[x][y - 1][z][1]) -
                               w * (v - self.velocity[x][y][z - 1][1]) +
                               self.viscosity * ((self.velocity[x + 1][y][z][1] +
                                                  self.velocity[x - 1][y][z][1] +
                                                  self.velocity[x][y + 1][z][1] +
                                                  self.velocity[x][y - 1][z][1] +
                                                  self.velocity[x][y][z + 1][1] +
                                                  self.velocity[x][y][z - 1][1]) -
                                                 6 * v))
                    w += dt * (-u * (w - self.velocity[x - 1][y][z][2]) -
                               v * (w - self.velocity[x][y - 1][z][2]) -
                               w * (w - self.velocity[x][y][z - 1][2]) +
                               self.viscosity * ((self.velocity[x + 1][y][z][2] +
                                                  self.velocity[x - 1][y][z][2] +
                                                  self.velocity[x][y + 1][z][2] +
                                                  self.velocity[x][y - 1][z][2] +
                                                  self.velocity[x][y][z + 1][2] +
                                                  self.velocity[x][y][z - 1][2]) -
                                                 6 * w))
                    self.velocity[x][y][z][0] = u
                    self.velocity[x][y][z][1] = v
                    self.velocity[x][y][z][2] = w

        # Calculate pressure
        for i in range(20):
            for x in range(1, self.width - 1):
                for y in range(1, self.height - 1):
                    for z in range(1, self.depth - 1):
                        self.pressure[x][y][z] = ((self.pressure[x + 1][y][z] +
                                                   self.pressure[x - 1][y][z] +
                                                   self.pressure[x][y + 1][z] +
                                                   self.pressure[x][y - 1][z] +
                                                   self.pressure[x][y][z + 1] +
                                                   self.pressure[x][y][z - 1]) +
                                                  self.density * (self.velocity[x][y][z][0] -
                                                                  self.velocity[x - 1][y][z][0] +
                                                                  self.velocity[x][y][z][1] -
                                                                  self.velocity[x][y - 1][z][1] +
                                                                  self.velocity[x][y][z][2] -
                                                                  self.velocity[x][y][z - 1][2])) / 6.0

        # Update velocity
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                for z in range(1, self.depth - 1):
                    self.velocity[x][y][z][0] -= dt * (self.pressure[x + 1][y][z] -
                                                       self.pressure[x - 1][y][z]) / (2.0 * self.density)
                    self.velocity[x][y][z][1] -= dt * (self.pressure[x][y + 1][z] -
                                                       self.pressure[x][y - 1][z]) / (2.0 * self.density)
                    self.velocity[x][y][z][2] -= dt * (self.pressure[x][y][z + 1] -
                                                       self.pressure[x][y][z - 1]) / (2.0 * self.density)