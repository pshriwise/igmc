from collections.abc import Callable

import numpy as np
from numpy.random import rand

from .particle import Particle
from .distributions import isotropic_dir
from. import checkvalue as cv


class ParticleGenerator:

    def __init__(self, space=None, angle=None, energy=None):
        self.space = space if space else self._default_spatial
        self.angle = angle if angle else self._default_angle
        self.energy = energy if energy else self._default_engery

    def __call__(self):
        xyz = self.space()
        uvw = self.angle()
        energy = self.energy()
        return Particle(r=xyz, u=uvw, e=energy)

    def __next__(self):
        return self()

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, val):
        cv.check_type('spatial distribution', val, Callable)
        self._space = val

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        cv.check_type('angular distribution', val, Callable)
        self._angle = val

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, val):
        cv.check_type('energy distribution', val, Callable)
        self._energy = val

    @staticmethod
    def _default_spatial():
        return (0.0, 0.0, 0.0)

    @staticmethod
    def _default_angle():
        return isotropic_dir()

    @staticmethod
    def _default_engery():
        return 10.0
