from collections import defaultdict
import numpy as np
import sys

from sympy import parse_expr
from sympy.abc import x
from sympy.parsing.sympy_parser import standard_transformations

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, \
    QLineEdit, QMessageBox, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
import matplotlib.pyplot as plt

from golden_section import golden_section_method


class Window(QDialog):
    def __init__(self, parent=None):

        super(Window, self).__init__(parent)
        self.setWindowTitle('Метод золотого сечения')
        self.resize(950, 770)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button_show = QPushButton('Показать', self)
        self.button_show.clicked.connect(self.process_show_button)

        self.button_prev = QPushButton('<-', self)
        self.button_prev.move(730, 40)
        self.button_prev.clicked.connect(self.show_prev_iteration)

        self.button_next = QPushButton('->', self)
        self.button_next.move(830, 40)
        self.button_next.clicked.connect(self.show_next_iteration)

        self.textbox = QLineEdit(self)
        func = QLabel('Function: ')

        self.textbox_a = QLineEdit(self)
        a = QLabel('Left border: ')

        self.textbox_b = QLineEdit(self)
        b = QLabel('Right border: ')

        self.textbox_eps = QLineEdit(self)
        eps = QLabel('Accuracy: ')

        layout = QVBoxLayout()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        layout.addWidget(self.button_show)

        layout.addWidget(func)
        layout.addWidget(self.textbox)

        layout.addWidget(a)
        layout.addWidget(self.textbox_a)

        layout.addWidget(b)
        layout.addWidget(self.textbox_b)

        layout.addWidget(eps)
        layout.addWidget(self.textbox_eps)

        self.setLayout(layout)

        self.params = {'is_good_data': False,
                       'a': 0,
                       'b': 0,
                       'eps': 0.1,
                       'function': False,
                       'iteration': 0,
                       'total_iterations': 0,
                       'data': defaultdict()}

    def func(self, symb, num):
        return symb.subs(x, num)

    def is_digit(self, expr):
        return str(expr).lstrip("-").replace(".", "", 1).isdigit()

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot()

        expr = self.params['function']
        iteration = self.params['iteration']
        points = self.params['data'][iteration]
        answer = self.params['data']['answer']

        t = np.linspace(self.params['a'], self.params['b'], 100)

        # график функции
        ax.plot(t, [self.func(expr, i) for i in t], '-')

        # точки метода a, c, d, b
        for point in points:
            ax.plot(point, self.func(expr, point), '*', color='red')

        # ответ метода
        ax.plot(answer, self.func(expr, answer), '*', color='blue')

        ax.set_title('Итерация: ' + str(self.params['iteration']) +
                     ', x* = ' + str(round(answer, 6)))
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')

        self.canvas.draw()

    def parse(self, expression, check_num):
        try:
            expr = parse_expr(expression,
                              transformations=standard_transformations)
            if self.is_digit(expr.subs(x, check_num)):
                return expr
            return False
        except Exception:
            return False

    def check_input(self):

        function = self.textbox.text()
        a = self.textbox_a.text()
        b = self.textbox_b.text()
        eps = self.textbox_eps.text()

        if self.is_digit(a) and self.is_digit(b) and \
                self.is_digit(eps) and function:
            expr = self.parse(function, float(a))
            if expr:
                return expr, float(a), float(b), float(eps)
        return False

    def update_params(self, input_data):
        expr, a, b, eps = input_data

        self.params['function'] = expr
        self.params['a'] = a
        self.params['b'] = b
        self.params['eps'] = eps
        self.params['is_good_data'] = True
        self.params['iteration'] = 0

        data, total = golden_section_method(expr, a, b, eps)
        self.params['data'] = data
        self.params['total_iterations'] = total

    def process_show_button(self):
        input_data = self.check_input()

        if input_data:
            self.update_params(input_data)
            self.plot()
        else:
            self.params['is_good_data'] = False
            self.figure.clear()
            QMessageBox.question(self, 'Ошибка', 'Введены некорректные данные',
                                 QMessageBox.Ok, QMessageBox.Ok)

    def show_next_iteration(self):
        if self.params['is_good_data']:
            if self.params['iteration'] < self.params['total_iterations']:
                self.params['iteration'] += 1
            self.plot()

    def show_prev_iteration(self):
        if self.params['is_good_data']:
            if self.params['iteration'] > 0:
                self.params['iteration'] -= 1
            self.plot()


app = QApplication(sys.argv)

main = Window()
main.show()

sys.exit(app.exec_())
