from collections.abc import Iterable
from numbers import Real

import numpy as np
from numpy.random import rand

from distributions import isotropic_dir

from py_iga.mixin import IDManagerMixin
import py_iga.checkvalue as cv


class Particle(IDManagerMixin):

    next_id = 1
    used_ids = set()

    def __init__(self, id=None, r=None, u=None, e=None):

        self.id = id
        self.r = r if r else (0.0, 0.0, 0.0)
        self.u = u if u else (1.0, 0.0, 0.0)
        self.e = e if e else 10.0

        self.advance_events = 0
        self.scatter_events = 0

    def __repr__(self):
        out = "Particle {} terminated:\n".format(self.id)
        out += "\tPosition: {}\n".format(self.r)
        out += "\tDirection: {}\n".format(self.u)
        out += "\tEnergy: {}\n".format(self.e)
        out += "\tScattering Events: {}\n".format(self.n_scatter_events)
        out += "\tAdvance Events: {}\n".format(self.n_advance_events)
        out += "\tTotal Events: {}\n".format(self.n_events)
        return out

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, val):
        cv.check_type('position', val, Iterable, Real)
        cv.check_length('position', val, 3)
        self._r = np.asarray(val)

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, val):
        cv.check_type('direction', val, Iterable, Real)
        cv.check_length('direction', val, 3)
        self._u = np.asarray(val)

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, val):
        cv.check_type('energy', val, Real)
        self._e = val

    def advance(self, majorant):
        # sample distance
        dist = -np.log(rand()) / majorant
        # advance particle
        self.r = self.r + dist * self.u
        # increment counter
        self.advance_events += 1

    def scatter(self):
        # decrement energy
        self.e = (0.5 + 0.5 * rand()) * self.e
        # sample direction
        self.u = isotropic_dir()
        # increment counter
        self.scatter_events += 1

    @property
    def n_events(self):
        return self.scatter_events + self.advance_events

    @property
    def n_advance_events(self):
        return self.advance_events

    @property
    def n_scatter_events(self):
        return self.scatter_events
