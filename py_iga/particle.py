from collections.abc import Iterable
from numbers import Real

import numpy as np
from numpy.random import rand

from .distributions import isotropic_dir

from .mixin import IDManagerMixin
from . import checkvalue as cv


class Particle(IDManagerMixin):
    """
    Particle class. Used to represent a particle in phase space.

    Parameters
    ----------
    id : int
        Particle ID. Defaults to next value provided by the mixin class.
    r : iterable of 3 floats
        Spatial location in Cartesian space. Defaults to the origin.
    u : iterable of 3 floats
        Unit vector representing the direction. Defaults to (1.0, 0.0, 0.0)
    e : float


    Attributes
    ----------
    id : int
        Particle ID
    r : ndarray of 3 floats
        Position in Cartesian space
    u : ndarray of 3 floats
        Directional unit vector
    e : float
        Particle energy
    xs : float
        Total cross section of the current cell.
    cell : openmc.Cell
        Cell containing the particle
    n_events : int
        Number of total particle events.
    n_advance_events : int
        Number of advance events.
    n_scatter_events : int
        Number of scatter events.
    """
    next_id = 1
    used_ids = set()

    def __init__(self, id=None, r=None, u=None, e=None):

        self.id = id
        self.r = r if r else (0.0, 0.0, 0.0)
        self.u = u if u else (1.0, 0.0, 0.0)
        self.e = e if e else 10.0

        # statistics
        self.advance_events = 0
        self.scatter_events = 0
        self.distance_traveled = 0.0

        # geometry
        self._cell = None

        # cross-section
        self._xs = None

    def __repr__(self):
        out = "Particle {} terminated:\n".format(self.id)
        out += "\tPosition: {}\n".format(self.r)
        out += "\tDirection: {}\n".format(self.u)
        out += "\tEnergy: {}\n".format(self.e)
        out += "\tDistance traveled: {}\n".format(self.distance_traveled)
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
        self.distance_traveled += dist

    def scatter(self):
        # decrement energy
        self.e *= 0.5
        # sample direction
        self.u = isotropic_dir()
        # increment counter
        self.scatter_events += 1

    def locate(self, geometry):
        self._cell, self._xs = geometry.locate(self.r, self.u)

    @property
    def xs(self):
        if not self._xs:
            raise RuntimeError("Cross-section called for but not set")

        return self._xs

    @property
    def cell(self):
        if not self._cell:
            raise RuntimeError("Cell called for but not set")

        return self._cell

    @property
    def n_events(self):
        return self.scatter_events + self.advance_events

    @property
    def n_advance_events(self):
        return self.advance_events

    @property
    def n_scatter_events(self):
        return self.scatter_events
