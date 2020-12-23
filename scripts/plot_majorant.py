import numpy as np
from matplotlib import pyplot as plt

import openmc

from igmc import plot_majorant, majorants_from_model

if __name__ == "__main__":
    pin_cell_model = openmc.examples.pwr_assembly()

    e_grid, material_cross_sections = majorants_from_model(pin_cell_model)

    plot_majorant(e_grid, material_cross_sections)
