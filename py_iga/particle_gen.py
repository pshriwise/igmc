import numpy as np
from numpy.random import rand


from .particle import Particle

class ParticleGenerator:

    def __call__(self):
        # all particles start on the origin for now
        xyz = (0.0, 0.0, 0.0)

        # isotropic sampling in direction
        phi = rand() * 2.0 * np.pi
        t = -1.0 + 2.0 * rand()

        u = np.sqrt(1 - t*t) * np.cos(phi)
        v = np.sqrt(1 - t*t) * np.sin(phi)
        w = t

        uvw = (u, v, w)

        return Particle(r=xyz, u=uvw)
