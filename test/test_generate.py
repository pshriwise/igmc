
import numpy as np
from numpy.random import rand
from numpy.testing import assert_array_equal

from py_iga.mixin import reset_auto_ids
from py_iga.particle_gen import Particle, ParticleGenerator

def test_particle():

    p = Particle(id=20)

    assert_array_equal(p.r, (0.0, 0.0, 0.0))
    assert_array_equal(p.u, (1.0, 0.0, 0.0))
    assert p.e == 10.0

    p.r = (5.0, 0.0, 5.0)
    p.u = (0.7071, 0.0, 0.7071)
    p.e = 0.1

    assert p.id == 20
    assert_array_equal(p.r, (5.0, 0.0, 5.0))
    assert_array_equal(p.u, (0.7071, 0.0, 0.7071))
    assert p.e == 0.1


def test_generate():

    gen = ParticleGenerator()

    p = gen()

    assert_array_equal(p.r, (0.0, 0.0, 0.0))
    assert not np.array_equal(p.u, (1.0, 0.0, 0.0))


def test_mixin():
    reset_auto_ids()

    gen = ParticleGenerator()

    n_particles = 10

    for i in range(n_particles):
        p = Particle()
        assert p.id == i + 1

    for i in range(n_particles):
        p = gen()
        assert p.id == n_particles + i + 1

def test_advance():

    p = Particle()

    p.advance(10.0)

    assert not np.array_equal(p.r, (0.0, 0.0, 0.0))


def test_scatter():

    p = Particle()

    e = p.e

    p.scatter()

    assert p.e == 0.5 * e


def test_simulate():

    # create a single particle
    p = Particle()

    majorant_xs = 8.0
    total_xs = 2.0

    while p.e > 1E-03:
        p.advance(majorant_xs)
        if rand() < (total_xs / majorant_xs):
            print("Scattering")
            p.scatter()

    print(p.termination_report())
