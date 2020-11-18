import numpy as np
from numpy.random import rand


def isotropic_dir():
    """
    Generates an isotropic distribution of
    random unit vectors.

    Returns
    -------
    NumPy array of 3 floats

    """
    phi = rand() * 2.0 * np.pi
    t = -1.0 + 2.0 * rand()

    u = np.sqrt(1 - t*t) * np.cos(phi)
    v = np.sqrt(1 - t*t) * np.sin(phi)
    w = t

    return (u, v, w)
