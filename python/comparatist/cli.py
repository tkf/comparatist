from __future__ import print_function

import json
import itertools


def run_funcs(module_names, run_names, repeat):
    from .utils.importer import import_object
    from .utils.timing import gettimings

    for i in range(repeat):
        for m, r in itertools.product(module_names, run_names):
            func = import_object('.' + m, __name__).prepare(r)
            pre = gettimings()
            func()
            post = gettimings()
            yield dict(module=m, run=r, pre=pre, post=post)


def cli_run(output, **kwds):
    """
    Run benchmarks.
    """
    benchmark = list(run_funcs(**kwds))
    try:
        json.dump(dict(benchmark=benchmark), output)
    finally:
        output.close()


def make_parser(doc=__doc__):
    import argparse

    class FormatterClass(argparse.RawDescriptionHelpFormatter,
                         argparse.ArgumentDefaultsHelpFormatter):
        pass

    parser = argparse.ArgumentParser(
        formatter_class=FormatterClass,
        description=doc)
    subparsers = parser.add_subparsers()

    def subp(command, func):
        doc = func.__doc__
        title = None
        for title in filter(None, map(str.strip, (doc or '').splitlines())):
            break
        p = subparsers.add_parser(
            command,
            formatter_class=FormatterClass,
            help=title,
            description=doc)
        p.set_defaults(func=func)
        return p

    def csv(x):
        return x.split(',')

    p = subp('run', cli_run)
    p.add_argument('module_names', type=csv)
    p.add_argument('run_names', type=csv, nargs='?', default='default')
    p.add_argument('--output', default='-', type=argparse.FileType('w'))
    p.add_argument('--repeat', type=int, default=5)

    return parser


def main(args=None):
    parser = make_parser()
    ns = parser.parse_args(args)
    return (lambda func, **kwds: func(**kwds))(**vars(ns))


if __name__ == '__main__':
    main()
