import numpy

from ._helper import make_prepare


def simulate(x, m, y):
    for i in range(1, len(x)):
        numpy.dot(m, x[i-1], out=y)
        numpy.tanh(y, out=x[i])
    return x, m


prepare = make_prepare(simulate)
