import numpy as np
from numpy.random import rand

from py_iga.particle_gen import ParticleGenerator


def simulate():

    ## Temporary Parameter Storage ##
    n_particles = 1000
    e_min = 1E-03
    majorant_xs = 10
    total_xs = 9.9
    seed = 110

    np.random.seed(seed)

    particle_generator = ParticleGenerator()

    for i in range(n_particles):
        p = particle_generator()

        while p.e > e_min:
            p.advance(majorant_xs)

            if rand() < total_xs / majorant_xs:
                p.scatter()

        print(p)

if __name__ == "__main__":
    simulate()
