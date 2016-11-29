import numpy


params = dict(
    default=dict(x0=0.1, dim=1000, steps=100, gain=5.0, seed=1),
)


def init(x0, dim, steps, gain, seed):
    rng = numpy.random.RandomState(seed)
    x = numpy.zeros((steps, dim), dtype=float)
    x[0] = x0
    m = rng.randn(dim, dim) / numpy.sqrt(dim) * gain
    y = numpy.zeros(dim, dtype=float)
    return dict(x=x, m=m, y=y)


def make_prepare(simulate):
    def prepare(name):
        kwds = init(**params[name])

        def run():
            simulate(**kwds)
            return kwds
        return run
    return prepare
