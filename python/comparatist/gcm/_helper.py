import numpy


params = dict(
    default=dict(x0=0.1, dim=1000, steps=10000,
                 r=4.0, epsilon=0.1, map='logistic'),
)

mapdb = dict(
    logistic=lambda x, r: r * x * (1 - x),
)


def init(x0, dim, steps, map, **kwds):
    x = numpy.zeros((steps, dim), dtype=float)
    x[0] = x0
    return dict(x=x, f=mapdb[map], **kwds)


def make_prepare(simulate):
    def prepare(name):
        kwds = init(**params[name])

        def run():
            simulate(**kwds)
            return kwds
        return run
    return prepare
