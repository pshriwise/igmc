import numpy as np
from numpy.random import rand

import openmc

from py_iga import ParticleGenerator

def simulate():

    ## Temporary Parameter Storage ##
    n_particles = 1000
    e_min = 1E-03
    majorant_xs = 10
    total_xs = 9.9
    seed = 110

    np.random.seed(seed)

    particle_generator = ParticleGenerator()

    # simple pincell geometry
    fuel_cyl = openmc.ZCylinder(r=1.5)
    clad_cyl = openmc.ZCylinder(r=1.7)

    fuel_cell = openmc.Cell(region= -fuel_cyl)
    clad_cell = openmc.Cell(region=+fuel_cyl & -clad_cyl)
    water_cell = openmc.Cell(region=+clad_cyl)

    geom = openmc.Geometry([fuel_cell, clad_cell, water_cell])

    xs_dict = {fuel_cell : 15.0,
               clad_cell : 10.0,
               water_cell : 2.0}

    majorant = max(val for val in xs_dict.values())

    for _ in range(n_particles):
        p = particle_generator()
        while p.e > e_min:
            p.advance(majorant)
            p.locate(geom, xs_dict)

            if not p.cell:
                break

            if rand() < p.xs / majorant:
                p.scatter()

        print(p)

if __name__ == "__main__":
    simulate()
