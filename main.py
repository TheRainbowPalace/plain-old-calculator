#!/usr/bin/env python

"""
Author: Jakob Rieke
"""


import sys
import parser
from calc_math import *
from observable import Observable
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, \
    QLayout, QLabel, QVBoxLayout, QTextEdit


class App:
    def __init__(self):
        self.title = Observable("Calculator")
        self.empty_formula = '0'
        self.formula = Observable(self.empty_formula)
        self.result = Observable("")
        self.history = []
        self.history_position = -1
        self.max_history_length = 100


def append(app, value):
    if app.formula.value == '0':
        app.formula.set(str(value))
    else:
        app.formula.set(app.formula.value + value)

    app.history_position = -1


def clear(app):
    app.formula.set(app.empty_formula)


def clear_history(app):
    app.history.clear()
    app.history_position = -1
    app.result.set('')


def clear_history_position(app):
    pass


def select_previous(app):
    print(app.history)
    print()
    if len(app.history) == 0:
        return
    app.history_position = (app.history_position + 1) % len(app.history)
    print(app.history_position)
    app.formula.set(app.history[app.history_position])


def select_next(app):
    if len(app.history) == 0:
        return
    pos = (app.history_position - 1)
    if pos < 0:
        pos = len(app.history) - 1

    app.history_position = pos
    app.formula.set(app.history[pos])


def evaluate(app):
    try:
        result = eval(parser.expr(app.formula.value).compile())
        app.result.set('<i>' + app.formula.value + '</i> = ' + str(result))
        clear(app)
    except TypeError as e:
        app.result.set(str(e))
    except SyntaxError:
        app.result.set("Invalid syntax")

    # Add evaluated formula to history
    app.history.append(app.formula.value)
    if len(app.history) > app.max_history_length:
        app.history = app.history[1:]


def setup_buttons(grid, app):
    toggle_mode_btn = QPushButton("2^nd")
    grid.addWidget(toggle_mode_btn, 1, 0, 1, 1)

    rand_btn = QPushButton("Rand")
    grid.addWidget(rand_btn, 4, 5, 1, 1)
    rand_btn.clicked.connect(lambda: append(app, "rand()"))

    bracket_close_btn = QPushButton(")")
    grid.addWidget(bracket_close_btn, 0, 1, 1, 1)
    bracket_close_btn.clicked.connect(lambda: append(app, ")"))

    bracket_open_btn = QPushButton("(")
    grid.addWidget(bracket_open_btn, 0, 0, 1, 1)
    bracket_open_btn.clicked.connect(lambda: append(app, "("))

    pushButton_44 = QPushButton("EE")
    grid.addWidget(pushButton_44, 3, 5, 1, 1)

    # Setup constants
    e_button = QPushButton("e")
    grid.addWidget(e_button, 3, 4, 1, 1)
    e_button.clicked.connect(lambda: append(app, "e"))

    pi_btn = QPushButton("π")
    grid.addWidget(pi_btn, 4, 4, 1, 1)
    pi_btn.clicked.connect(lambda: append(app, "pi"))

    faculty_btn = QPushButton("n!")
    grid.addWidget(faculty_btn, 3, 0, 1, 1)
    faculty_btn.clicked.connect(lambda: append(app, "factorial("))

    push_button_27 = QPushButton("1/x")
    grid.addWidget(push_button_27, 2, 0, 1, 1)
    push_button_27.clicked.connect(lambda: append(app, "1/"))

    # Setup exponential functions
    exp_btn = QPushButton("e^x")
    grid.addWidget(exp_btn, 1, 4, 1, 1)
    exp_btn.clicked.connect(lambda: append(app, "exp("))

    push_button_14 = QPushButton("10^x")
    grid.addWidget(push_button_14, 1, 5, 1, 1)
    push_button_14.clicked.connect(lambda: append(app, "10**"))

    pushButton_18 = QPushButton("x^2")
    grid.addWidget(pushButton_18, 1, 1, 1, 1)
    pushButton_18.clicked.connect(lambda: append(app, "**2"))

    pushButton_17 = QPushButton("x^3")
    grid.addWidget(pushButton_17, 1, 2, 1, 1)
    pushButton_17.clicked.connect(lambda: append(app, "**3"))

    power_btn = QPushButton("x^y")
    grid.addWidget(power_btn, 1, 3, 1, 1)
    power_btn.clicked.connect(lambda: append(app, "**"))

    # Setup memory functionality
    mem_clear_btn = QPushButton("mc")
    grid.addWidget(mem_clear_btn, 0, 2, 1, 1)
    mem_clear_btn.clicked.connect(lambda: clear_history(app))

    previous_btn = QPushButton("pre")
    grid.addWidget(previous_btn, 0, 3, 1, 1)
    previous_btn.clicked.connect(lambda: select_previous(app))

    next_btn = QPushButton("next")
    grid.addWidget(next_btn, 0, 4, 1, 1)
    next_btn.clicked.connect(lambda: select_next(app))

    mem_remove_btn = QPushButton("mr")
    grid.addWidget(mem_remove_btn, 0, 5, 1, 1)
    mem_remove_btn.clicked.connect(lambda: clear_history_position(app))

    # Setup trigonometric functions
    cos_btn = QPushButton("cos")
    grid.addWidget(cos_btn, 3, 2, 1, 1)
    cos_btn.clicked.connect(lambda: append(app, "cos("))

    cosh_btn = QPushButton("cosh")
    grid.addWidget(cosh_btn, 4, 2, 1, 1)
    cosh_btn.clicked.connect(lambda: append(app, "cosh("))

    sin_btn = QPushButton("sin")
    grid.addWidget(sin_btn, 3, 1, 1, 1)
    sin_btn.clicked.connect(lambda: append(app, "sin("))

    sinh_btn = QPushButton("sinh")
    grid.addWidget(sinh_btn, 4, 1, 1, 1)
    sinh_btn.clicked.connect(lambda: append(app, "sinh("))

    tan_btn = QPushButton("tan")
    grid.addWidget(tan_btn, 3, 3, 1, 1)
    tan_btn.clicked.connect(lambda: append(app, "tan("))

    tanh_btn = QPushButton("tanh")
    grid.addWidget(tanh_btn, 4, 3, 1, 1)
    tanh_btn.clicked.connect(lambda: append(app, "tanh("))

    deg_btn = QPushButton("deg")
    grid.addWidget(deg_btn, 4, 0, 1, 1)
    deg_btn.clicked.connect(lambda: append(app, "deg("))

    # Setup logarithmic functions
    log10_btn = QPushButton("log10")
    grid.addWidget(log10_btn, 2, 5, 1, 1)
    log10_btn.clicked.connect(lambda: append(app, "log10("))

    ln_btn = QPushButton("ln")
    grid.addWidget(ln_btn, 2, 4, 1, 1)
    ln_btn.clicked.connect(lambda: append(app, "ln("))

    # Setup sqrt functions
    sqrt_btn = QPushButton("sqrt")
    grid.addWidget(sqrt_btn, 2, 3, 1, 1)
    sqrt_btn.clicked.connect(lambda: append(app, "sqrt(x, "))

    sqrt2_btn = QPushButton("sqrt2")
    grid.addWidget(sqrt2_btn, 2, 1, 1, 1)
    sqrt2_btn.clicked.connect(lambda: append(app, "sqrt2("))

    sqrt3_btn = QPushButton("sqrt3")
    grid.addWidget(sqrt3_btn, 2, 2, 1, 1)
    sqrt3_btn.clicked.connect(lambda: append(app, "sqrt3("))


def setup_number_buttons(grid, app):
    number0_btn = QPushButton("0")
    grid.addWidget(number0_btn, 4, 6, 1, 2)
    number0_btn.clicked.connect(lambda: append(app, "0"))

    number1_btn = QPushButton("1")
    grid.addWidget(number1_btn, 3, 6, 1, 1)
    number1_btn.clicked.connect(lambda: append(app, "1"))

    number2_btn = QPushButton("2")
    grid.addWidget(number2_btn, 3, 7, 1, 1)
    number2_btn.clicked.connect(lambda: append(app, "2"))

    number3_btn = QPushButton("3")
    grid.addWidget(number3_btn, 3, 8, 1, 1)
    number3_btn.clicked.connect(lambda: append(app, "3"))

    number4_btn = QPushButton("4")
    grid.addWidget(number4_btn, 2, 6, 1, 1)
    number4_btn.clicked.connect(lambda: append(app, "4"))

    number5_btn = QPushButton("5")
    grid.addWidget(number5_btn, 2, 7, 1, 1)
    number5_btn.clicked.connect(lambda: append(app, "5"))

    number6_btn = QPushButton("6")
    grid.addWidget(number6_btn, 2, 8, 1, 1)
    number6_btn.clicked.connect(lambda: append(app, "6"))

    number7_btn = QPushButton("7")
    grid.addWidget(number7_btn, 1, 6, 1, 1)
    number7_btn.clicked.connect(lambda: append(app, "7"))

    number8_btn = QPushButton("8")
    grid.addWidget(number8_btn, 1, 7, 1, 1)
    number8_btn.clicked.connect(lambda: append(app, "8"))

    number9_btn = QPushButton("9")
    grid.addWidget(number9_btn, 1, 8, 1, 1)
    number9_btn.clicked.connect(lambda: append(app, "9"))


def setup_basic_buttons(grid, app):
    ac_btn = QPushButton("AC")
    grid.addWidget(ac_btn, 0, 6, 1, 1)
    ac_btn.clicked.connect(lambda: clear(app))

    sign_btn = QPushButton("Br")
    grid.addWidget(sign_btn, 0, 7, 1, 1)
    sign_btn.clicked.connect(lambda: app.formula.set(app.formula.value[:-1]))

    percent_btn = QPushButton("mod")
    grid.addWidget(percent_btn, 0, 8, 1, 1)
    percent_btn.clicked.connect(lambda: append(app, "%"))

    divide_btn = QPushButton("/")
    grid.addWidget(divide_btn, 0, 9, 1, 1)
    divide_btn.clicked.connect(lambda: append(app, "/"))

    multiply_btn = QPushButton("*")
    grid.addWidget(multiply_btn, 1, 9, 1, 1)
    multiply_btn.clicked.connect(lambda: append(app, "*"))

    plus_btn = QPushButton("+")
    grid.addWidget(plus_btn, 2, 9, 1, 1)
    plus_btn.clicked.connect(lambda: append(app, "+"))

    minus_btn = QPushButton("-")
    grid.addWidget(minus_btn, 3, 9, 1, 1)
    minus_btn.clicked.connect(lambda: append(app, "-"))

    comma_btn = QPushButton(".")
    grid.addWidget(comma_btn, 4, 8, 1, 1)
    comma_btn.clicked.connect(lambda: append(app, "."))

    eval_btn = QPushButton("=")
    grid.addWidget(eval_btn, 4, 9, 1, 1)
    eval_btn.clicked.connect(lambda: evaluate(app))


def main():
    qt_app = QApplication(sys.argv)
    qt_app.setStyleSheet("""
        QWidget#window {
            background-color: #8E8E8E;
        }
        
        QPushButton {
            background-color: #D6D6D6;
            color: #282828;
            font-size: 15px;
            font-weight: 500;
            border-width: 0px;
            border-radius: 0px;
            width: 56px;
            height: 47px;
        }
        QPushButton:pressed {
            background-color: #8E8E8E;
            border-style: inset;
        }
        QPushButton[text="="], 
        QPushButton[text="+"], 
        QPushButton[text="-"],
        QPushButton[text="*"], 
        QPushButton[text="/"] {
            background-color: #F4913D;
            color: white;
        }
        QPushButton[text="="]:pressed, 
        QPushButton[text="+"]:pressed, 
        QPushButton[text="-"]:pressed,
        QPushButton[text="*"]:pressed, 
        QPushButton[text="/"]:pressed {
            background-color: #D6813A;
        }
        
        QWidget#output {
            background-color: #282828;
        }
        QLabel#output, QLabel#result {
            color: white;
            font-weight: light;
        }
        QLabel#output {
            font-size: 30px;
        }
        QLabel#result {
            font-size: 12px;
        }
        
        QTextEdit {
            background-color: transparent;
            max-height: 45px;
            font-size: 30px;
            min-width: 560px;
            max-width: 560px;
            text-align: right;
            color: white;
        }
    """)

    app_icon = QIcon()
    app_icon.addFile('resources/icon-16x.png', QtCore.QSize(16, 16))
    app_icon.addFile('resources/icon-64x.png', QtCore.QSize(64, 64))
    app_icon.addFile('resources/icon-128x.png', QtCore.QSize(128, 128))
    app_icon.addFile('resources/icon-256x.png', QtCore.QSize(256, 256))
    qt_app.setWindowIcon(app_icon)

    app = App()

    formula = QLabel("0")
    formula.setWordWrap(True)
    app.formula.listen(lambda o, n: formula.setText(n))
    formula.setObjectName("output")

    result = QLabel(app.result.value)
    app.result.listen(lambda o, n: result.setText(n))
    result.setObjectName("result")

    text_edit = QTextEdit()
    text_edit.setAlignment(QtCore.Qt.AlignRight)
    text_edit.setLineWrapMode(False)
    text_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    output_layout = QVBoxLayout()
    output_layout.addWidget(result, 0, QtCore.Qt.AlignRight)
    output_layout.addWidget(formula, 0, QtCore.Qt.AlignRight)
    # output_layout.addWidget(text_edit, 0, QtCore.Qt.AlignRight)
    output_layout.setContentsMargins(10, 5, 10, 5)

    output = QWidget()
    output.setObjectName('output')
    output.setLayout(output_layout)

    controls = QGridLayout()
    controls.setSizeConstraint(QLayout.SetNoConstraint)
    controls.setContentsMargins(0, 0, 0, 0)
    controls.setSpacing(1)

    setup_buttons(controls, app)
    setup_number_buttons(controls, app)
    setup_basic_buttons(controls, app)

    root = QVBoxLayout()
    root.setContentsMargins(0, 0, 0, 0)
    root.setSpacing(0)
    root.addWidget(output)
    root.addLayout(controls)

    window = QWidget()
    window.setObjectName("window")
    window.setLayout(root)
    # window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    window.setWindowTitle(app.title.value)
    app.title.listen(lambda o, n: window.setWindowTitle(n))
    window.show()
    window.setFixedSize(window.width(), window.height())

    sys.exit(qt_app.exec())


main()