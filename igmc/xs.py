from collections.abc import Iterable
from numbers import Real

from .binary_search import binary_search
from . import checkvalue as cv

class CEXS:
    """
    Continuous-energy cross-section class. Used to compute cross
    sections from provided point-wise data.

    Parameters
    ----------
    e_grid : Iterable of float
       Energy values for the point-wise data (in eV)
    data : Iterable of float
       Cross-section data values (b)

    Attributes
    ----------
    e_grid : Iterable of float
       Energy values for the point-wise data (in eV)
    xs_vals : Iterable of float
       Cross-section data values (b)
    """
    def __init__(self, e_grid, data):
        self.e_grid = e_grid
        self.xs_vals = data

    @property
    def e_grid(self):
        return self._e_grid

    @e_grid.setter
    def e_grid(self, vals):
        cv.check_type('e_grid', vals, Iterable, Real)
        self._e_grid = vals

    @property
    def xs_vals(self):
        return self._data

    @xs_vals.setter
    def xs_vals(self, vals):
        cv.check_type('xs data', vals, Iterable, Real)
        self._data = vals

    def calculate_xs(self, e):
        """
        Compute the cross section at the specified energy value
        """
        # return only value if this is a flat xs
        if len(self.xs_vals) == 1:
            return self.xs_vals[0]

        # determine energy values to interpolate between
        idx = binary_search(self.e_grid, e)
        # calculate interpolation factor
        f = e - self.e_grid[idx]
        f /= self.e_grid[idx + 1] - self.e_grid[idx]

        xs = f * self.xs_vals[idx] + (1 - f) * self.xs_vals[idx + 1]

        return xs
