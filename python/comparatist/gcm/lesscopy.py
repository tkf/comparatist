import numpy

from ._helper import make_prepare


def simulate(x, f, r, epsilon):
    y = numpy.zeros_like(x[0])
    for i in range(1, len(x)):
        y[:] = x[i-1]
        y *= (1 - epsilon)
        y += epsilon * x[i-1].mean()

        # r * y * (1 - y)
        x[i] = y
        y -= 1
        x[i] *= -r
        x[i] *= y
    return x


prepare = make_prepare(simulate)
