import glob
import json

import pandas


def loadjson(paths):
    if isinstance(paths, str):
        paths = glob.glob(paths)
    for p in paths:
        with open(p) as file:
            result = json.load(file)
        yield dict(result, path=p)


def load(paths):
    table = []
    for data in loadjson(paths):
        for row in data['benchmark']:
            table.append(dict(row, path=data['path'], lang=data["lang"]))
    df = pandas.DataFrame(table)
    mod = df["module"].str.extract(r"(?P<model>[^\.]+)\.(?P<impl>.+)",
                                   expand=True)
    df["sim"] = mod["model"] + " [" + df["lang"] + "] " + mod["impl"]
    return df


def elapsed(paths):
    from . import chart
    return chart.elapsed(load(paths))
