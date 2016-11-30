import os

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


def prepare(name):
    jl = getjulia()
    jlrun = jl.eval("""
    using Comparatist.Simulators.gcm.loop
    Comparatist.Simulators.gcm.loop.prepare(:{0})
    """.format(name))

    def run():
        kwds = jlrun()
        kwds['x'] = kwds['x'].T
        return kwds
    return run
