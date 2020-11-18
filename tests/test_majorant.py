
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

from py_iga.majorant import Max2D


def test_majorant():

    e_1 = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
    xs_1 = (1.0, 1.0, 3.0, 3.0, 1.0, 3.0, 3.0)

    majorant = Max2D()

    majorant.update(e_1, xs_1)

    assert_array_equal(e_1, majorant.x_values)
    assert_array_equal(xs_1, majorant.y_values)

    e_2 = (1.25, 1.5, 1.75, 2.75, 2.9, 3.5, 4.0, 5.5, 6.5, 7.0)
    xs_2 = (0.0, 0.0, 2.0, 2.0, 4.0, 4.0, 2.0, 2.0, 2.0, 3.0)

    majorant.update(e_2, xs_2)

    exp_majorant_e_grid = (1.0, 1.625, 1.75, 2.5, 2.794118,
                           2.9, 3.5, 3.75, 4.0, 4.5, 5.5,
                           6.0, 7.0, 7.0)
    exp_majorant_xs = (1.0, 1.0, 2.0, 2.0, 2.588235,
                       4.0, 4.0, 3.0, 3.0, 2.0,
                       2.0, 3.0, 3.0, 3.0)

    assert_array_almost_equal(exp_majorant_e_grid, majorant.x_values)
    assert_array_almost_equal(exp_majorant_xs, majorant.y_values)
