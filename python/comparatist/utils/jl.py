import os

import numpy
import julia


jlbase = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      os.path.pardir, os.path.pardir, os.path.pardir,
                      'julia')
os.environ['JULIA_LOAD_PATH'] = jlbase + (
    ':' + os.environ['JULIA_LOAD_PATH']
    if 'JULIA_LOAD_PATH' in os.environ
    else ''
)

JL = None


def getjulia():
    global JL
    if not JL:
        JL = julia.Julia()
    return JL


def jlprepare(module, name, **kwds):
    jl = getjulia()
    jlrun = jl.eval("""
    import {module}
    function(; opts...)
        {module}.prepare(:{name}; opts...)
    end
    """.format(module=module, name=name))(**kwds)

    def run():
        kwds = jlrun()
        for k, v in kwds.items():
            if isinstance(v, numpy.ndarray):
                kwds[k] = v.T
        return kwds
    return run


def make_prepare(module, **kwds):
    return lambda name: jlprepare(module, name, **kwds)
