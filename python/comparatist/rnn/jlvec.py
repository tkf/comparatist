from ..utils.jl import jlprepare
from ._helper import init, params


def prepare(name):
    kwds = init(**params[name])
    jlrun = jlprepare("Comparatist.Simulators.rnn.vec", name, m=kwds["m"])

    def run():
        jlkwds = jlrun()
        jlkwds["m"] = jlkwds["m"].T
        return jlkwds
    return run
