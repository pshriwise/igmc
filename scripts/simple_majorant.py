from matplotlib import pyplot as plt

from py_iga.majorant import Max2D

if __name__ == "__main__":
    e_1 = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
    xs_1 = (1.0, 1.0, 3.0, 3.0, 1.0, 3.0, 3.0)

    e_2 = (1.25, 1.5, 1.75, 2.75, 2.9, 3.5, 4.0, 5.5, 6.5, 7.0)
    xs_2 = (0.0, 0.0, 2.0, 2.0, 4.0, 4.0, 2.0, 2.0, 2.0, 3.0)

    majorant = Max2D()
    majorant.update(e_1, xs_1)
    majorant.update(e_2, xs_2)

    plt.plot(e_1, xs_1, marker='.')
    plt.plot(e_2, xs_2, marker='.')
    plt.show() # plot xs's only
    plt.plot(e_1, xs_1, marker='.')
    plt.plot(e_2, xs_2, marker='.')
    plt.plot(majorant.x_values, majorant.y_values, marker='.')
    plt.show() # plot w/ majorant
