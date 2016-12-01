import numpy
import pytest

from .. import clib
from .. import vec
from .. import jlloop
from .. import jlvec

modules = [vec, clib, jlloop, jlvec]
tmax = 20


@pytest.mark.parametrize('ma, mb', [(modules[0], m) for m in modules[1:]])
@pytest.mark.parametrize('name', ['default'])
def test_comparison(ma, mb, name):
    ra = ma.prepare(name)()
    rb = mb.prepare(name)()
    numpy.testing.assert_equal(ra['m'], rb['m'])
    numpy.testing.assert_almost_equal(ra['x'][:tmax], rb['x'][:tmax])
