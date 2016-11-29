import ctypes
import numpy

from ..utils.c import load_library


double1d = ctypes.POINTER(ctypes.c_double)


class RecurrentNeuralNetwork(ctypes.Structure):
    _fields_ = [
        ("dim", ctypes.c_int),
        ("steps", ctypes.c_int),
        ("m", double1d),
        ("x", double1d),
        ]


class Simulator:

    _lib = load_library('libcomparatist_rnn')
    _run = _lib.RecurrentNeuralNetwork_run
    _run.argtypes = [ctypes.POINTER(RecurrentNeuralNetwork)]

    def __init__(self, x0=0.1, dim=1000, steps=10):
        self.m = numpy.ones((dim, dim), dtype=float) / dim * 0.5
        self.x = numpy.ones((steps, dim), dtype=float)
        self.x[0] = x0

        self.struct = RecurrentNeuralNetwork()
        self.struct.steps = steps
        self.struct.dim = dim
        self.struct.x = self.x.ctypes.data_as(double1d)
        self.struct.m = self.m.ctypes.data_as(double1d)

    def run(self):
        self._run(ctypes.pointer(self.struct))


def prepare(name):
    from ._base import init, params
    kwds = init(**params[name])
    steps, dim = kwds["x"].shape
    sim = Simulator(x0=kwds["x"][0], dim=dim, steps=steps)
    sim.m[:] = kwds["m"]
    return sim.run
