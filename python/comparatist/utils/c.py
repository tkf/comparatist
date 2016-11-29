import os

import numpy

libdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      os.path.pardir, os.path.pardir, os.path.pardir,
                      'lib')


def load_library(name):
    return numpy.ctypeslib.load_library(name, libdir)
