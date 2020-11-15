
from collections import defaultdict
import sys

import numpy as np
from matplotlib import pyplot as plt
import openmc
from openmc.plotter import calculate_cexs

from majorant import Max2D, MicroMajorant, MaterialMajorant

def setup_energy_grid(nuclides):
    """
    Returns an energy grid containing each unique
    energy value in the point-wise data sets of `nuclides`

    nuclides : defaultdict of MicroscopicMajorant instances
    """

    e_grid_out = None

    # get the energy grid for each nuclide
    for nuclide in nuclides.values():
        if e_grid_out is None:
            e_grid_out = nuclide.e_grid
        else:
            e_grid_out = np.unique(np.concatenate((e_grid_out, nuclide.e_grid)))

    return e_grid_out

def majorants_from_model(model):
    """
    Calculate the macroscopic majorant for a set of materials

    model : openmc.Model
    """

    # get all the nuclides and their temperatures

    material_temps = defaultdict(set)

    # get all temperatures set on cells
    for cell in model.geometry.get_all_cells().values():
        if isinstance(cell.fill, openmc.Material):
            material_temps[cell.fill].add(cell.temperature)

    # and all temperatures set on materials
    [material_temps[mat].add(mat.temperature) for mat in model.materials]

    nuclides = defaultdict(set)
    for material in model.materials:
        for name, _, _ in material.nuclides:
            nuclides[name] = material_temps[material]

    default_temperature = 294 # K
    for temps in nuclides.values():
        if None in temps:
            temps.add(default_temperature)
            temps.discard(None)

    # compute majorants for all nuclide temperatures
    nuclide_majorants = defaultdict(MicroMajorant)
    for nuclide, temperatures in nuclides.items():
        print("Computing majorant for {}...".format(nuclide))
        m = MicroMajorant(nuclide, temperatures)
        nuclide_majorants[nuclide] = m
        plt.plot(m.x_values, m.y_values, label=nuclide)

    plt.figure(1)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Microscopic Cross Sections')
    plt.legend()

    # setup the common energy grid
    print("Computing common energy grid...")
    common_e_grid = setup_energy_grid(nuclide_majorants)
    print("Energy grid size: {}".format(common_e_grid.size))
    print("Energy grid min (eV): {}".format(common_e_grid[0]))
    print("Energy grid max (eV): {}".format(common_e_grid[-1]))

    for nuclide_majorant in nuclide_majorants.values():
        print("Evaluating {} on the common energy grid...".format(nuclide_majorant.nuclide))
        nuclide_majorant.update_grid(common_e_grid)

    # calculate the majorant cross section for each material on the common energy grid
    material_majorants = []
    for material in model.materials:
        material_majorants.append(MaterialMajorant(material, nuclide_majorants))

    return common_e_grid, material_majorants

if __name__ == "__main__":
    pin_cell_model = openmc.examples.pwr_assembly()

    e_grid, material_cross_sections = majorants_from_model(pin_cell_model)

    plt.figure(2)

    for mat_xs in material_cross_sections:
        xs = mat_xs.xs(e_grid) # compute material cross section on the energy grid
        zero_mask = xs > 0 # only plot values greater than zero
        plt.plot(e_grid[zero_mask], xs[zero_mask], label=mat_xs.material.name)

    # majorant = Max2D.from_others(material_cross_sections)
    majorant = Max2D()
    for other in material_cross_sections:
        majorant.update(e_grid, other.xs(e_grid))
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
