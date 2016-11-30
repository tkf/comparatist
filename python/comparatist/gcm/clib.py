import ctypes
import numpy

from ..utils.c import load_library


double1d = ctypes.POINTER(ctypes.c_double)


class GloballyCoupledMap(ctypes.Structure):
    _fields_ = [
        ("dim", ctypes.c_int),
        ("steps", ctypes.c_int),
        ("r", ctypes.c_double),
        ("epsilon", ctypes.c_double),
        ("x", double1d),
        ]


class Simulator:

    _lib = load_library('libcomparatist_gcm')

    def __init__(self, x0, r, epsilon, dim, steps, map='logistic'):
        self.x = numpy.ones((steps, dim), dtype=float)
        self.x[0] = x0

        self._run = getattr(self._lib, 'GloballyCoupledMap_' + map)
        self._run.argtypes = [ctypes.POINTER(GloballyCoupledMap)]

        self.struct = GloballyCoupledMap()
        self.struct.steps = steps
        self.struct.dim = dim
        self.struct.r = r
        self.struct.epsilon = epsilon
        self.struct.x = self.x.ctypes.data_as(double1d)

    def run(self):
        self._run(ctypes.pointer(self.struct))


def prepare(name):
    from ._helper import init, params
    kwds = init(**params[name])
    steps, dim = kwds["x"].shape
    sim = Simulator(x0=kwds["x"][0], dim=dim, steps=steps,
                    r=kwds['r'], epsilon=kwds['epsilon'])
    kwds["x"] = sim.x

    def run():
        sim.run()
        return kwds
    return run
