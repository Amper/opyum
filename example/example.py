from math import pi, e, sqrt
C_M = (- 2)
C_S = 1 / 2

def gaussians(xs):
    c1 = (1 / C_S * sqrt(2 * pi))
    c2 =  - ((1.0 / 2.0) / (C_S ** 2))
    for x in ((c1 * (e ** (c2 * ((x - C_M) ** 2)))) for x in xs):
        yield x
for (x, y) in enumerate(gaussians(range(10))):
    print(('g({})' + ' = ' + '{}').format(x, y))