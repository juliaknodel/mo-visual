# import math
from math import ceil, log
import unittest
from sympy.abc import x
from source.golden_section import golden_section_method, PHI1


def get_problem_params():
    """
    :return: 1. function - function to be minimized
             2. left_border - left border of the initial uncertainty interval
             3. right_border - right border of the initial uncertainty interval
             4. accuracy  - required accuracy of the solution
             5. n_exp - theoretical number of iterations
    """
    left_border = -1
    right_border = 1
    accuracy = 0.1
    function = x**2

    # theoretical number of iterations
    n_exp = int(ceil(log(accuracy / (right_border - left_border)) / log(PHI1)))

    return function, left_border, right_border, accuracy, n_exp


class TestGoldenSectionMethod(unittest.TestCase):

    def test_GSM_ChecksIfTheNumOfIterationsEqualsTheoreticalEstimation(self):
        expr, a, b, eps, n_exp = get_problem_params()
        results = golden_section_method(expr, a, b, eps)
        iterations_list, actual_iterations_num = results
        self.assertEqual(actual_iterations_num, n_exp)

    def test_GSM_ChecksIfLenOfFinalUncertaintyIntervalLessThanAccuracy(self):
        expr, a, b, eps, n_exp = get_problem_params()

        results = golden_section_method(expr, a, b, eps)
        iterations_list, actual_iterations_num = results

        last_iter = iterations_list[actual_iterations_num]
        final_interval_length = abs(last_iter[-1] - last_iter[0])
        self.assertEqual(final_interval_length < eps, True)
