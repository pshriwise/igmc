from numbers import Real

import numpy as np

import openmc

from . import checkvalue as cv


class Geometry:

    def __init__(self):
        # list of OpenMC cells
        self._cells = []

        # mapping of cells to cross-section
        self._xs_map = {}

        # global majorant value
        self._majorant = np.inf

    def locate(self, r, u):
        if not self.cells:
            raise RuntimeError("No cells in the geometry")

        cell_out = None
        for cell in self.cells:
            if r in cell and not cell_out:
                cell_out = cell
            else:
                raise RuntimeError("Geometry Error: point located in more than one cell")

        return cell_out, self._xs_map[cell_out]


    def add_cell(self, cell, total_xs):
        cv.check_type('cell', cell, openmc.Cell)
        cv.check_type('total xs', total_xs, Real)
        self._cells.append(cell)
        self._xs_map[cell] = total_xs
        self.update_majorant()

    @property
    def majorant(self):
        if not self.cells:
            raise RuntimeError("Majorant requested with no cells in the Geometry")
        return self._majorant

    @property
    def cells(self):
        return self._cells

    def update_majorant(self):
        self._majorant = max(self._xs_map.values())



