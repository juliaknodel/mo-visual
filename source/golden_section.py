import math
from collections import defaultdict

from sympy.abc import x

PHI1 = (math.sqrt(5) - 1) / 2  # 1 / phi
PHI2 = (3 - math.sqrt(5)) / 2  # 1 / phi^2


def f(symb, num):
    return symb.subs(x, num)


def golden_section_method(sym, a, b, eps):
    n_fact = 0
    (a, b) = (min(a, b), max(a, b))

    points = defaultdict(list)

    if b - a <= eps:
        points[0] = [a, b]
        points['answer'] = a + (b - a) / 2
        return points, n_fact

    c = a + PHI2 * (b - a)
    d = a + PHI1 * (b - a)

    yc = f(sym, c)
    yd = f(sym, d)

    points[0] = [a, c, d, b]

    while b - a > eps:
        n_fact += 1
        if yc < yd:
            b = d
            d = c
            yd = yc
            c = a + PHI2 * (b - a)
            yc = f(sym, c)
        else:
            a = c
            c = d
            yc = yd
            d = a + PHI1 * (b - a)
            yd = f(sym, d)
        points[n_fact] = [a, c, d, b]

    points['answer'] = a + (b - a) / 2
    return points, n_fact
