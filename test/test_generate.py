
import numpy as np
from numpy.testing import assert_array_equal

from py_iga.particle_gen import Particle, ParticleGenerator


def test_parrticle():

    p = Particle()

    assert_array_equal(p.r, (0.0, 0.0, 0.0))
    assert_array_equal(p.u, (1.0, 0.0, 0.0))
    assert p.e == 10.0

    p.r = (5.0, 0.0, 5.0)
    p.u = (0.7071, 0.0, 0.7071)
    p.e = 0.1

    assert_array_equal(p.r, (5.0, 0.0, 5.0))
    assert_array_equal(p.u, (0.7071, 0.0, 0.7071))
    assert p.e == 0.1


def test_generate():

    gen = ParticleGenerator()

    p = gen()

    assert_array_equal(p.r, (0.0, 0.0, 0.0))
    assert not np.array_equal(p.u, (1.0, 0.0, 0.0))
