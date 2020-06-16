import math
from collections import defaultdict

from sympy.abc import x

PHI1 = (math.sqrt(5) - 1) / 2  # 1 / golden_ratio
PHI2 = (3 - math.sqrt(5)) / 2  # 1 / golden_ratio^2


def f(function, num):
    """
    :param function: sympy expression to calculate at the num
    :param num: real number
    :return: function(num)
    """
    return function.subs(x, num)


def golden_section_method(function, left_border, right_border, accuracy):
    """
    :param function: function to be minimized
    :param left_border: left border of the initial uncertainty interval
    :param right_border: right border of the initial uncertainty interval
    :param accuracy: required accuracy of the solution
    :return: 1. dictionary that stores the state at each iteration
                (the boundaries of the uncertainty interval)
                by the key ['iteration number']
                and solution by the key ['answer']
             2. number of iterations
    """
    n_fact = 0
    (a, b) = (min(left_border, right_border), max(left_border, right_border))

    points = defaultdict(list)

    if b - a <= accuracy:
        points[0] = [a, b]
        points['answer'] = a + (b - a) / 2
        return points, n_fact

    c = a + PHI2 * (b - a)
    d = a + PHI1 * (b - a)

    yc = f(function, c)
    yd = f(function, d)

    points[0] = [a, c, d, b]

    while b - a > accuracy:
        n_fact += 1
        if yc < yd:
            b = d
            d = c
            yd = yc
            c = a + PHI2 * (b - a)
            yc = f(function, c)
        else:
            a = c
            c = d
            yc = yd
            d = a + PHI1 * (b - a)
            yd = f(function, d)
        points[n_fact] = [a, c, d, b]

    points['answer'] = a + (b - a) / 2
    return points, n_fact
