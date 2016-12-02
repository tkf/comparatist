import ctypes
from ctypes import (POINTER, c_char_p, c_size_t, c_int, c_long, c_ulong,
                    c_double, c_void_p)
from ctypes.util import find_library


class _c_gsl_rng_type(ctypes.Structure):
    _fields_ = [('name', c_char_p),
                ('max', c_long),
                ('min', c_size_t),
                ('__set', c_void_p),
                ('__get', c_void_p),
                ('__get_double', c_void_p),
                ]
_c_gsl_rng_type_p = POINTER(_c_gsl_rng_type)


class _c_gsl_rng(ctypes.Structure):
    _fields_ = [('type', _c_gsl_rng_type_p),
                ('state', c_void_p)]
_c_gsl_rng_p = POINTER(_c_gsl_rng)


class _GSLFuncLoader(object):

    # see: http://code.activestate.com/recipes/576549-gsl-with-python3/
    gslcblas = ctypes.CDLL(find_library('gslcblas'), mode=ctypes.RTLD_GLOBAL)
    gsl = ctypes.CDLL(find_library('gsl'))

    def _load_1(self, name, argtypes=None, restype=None):
        func = getattr(self.gsl, name)
        if argtypes is not None:
            func.argtypes = argtypes
        if restype is not None:
            func.restype = restype
        setattr(self, name, func)
        return func

    def _load(self, name, argtypes=None, restype=None):
        if isinstance(name, str):
            return self._load_1(name, argtypes, restype)
        else:
            try:
                return [self._load_1(n, argtypes, restype) for n in name]
            except TypeError:
                raise ValueError('name=%r should be a string or iterative '
                                 'of string' % name)


func = _GSLFuncLoader()
func._load('gsl_strerror', [c_int], c_char_p)
func._load('gsl_rng_alloc', [_c_gsl_rng_type_p], _c_gsl_rng_p)
func._load('gsl_rng_set', [_c_gsl_rng_p, c_ulong])
func._load('gsl_rng_free', [_c_gsl_rng_p])
func._load('gsl_rng_types_setup',
           restype=c_void_p)  # POINTER(_c_gsl_rng_p)
func._load('gsl_rng_state', [_c_gsl_rng_p], c_void_p)
func._load('gsl_rng_size', [_c_gsl_rng_p], c_size_t)
func._load(['gsl_ran_gaussian',
            'gsl_ran_gaussian_ziggurat',
            'gsl_ran_gaussian_ratio_method'],
           [_c_gsl_rng_p, c_double],
           c_double)


gsl_strerror = func.gsl_strerror


def _get_gsl_rng_type_p_dict():
    """
    Get all ``gsl_rng_type`` as dict which has pointer to each object

    This is equivalent to C code bellow which is from GSL document:

    .. sourcecode:: c

          const gsl_rng_type **t, **t0;
          t0 = gsl_rng_types_setup ();
          for (t = t0; *t != 0; t++)
            {
              printf ("%s\n", (*t)->name);  /* instead, store t to dict */
            }

    """
    t = func.gsl_rng_types_setup()
    dt = ctypes.sizeof(c_void_p)
    dct = {}
    while True:
        a = c_void_p.from_address(t)
        if a.value is None:
            break
        name = c_char_p.from_address(a.value).value
        name = name.decode()  # for Python 3 (bytes to str)
        dct[name] = ctypes.cast(a, _c_gsl_rng_type_p)
        t += dt
    return dct


class gsl_rng(object):
    _gsl_rng_alloc = func.gsl_rng_alloc
    _gsl_rng_set = func.gsl_rng_set
    _gsl_rng_free = func.gsl_rng_free
    _gsl_rng_type_p_dict = _get_gsl_rng_type_p_dict()
    _ctype_ = _c_gsl_rng_p  # for railgun

    def __init__(self, seed=None, name='mt19937'):
        self._gsl_rng_name = name
        self._gsl_rng_type_p = self._gsl_rng_type_p_dict[name]
        self._cdata_ = self._gsl_rng_alloc(self._gsl_rng_type_p)
        # the name '_cdata_' is for railgun
        if seed is not None:
            self.set(seed)

    def __setstate__(self, data):
        (attrs, state) = data
        self.__init__(name=attrs.pop('_gsl_rng_name'))
        self.__dict__.update(attrs)
        self.set_state(state)

    def __getstate__(self):
        attrs = self.__dict__.copy()
        del attrs['_gsl_rng_type_p']
        del attrs['_cdata_']
        return (attrs, self.get_state())

    def __copy__(self):
        clone = self.__class__.__new__(self.__class__)
        clone.__dict__.update(self.__dict__)
        return clone

    def __del__(self):
        self._gsl_rng_free(self._cdata_)

    def set(self, seed):
        self._gsl_rng_set(self._cdata_, seed)

    _gsl_ran_gaussian = {
        '': func.gsl_ran_gaussian,
        'ziggurat': func.gsl_ran_gaussian_ziggurat,
        'ratio_method': func.gsl_ran_gaussian_ratio_method,
        }

    def ran_gaussian(self, sigma=1.0, method=''):
        return self._gsl_ran_gaussian[method](self._cdata_, sigma)

    def get_state(self):
        """
        Return state of the random number generator as a byte string.
        """
        ptr = func.gsl_rng_state(self._cdata_)
        size = func.gsl_rng_size(self._cdata_)
        buf = ctypes.create_string_buffer(size)
        ctypes.memmove(buf, ptr, size)
        return buf.raw

    def set_state(self, state):
        """
        Set state returned by :meth:`get_state`.
        """
        ptr = func.gsl_rng_state(self._cdata_)
        size = func.gsl_rng_size(self._cdata_)
        given_size = len(state)
        # Pass size explicitly, otherwise it will create a buffer with
        # extra NULL terminator in it:
        buf = ctypes.create_string_buffer(state, given_size)
        if given_size != size:
            raise ValueError(
                'Trying to set incompatible length of state.  '
                'Size of the given state is {0} while {1} is required.  '
                .format(given_size, size))
        ctypes.memmove(ptr, buf, size)


def plot_gaussian(method='', sigma=1, show=True):
    import pylab
    rng = gsl_rng()
    pylab.hist(
        [rng.ran_gaussian(method=method, sigma=sigma) for i in range(10000)],
        bins=100, normed=True)
    if show:
        pylab.show()


def print_error_codes():
    for i in range(1000):
        error_message = gsl_strerror(i)
        if error_message != 'unknown error code':
            print('% 4d: "%s"' % (i, error_message))


def main():
    import sys

    cmd2func = dict(
        print_error_codes=print_error_codes,
        plot_gaussian=plot_gaussian,
        )
    if len(sys.argv) == 0:
        print('Please specify command or code to execute\n')
        for name in sorted(cmd2func):
            print(name)
    else:
        (cmd,) = sys.argv[1:]
        if cmd in cmd2func:
            print("Calling function: %s" % cmd)
            cmd2func[cmd]()
        else:
            print("Executing code: %s" % cmd)
            ret = eval(cmd, globals())
            if ret is not None:
                print("Returned %r" % ret)


if __name__ == '__main__':
    main()
