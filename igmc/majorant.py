from collections.abc import Iterable
from collections import defaultdict
from numbers import Real
import sys

from .binary_search import binary_search
from . import checkvalue as cv

import numpy as np
import openmc
from openmc.plotter import calculate_cexs

class data2D:
    """
    Helper class for tracking iteration over 2D data

    Parameters
    ----------
    x_vals : Iterable of float
        x values of the data

    y_vals : Iterable of float
        y values of the data

    Attributes
    ----------
    x_vals : Iterable of floats
        Interal storage of the data x values
    y_vals : Iterable of floats
        Internal storage of the data y values
    idx : int
        Current index into the data. Used to track
        iteration for external algorithms.
    """

    def __init__(self, x_vals, y_vals):
        cv.check_type('x_vals', x_vals, Iterable, Real)
        cv.check_type('y_vals', y_vals, Iterable, Real)
        assert(len(x_vals) == len(y_vals))
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.idx = 0

    def __iadd__(self, val):
        """
        Advance index in-place
        """
        assert(isinstance(val, int))
        self.idx += val
        return self

    def complete(self):
        """
        Check to see if the index has gone
        beyond the size of the data.
        """
        return self.idx >= len(self.x_vals)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            out = self.get()
        except IndexError:
            raise StopIteration
        self.idx += 1
        return out

    def get_x(self, i=None):
        """
        Return the x value for the current index
        """
        if i is None:
            i = self.idx
        return self.get(i)[0]

    def get_y(self, i=None):
        """
        Return the y value for the current index
        """
        if i is None:
            i = self.idx
        return self.get(i)[1]

    def get(self, i=None):
        """
        Return the x-y value pair pair at index as a tuple
        """
        if i is None:
            i = self.idx

        if i >= len(self.x_vals):
            raise IndexError("Cannot return value at index {} "
                            "for data with size {}".format(i, len(self.x_vals)))

        return (self.x_vals[i], self.y_vals[i])

    def pop(self):
        """
        Return the current x-y tuple pair
        and advance the internal index.
        """
        out = self.get()
        self += 1
        return out

    def advance(self, x_val):
        """
        Advance the internal index up to the
        specified x value.

        Parameters
        ----------
        x_val : float
            X value to advance the internal index
            to.
        """
        x = self.get()[0]
        while(x <= x_val):
            self += 1
            x = self.get()[0]

    def prev(self):
        """
        Get the value right behind the current index
        """
        return self.get(self.idx - 1)

class Max2D:
    """
    Storage of 2D data that can be updated, creating a new
    pointwise dataset representing the maximum of both datasets.

    Attributes
    ----------
    x_values : Iterable of floats
        x data
    y_values : Iterable of floats
        y data
    """
    def __init__(self):
        self._x_values = None
        self._y_values = None

    @property
    def x_values(self):
        return self._x_values

    @property
    def y_values(self):
        return self._y_values

    def __iter__(self):
        yield self.x_values
        yield self.y_values

    def get(self, idx):
        return (self._x_values[idx], self._y_values[idx])

    def update(self, other_x, other_y):
        """
        Update the internal datasets to be the maximum of
        the internal and provided pointwise datasets.

        Parameters
        ----------
        other_x : Iterable of float
            x values of the other dataset
        other_y : Iterable of float
            y values of the other dataset
        """
        # early exit if there is no current data
        if self._x_values is None:
            self._x_values = other_x
            self._y_values = other_y
            return

        xs_a = data2D(self._x_values, self._y_values)
        xs_b = data2D(other_x, other_y)

        # some variables to track xs information
        current_xs = None
        other_xs = None

        # output values
        xs_out = []
        mask = [True]

        # select the first point along the energy axis
        if xs_a.get_x() < xs_b.get_x():
            xs_out.append(xs_a.pop())
            current_xs = xs_a
            other_xs = xs_b
        elif xs_a.get_x() > xs_b.get_x():
            xs_out.append(xs_b.pop())
            current_xs = xs_b
            other_xs = xs_a
        else:
            # starting energy values are the same
            # choose the larger xs vale
            if xs_a.get_y() > xs_b.get_y():
                xs_out.append(xs_a.pop())
                current_xs = xs_a
                other_xs = xs_b
            else:
                xs_out.append(xs_b.pop())
                current_xs = xs_b
                other_xs = xs_a

        while(True):
            # get next value for current
            try:
                current_next = current_xs.get()
                other_next = other_xs.get()
                last_pnt = xs_out[-1]
            except IndexError:
                break

            above = self.is_above(last_pnt, current_next, other_next)
            nearer = other_next[0] < current_next[0]

            # for clarity
            below = not above
            farther = not nearer

            # if the next point in the other cross section is
            # above our current value, check for an intersection
            if above:
                p1 = last_pnt
                p2 = current_next
                p3 = other_xs.prev()
                p4 = other_next

                intersection = self.intersect_2d(p1, p2, p3, p4)

                mask.append(True)
                if intersection:
                    xs_out.append(intersection)
                    # switch the cross sections
                    # if there is an intersection
                    temp = other_xs
                    other_xs = current_xs
                    current_xs = temp
                else:
                    if nearer:
                        print("Warning: No intersection found for above, nearer")
                    xs_out.append(current_next)
            # if the next point in the other cross section is
            # below our current value and nearer in energy than
            # the next point in our current cross section,
            # insert a point along the segment of our current
            # cross section
            elif below and nearer:
                # compute y value
                m = (current_next[1] - last_pnt[1]) / (current_next[0] - last_pnt[0])
                d = (other_next[0] - last_pnt[0])
                xs_out.append((other_next[0], last_pnt[1] + d * m))
                mask.append(False)
            # if the next point in the other cross section is below
            # this segment and farther out, insert the next point
            # in the current cross section
            elif below and farther:
                xs_out.append(current_next)
                mask.append(True)
            # advance the cross section indices past
            # the energy of the last value in the output
            # cross section
            try:
                current_xs.advance(xs_out[-1][0])
                other_xs.advance(xs_out[-1][0])
            except:
                break

        # one or both of the cross sections should be complete
        assert(xs_b.complete() or xs_a.complete())

        energy = [pnt[0] for m, pnt in zip(mask, xs_out) if m]
        xs = [pnt[1] for m, pnt in zip(mask, xs_out) if m]

        # add any additional data
        for pnt in xs_a:
            energy.append(pnt[0])
            xs.append(pnt[1])

        for pnt in xs_b:
            energy.append(pnt[0])
            xs.append(pnt[1])

        self._x_values = energy
        self._y_values = xs

    def update_grid(self, fine_grid):
        """
        Update the current data using a new set of x-values
        (new grid must be more refined than the previous grid)

        Parameters
        ----------
        fine_grid : Iterable of float
            x values of the new x grid
        """
        assert(len(fine_grid) >= len(self.x_values))

        y_new = np.full_like(fine_grid, 0.0)

        fine_idx = 0
        x_idx = 0

        while True:

            if fine_idx >= len(fine_grid):
                break

            if x_idx >= len(self.x_values) - 2:
                break

            # current value we're calculating for
            fine_e = fine_grid[fine_idx]

            # make sure we're at the right place in the
            # original data
            while fine_e > self.x_values[x_idx + 1]:
                x_idx += 1

            # calculate the cross section value for the fine grid point
            m = (self.y_values[x_idx + 1] - self.y_values[x_idx]) / \
                (self.x_values[x_idx + 1] - self.x_values[x_idx])
            de = fine_e - self.x_values[x_idx]
            val = self.y_values[x_idx] + m * de
            y_new[fine_idx] = val

            fine_idx += 1

        self._x_values = fine_grid
        self._y_values = y_new

    @staticmethod
    def is_above(pnt1, pnt2, pnt3):
        """
        Determines if pnt3 is above or below the between pnt1 -> pnt2

        Parameters
        ----------
        pnt1 : x,y pair of floats
            First point of the line segment
        pnt2 : x,y pair of floats
            Second point of the line segment
        pnt3 : x,y pair of floats
            Point to test

        Returns
        -------
        bool : True if pnt3 if above the line, False if not
        """
        m = (pnt2[1] - pnt1[1]) / (pnt2[0] - pnt1[0])
        l = pnt1[1] + m * (pnt3[0] - pnt1[0])

        return l < pnt3[1]

    @staticmethod
    def intersect_2d(pnt1, pnt2, pnt3, pnt4):
        """
        Given 4 points, checks if the line segments (pnt1, pnt2) and
        (pnt3, pnt4) intersect.

        Parameters
        ----------
        pnt1 : x,y pair of floats
            First point of the first line segment
        pnt2 : x,y pair of floats
            Second point of the first line segment
        pnt3 : x,y pair of floats
            First point of the second line segment
        pnt4 : x,t pair of floats
            Second point of the second line segment

        Returns
        -------
        None if no intersection is found. The (x, y) location of the
        intersection if one is found.
        """
        denominator = (pnt4[0] - pnt3[0]) * (pnt1[1] - pnt2[1]) - (pnt1[0] - pnt2[0]) * (pnt4[1] - pnt3[1])
        numerator = (pnt3[1] - pnt4[1]) * (pnt1[0] - pnt3[0]) + (pnt4[0] - pnt3[0]) * (pnt1[1] - pnt3[1])

        if denominator == 0.0:
            return None

        t = numerator / denominator

        if 0.0 <= t and t <= 1.0:
            x = pnt1[0] + (pnt2[0] - pnt1[0]) * t
            m = (pnt2[1] - pnt1[1]) / (pnt2[0] - pnt1[0])
            y = pnt1[1] + (x - pnt1[0]) * m
            return x, y

    @classmethod
    def from_others(cls, others):
        """
        Create a Max2D dataset from many other datasets
        """
        assert isinstance(others, Iterable)
        assert all(isinstance(other, Max2D) for other in others)
        out = cls()
        for other in others:
            out.update(other.x_values, other.y_values)
        return out


class MicroMajorant(Max2D):
    """
    Generates a majorant cross section for a nuclide over a
    provided set of temperatures.

    Parameters
    ----------
    nuclide : str
        Name of the nuclide in GND format
    temperatures : Iterable of float
        List of temperatures over which to compute the majorant

    Attributes
    ----------
    nuclide : str
        Name of the nuclide
    temperatures : Iterable of float
        List of temperatures represented in the majorant
    e_grid : Iterable of float
        Energy values of the pointwise data
    xs : Iterable of float
        Cross section values corresponding to the energy grid
    """
    def __init__(self, nuclide, temperatures):
        super().__init__()
        self._nuclide = nuclide
        self._temperatures = temperatures

        for temperature in temperatures:
                e_grid, xs = calculate_cexs(nuclide, 'nuclide', ('total',), temperature=temperature)
                xs.shape = (xs.size,)
                self.update(e_grid, xs)

    @property
    def nuclide(self):
        return self._nuclide

    @property
    def temperatures(self):
        return self._temperatures

    @property
    def e_grid(self):
        return self._x_values

    @property
    def xs(self):
        return self._y_values


class MaterialMajorant(Max2D):
    """
    Majorant cross section for a material

    Parameters
    ----------
    material : openmc.Material
        Material definition used to generate the majorant
    nuclide_majorants : defaultdict
        Dictionary with nuclide names as keys and MicroMajorant
        instances as values

    Attributes
    ----------
    nuclide_majorants : defaultdict
        Dictionary with nuclide names as keys and MicroMajorant
        instances as values
    e_grid : Iterable of float
        Energy values of the pointwise data
    xs : Iterable of float
        Cross section values corresponding to the energy grid
    """
    def __init__(self, material, nuclide_majorants=None):
        super().__init__()
        cv.check_type('material', material, openmc.Material)
        self._material = material
        self._nuc_majorants = None
        self._e_grid = None

        if nuclide_majorants:
            cv.check_type('nuclide majorants', nuclide_majorants, defaultdict)
            self._nuc_majorants = nuclide_majorants
            self._e_grid = list(nuclide_majorants.values())[0].e_grid

    @property
    def material(self):
        return self._material

    @property
    def nuclide_majorants(self):
        return self._nuc_majorants

    @nuclide_majorants.setter
    def nuclide_majorants(self, new_majorants):
        cv.check_type('new_majorants', new_majorants, defaultdict)
        self._nuc_majorants = new_majorants
        self._e_grid = list(new_majorants.values())[0].e_grid

    @property
    def e_grid(self):
        return self._e_grid

    def xs(self, e_grid):
        """
        Compute the cross section value of the majorant xs for
        the material at this energy
        """
        barns_to_cm_sq = 10e-24

        awr_inv = 1.0 / self.material.average_molar_mass # mol / g

        av = openmc.data.AVOGADRO

        density = self.material.density

        atom_density = awr_inv * av * density * barns_to_cm_sq

        xs_out = np.zeros_like(e_grid)

        for nuclide, percent, _percent_type in self.material.nuclides:
            xs_out += percent * atom_density * self.nuclide_majorants[nuclide].y_values

        return xs_out

class Majorant(Max2D):

    def calculate_xs(self, e):
        # determine energy values to interpolate between
        idx = binary_search(self.x_values, e)

        # calculate interpolation factor
        f = e - self.x_values[idx]
        f /= self.x_values[idx + 1] - self.x_values[idx]

        xs = f * self.y_values[idx] + (1 - f) * self.y_values[idx + 1]

        return xs

    @classmethod
    def from_others(cls, energy_grid, other_majorants):
        # majorant = Majorant.from_others(cross_sections)
        majorant = cls()
        for other in other_majorants:
            majorant.update(energy_grid, other.xs(energy_grid))

        return majorant
