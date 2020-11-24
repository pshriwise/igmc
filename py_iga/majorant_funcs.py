from collections import defaultdict
import sys

import numpy as np
import openmc
from openmc.plotter import calculate_cexs

from .majorant import Majorant, MicroMajorant, MaterialMajorant

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
    Calculate the macroscopic majorant from materials on an OpenMC model

    model : openmc.Model instance
    """
    return majorants_from_geometry(model.geometry)

def majorants_from_geometry(geom):
    """
    Calculate the macroscopic majorant for a set of materials

    geom : openmc.Geometry instance
    """

    # get all the nuclides and their temperatures

    material_temps = defaultdict(set)

    # get all temperatures set on cells
    for cell in geom.get_all_cells().values():
        if isinstance(cell.fill, openmc.Material):
            material_temps[cell.fill].add(cell.temperature)

    materials = list(geom.get_all_materials().values())

    # and all temperatures set on materials
    [material_temps[mat].add(mat.temperature) for mat in materials]

    nuclides = defaultdict(set)
    for material in materials:
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
    for material in materials:
        material_majorants.append(MaterialMajorant(material, nuclide_majorants))

    return common_e_grid, material_majorants

def majorant_from_geometry(geom):
    """
    Compute the majorant for a given geometry

    Parameters
    ----------
    geom : openmc.Geometry
        Geometry for which the majorant is computed

    Returns
    -------
        Instance of `Majorant` for the geometry.
    """
    e_grid, mat_majorants = majorants_from_geometry(geom)
    return Majorant.from_others(e_grid, mat_majorants)
