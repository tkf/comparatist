import ctypes
import numpy

from ..utils.gsl import gsl_rng
from ..utils.c import load_library


double1d = ctypes.POINTER(ctypes.c_double)


class OrnsteinUhlenbeckProcess(ctypes.Structure):
    _fields_ = [
        ("steps", ctypes.c_int),
        ("dt", ctypes.c_double),
        ("sigma", ctypes.c_double),
        ("x", double1d),
        ("rng", gsl_rng._ctype_),
        ]


class Simulator:

    _lib = load_library('libcomparatist_oup')
    _run = _lib.OrnsteinUhlenbeckProcess_run
    _run.argtypes = [ctypes.POINTER(OrnsteinUhlenbeckProcess)]

    def __init__(self, x0=0, steps=10000, dt=0.1, sigma=1,
                 seed=None, rng=None):
        self.x = numpy.zeros(steps, dtype=float)
        self.x[0] = x0
        self.rng = rng or gsl_rng(seed)

        self.struct = OrnsteinUhlenbeckProcess()
        self.struct.steps = steps
        self.struct.dt = dt
        self.struct.sigma = sigma
        self.struct.x = self.x.ctypes.data_as(double1d)
        self.struct.rng = self.rng._cdata_

    def run(self):
        self._run(ctypes.pointer(self.struct))


def prepare(name):
    from ._helper import init, params
    kwds = init(**params[name])
    steps, = kwds["x"].shape
    sim = Simulator(x0=kwds["x"][0], steps=steps,
                    **{k: kwds[k] for k in ['dt', 'sigma', 'seed']})
    kwds["x"] = sim.x

    def run():
        sim.run()
        return kwds
    return run
