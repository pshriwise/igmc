import numpy as np
from numpy.random import rand

import openmc
from openmc.plotter import calculate_cexs

from py_iga import ParticleGenerator
from py_iga import majorant_from_geometry, CEXS


def simulate():

    ## Temporary Parameter Storage ##
    n_particles = 10000
    e_min = 1E-03
    majorant_xs = 10
    total_xs = 9.9
    seed = 110

    np.random.seed(seed)

    particle_generator = ParticleGenerator()

    # materials
    uo2 = openmc.Material(name='UO2 fuel at 2.4% wt enrichment')
    uo2.set_density('g/cm3', 10.29769)
    uo2.add_element('U', 1., enrichment=2.4)
    uo2.add_element('O', 2.)

    zircaloy = openmc.Material(name='Zircaloy 4')
    zircaloy.set_density('g/cm3', 6.55)
    zircaloy.add_element('Sn', 0.014  , 'wo')
    zircaloy.add_element('Fe', 0.00165, 'wo')
    zircaloy.add_element('Cr', 0.001  , 'wo')
    zircaloy.add_element('Zr', 0.98335, 'wo')

    borated_water = openmc.Material(name='Borated water')
    borated_water.set_density('g/cm3', 0.740582)
    borated_water.add_element('B', 4.0e-5)
    borated_water.add_element('H', 5.0e-2)
    borated_water.add_element('O', 2.4e-2)

    # simple pincell geometry
    fuel_cyl = openmc.ZCylinder(r=1.5)
    clad_cyl = openmc.ZCylinder(r=1.7)

    fuel_cell = openmc.Cell(region=-fuel_cyl, fill=uo2)
    clad_cell = openmc.Cell(region=+fuel_cyl & -clad_cyl, fill=zircaloy)
    water_cell = openmc.Cell(region=+clad_cyl, fill=borated_water)

    geom = openmc.Geometry([fuel_cell, clad_cell, water_cell])

    print("Computing material cross-sections...")
    xs_dict = {}
    for material in geom.get_all_materials().values():
        e_grid, xs = calculate_cexs(material, 'material', ('total',))
        xs_dict[material] = CEXS(e_grid, xs[0])

    print("Computing majorant cross-section...")
    majorant = majorant_from_geometry(geom)

    # transport loop
    for _ in range(n_particles):
        p = particle_generator()
        while p.e > e_min:
            maj_xs = majorant.calculate_xs(p.e)
            p.advance(maj_xs)
            p.locate(geom)
            p.calculate_xs(xs_dict)

            if not p.cell:
                break

            if p.xs > maj_xs:
                raise RuntimeError("Total XS value {} b is greater than the "
                                   "majorant value ({} b).".format(p.xs, maj_xs))

            if rand() < p.xs / maj_xs:
                p.scatter()

        print(p)

if __name__ == "__main__":
    simulate()
