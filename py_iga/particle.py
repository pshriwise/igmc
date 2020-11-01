from collections.abc import Iterable
from numbers import Real

from py_iga.mixin import IDManagerMixin
import py_iga.checkvalue as cv

class Particle(IDManagerMixin):

    next_id = 1
    used_ids = set()

    def __init__(self, id=None, r=None, u=None):

        self.id = id

        if r:
            self.r = r
        else:
            self.r = (0.0, 0.0, 0.0)

        if u:
            self.u = u
        else:
            self.u = (1.0, 0.0, 0.0)

    def __repr__(self):
        out = "Particle {}:\n".format(self.id)
        out += "\t Position: {}\n".format(self.r)
        out += "\t Direction: {}\n".format(self.u)
        return out

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, val):
        cv.check_type('position', val, Iterable, Real)
        cv.check_length('position', val, 3)
        self._r = val

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, val):
        cv.check_type('direction', val, Iterable, Real)
        cv.check_length('direction', val, 3)
        self._u = val