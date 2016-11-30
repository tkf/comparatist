from ._helper import make_prepare


def simulate(x, f, r, epsilon):
    for i in range(1, len(x)):
        x[i] = f((1 - epsilon) * x[i-1] + epsilon * x[i-1].mean(), r)
    return x


prepare = make_prepare(simulate)
