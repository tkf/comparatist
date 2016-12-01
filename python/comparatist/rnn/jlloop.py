from ..utils.jl import jlprepare
from ._helper import init, params


def prepare(name):
    kwds = init(**params[name])
    return jlprepare("Comparatist.Simulators.rnn.loop", name, m=kwds["m"].T)
