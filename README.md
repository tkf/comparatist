# Comparing simulators written in Julia, Python and C

Here are some benchmarks of simple simulations I wrote before picking
up a language before some more complex simulations.  These models are
simple but (hopefully) close enough to the ones I would use (typically
dynamical systems).  All implementations are checked to be equivalent
via automated testing, with help of the grate [PyJulia] library.

*Note:* I'm not a numerical computing expert.  Please let me know if I
miss some techniques to make those implementations faster!

[PyJulia]: https://github.com/JuliaPy/pyjulia


## Simulators

Several implementations of the following models are tested.  For the
time-complexity estimate, T is time steps and N is number of units
(dimension of the system).

- *Recurrent neural network (RNN)* [time = O(T N^2)] --
  The bottleneck is dense matrix-vector dot product.

- *Globally coupled map (GCM)* [time = O(T N)] --
  This is a typical dynamical system with mean-field type communication.
  Inner most loop have slightly complex (but simd'able) arithmetics.

- (maybe more to come...)


Implementations can be found in files:

- `julia/Comparatist/src/<model>/<implementation>.jl`
- `python/comparatist/<model>/<implementation>.py`
- `lib/libcomparatist_<model>.c`


Type of implementation:

- `vec` -- Vector-based.  Closer to mathematical equations.
- `loop` -- Loop-based.  Verbose, but fast in Julia.
- `clib` -- C implementation in `lib/`, loaded via Python.
- ...etc.


## Result

![Elapsed time (wall time) of each implementation.](https://github.com/tkf/comparatist/raw/data/elapsed.png)

Julia implementations are always the best.  C implementations are also
as good as Julia implementations.  Actually, several compile flags
(see lib/Makefile) have to be added in order to make C implementations
comparable to Julia's.  The fact that plain -O3 option couldn't beat
Julia was surprising.  I'm not sure what else to do for the C
implementations to beat Julia; contributions are welcome :)

(TODO: try icc)

Vector-based implantation in Python for the RNN (`rnn [python] vec`)
beats Julia, but this is probably to be due to the MKL dot-product
function called via numpy.  Indeed, when I use
[Julia build with MKL][conda-julia], Julia implementations are closer
to the best result of Python implementation (see blow); not a huge
improvement, though.

[conda-julia]: https://github.com/tkf/conda-julia/

![Elapsed time (wall time) of each implementation, using Julia build with MKL.](https://github.com/tkf/comparatist/raw/data/elapsed-julia-mkl.png)


## License

MIT (see LICENSE file)
