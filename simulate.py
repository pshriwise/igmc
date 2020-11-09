import numpy as np
from numpy.random import rand

import openmc

from py_iga import ParticleGenerator, Geometry

def simulate():

    ## Temporary Parameter Storage ##
    n_particles = 1000
    e_min = 1E-03
    majorant_xs = 10
    total_xs = 9.9
    seed = 110

    np.random.seed(seed)

    particle_generator = ParticleGenerator()

    geom = Geometry()

    # simple pincell geometry
    fuel_cyl = openmc.ZCylinder(r=1.5)
    clad_cyl = openmc.ZCylinder(r=1.7)

    fuel_cell = openmc.Cell(region= -fuel_cyl)
    clad_cell = openmc.Cell(region=+fuel_cyl & -clad_cyl)
    water_cell = openmc.Cell(region=+clad_cyl)

    # simple geometry region
    geom.add_cell(fuel_cell, 15.0)
    geom.add_cell(clad_cell, 10.0)
    geom.add_cell(water_cell, 2.0)

    for _ in range(n_particles):
        p = particle_generator()
        while p.e > e_min:
            p.advance(geom.majorant)
            p.locate(geom)

            if not p.cell:
                break

            if rand() < p.xs / geom.majorant:
                p.scatter()

        print(p)

if __name__ == "__main__":
    simulate()
