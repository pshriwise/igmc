import numpy as np
from matplotlib import pyplot as plt

import openmc

from py_iga.majorant import Majorant
from py_iga.materials import majorants_from_model


def plot_majorant(energy_grid, cross_sections):

    for mat_xs in cross_sections:
        # compute material cross section on the energy grid
        xs = mat_xs.xs(e_grid)
        # only plot values greater than zero
        zero_mask = xs > 0
        plt.plot(e_grid[zero_mask], xs[zero_mask], label=mat_xs.material.name)

    majorant = Majorant.from_others(energy_grid, cross_sections)

    plt.plot(majorant.x_values,
                majorant.y_values,
                label="Majorant",
                linestyle='dashed',
                color='black')

    plt.yscale('log')
    plt.xscale('log')
    plt.legend()
    plt.title("Macroscopic Cross Sections")
    plt.show()


if __name__ == "__main__":
    pin_cell_model = openmc.examples.pwr_assembly()

    e_grid, material_cross_sections = majorants_from_model(pin_cell_model)

    plot_majorant(e_grid, material_cross_sections)
