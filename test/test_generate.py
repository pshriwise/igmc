
from py_iga.particle_gen import Particle, ParticleGenerator

def test_parrticle():

    p = Particle()

    assert p.r == (0.0, 0.0, 0.0)
    assert p.u == (1.0, 0.0, 0.0)

def test_generate():

    gen = ParticleGenerator()

    p = gen()

    assert p.r == (0.0, 0.0, 0.0)
    assert p.u != (1.0, 0.0, 0.0)
