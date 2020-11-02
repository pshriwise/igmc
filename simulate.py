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
    cell = openmc.Cell()
    geom.add_cell(cell, 9.9)

    for _ in range(n_particles):
        p = particle_generator()
        while p.e > e_min:
            p.advance(geom.majorant)
            p.locate(geom)
            if rand() < p.xs / geom.majorant:
                p.scatter()

        print(p)

if __name__ == "__main__":
    simulate()
