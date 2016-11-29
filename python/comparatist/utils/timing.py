import datetime
try:
    import resource
except ImportError:
    resource = None

_utc_zero = datetime.datetime.utcfromtimestamp(0)


def unixtimenow():
    """
    Return current Unix time as a float.

    Unix time (aka POSIX time or Epoch time) is defined as:

      the number of seconds that have elapsed since 00:00:00
      Coordinated Universal Time (UTC), Thursday, 1 January 1970, not
      counting leap seconds

      --- https://en.wikipedia.org/wiki/Unix_time

    """
    return (datetime.datetime.utcnow() - _utc_zero).total_seconds()


def _getrusage_self():
    """
    See: getrusage(2)
    """
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    return {k: getattr(rusage, k) for k in dir(rusage) if k.startswith('ru_')}

if resource is None:
    def getrusage_self():
        return {}
else:
    getrusage_self = _getrusage_self


def gettimings():
    return dict(
        unixtime=unixtimenow(),
        rusage=getrusage_self(),
    )
