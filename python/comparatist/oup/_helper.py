import numpy

params = dict(
    default=dict(x0=0, steps=1000000, dt=0.1, sigma=1, seed=1),
)


def init(steps, **kwds):
    return dict(x=numpy.zeros(steps, dtype=float), **kwds)
