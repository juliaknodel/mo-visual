import math
import unittest
from sympy.abc import x
from source.golden_section import golden_section_method, PHI1


def get_problem_params():
    a = -1
    b = 1
    eps = 0.1
    expr = x**2

    # n высчитывается из теории
    n_exp = int(math.ceil(math.log(eps / (b-a)) / math.log(PHI1)))
    return expr, a, b, eps, n_exp


class TestGoldenSectionMethod(unittest.TestCase):
    def test_GSM_GetProblem_ShouldReturnTheoryAndRealIterationsEqual(self):
        expr, a, b, eps, n_exp = get_problem_params()
        results = golden_section_method(expr, a, b, eps)
        iterations_list, actual_iterations_num = results
        self.assertEqual(actual_iterations_num, n_exp)

    def test_GSM_GetProblem_ShouldReturnEndIntervalSizeLessThanAccuracy(self):
        expr, a, b, eps, n_exp = get_problem_params()

        results = golden_section_method(expr, a, b, eps)
        iterations_list, actual_iterations_num = results

        last_iter = iterations_list[actual_iterations_num]
        end_interval_size = abs(last_iter[len(last_iter) - 1] - last_iter[0])
        self.assertEqual(end_interval_size < eps, True)
