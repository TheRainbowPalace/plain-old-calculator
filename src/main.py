#!/usr/bin/env python

"""
© 2018 Jakob Rieke

Main entry point for 'Plain Old Calculator' (Poc) application

Todo:
* Add persistent preference managing
* Add tooltips to controls
* Create a better application icon
* Create scripts to build Mac Os, Windows and Linux Executables
"""


import sys
from time import time
import math_core
from observable import Observable, ObservableBool, ObservableString
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, \
    QLayout, QVBoxLayout, QTextEdit, QMainWindow


class App:
    def __init__(self):
        self.title = Observable("Calculator")
        self.window_position = (0, 0)
        self.empty_formula = '0'
        self.formula = ObservableString(self.empty_formula)
        self.result = ObservableString("")
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


def clear_last(app):
    app.formula.set(app.formula.value[:-1])
    if app.formula.value == '':
        app.formula.set(app.empty_formula)


def clear_history(app):
    app.history.clear()
    app.history_position = -1
    app.result.set('')


def select_previous(app):
    if len(app.history) == 0:
        return
    app.history_position = (app.history_position + 1) % len(app.history)
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
    formula = app.formula.value
    try:
        result = math_core.evaluate(formula)
        app.result.set('<i>' + formula + '</i> = ' + str(result))
        clear(app)
    except TypeError as e:
        app.result.set(str(e))
    except SyntaxError:
        app.result.set("Invalid syntax")
    except NameError as e:
        error_string = str(e)
        app.result.set(error_string[0].upper() + error_string[1:])

    # Add evaluated formula to history
    app.history.append(formula)
    if len(app.history) > app.max_history_length:
        app.history = app.history[1:]


def setup_extended_operator_buttons(grid, app):
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

    pow2_button = QPushButton("x^2")
    grid.addWidget(pow2_button, 1, 1, 1, 1)
    pow2_button.clicked.connect(lambda: append(app, "**2"))

    pow3_button = QPushButton("x^3")
    grid.addWidget(pow3_button, 1, 2, 1, 1)
    pow3_button.clicked.connect(lambda: append(app, "**3"))

    power_btn = QPushButton("x^y")
    grid.addWidget(power_btn, 1, 3, 1, 1)
    power_btn.clicked.connect(lambda: append(app, "**"))

    ee_button = QPushButton("EE")
    grid.addWidget(ee_button, 3, 5, 1, 1)
    ee_button.clicked.connect(lambda: append(app, "*10**"))

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


def setup_extended_control_buttons(grid, app):
    comma_btn = QPushButton(",")
    grid.addWidget(comma_btn, 1, 0, 1, 1)
    comma_btn.clicked.connect(lambda: append(app, ','))
    comma_btn.setShortcut(',')

    rand_btn = QPushButton("Rand")
    grid.addWidget(rand_btn, 4, 5, 1, 1)
    rand_btn.clicked.connect(lambda: append(app, "rand()"))

    bracket_open_btn = QPushButton("(")
    grid.addWidget(bracket_open_btn, 0, 0, 1, 1)
    bracket_open_btn.clicked.connect(lambda: append(app, "("))
    bracket_open_btn.setShortcut('(')

    bracket_close_btn = QPushButton(")")
    grid.addWidget(bracket_close_btn, 0, 1, 1, 1)
    bracket_close_btn.clicked.connect(lambda: append(app, ")"))
    bracket_close_btn.setShortcut(')')

    # Setup memory functionality
    mem_clear_btn = QPushButton("mc")
    grid.addWidget(mem_clear_btn, 0, 2, 1, 1)
    mem_clear_btn.clicked.connect(lambda: clear_history(app))

    previous_btn = QPushButton("pre")
    grid.addWidget(previous_btn, 0, 3, 1, 1)
    previous_btn.clicked.connect(lambda: select_previous(app))
    previous_btn.setShortcut('Down')

    next_btn = QPushButton("next")
    grid.addWidget(next_btn, 0, 4, 1, 1)
    next_btn.clicked.connect(lambda: select_next(app))
    next_btn.setShortcut('Up')

    mem_remove_btn = QPushButton("mr")
    grid.addWidget(mem_remove_btn, 0, 5, 1, 1)
    mem_remove_btn.clicked.connect(lambda: print("Unassigned"))


def setup_number_buttons(grid, app):
    number0_btn = QPushButton("0")
    grid.addWidget(number0_btn, 4, 6, 1, 2)
    number0_btn.clicked.connect(lambda: append(app, "0"))
    number0_btn.setShortcut('0')

    number1_btn = QPushButton("1")
    grid.addWidget(number1_btn, 3, 6, 1, 1)
    number1_btn.clicked.connect(lambda: append(app, "1"))
    number1_btn.setShortcut('1')

    number2_btn = QPushButton("2")
    grid.addWidget(number2_btn, 3, 7, 1, 1)
    number2_btn.clicked.connect(lambda: append(app, "2"))
    number2_btn.setShortcut('2')

    number3_btn = QPushButton("3")
    grid.addWidget(number3_btn, 3, 8, 1, 1)
    number3_btn.clicked.connect(lambda: append(app, "3"))
    number3_btn.setShortcut('3')

    number4_btn = QPushButton("4")
    grid.addWidget(number4_btn, 2, 6, 1, 1)
    number4_btn.clicked.connect(lambda: append(app, "4"))
    number4_btn.setShortcut('4')

    number5_btn = QPushButton("5")
    grid.addWidget(number5_btn, 2, 7, 1, 1)
    number5_btn.clicked.connect(lambda: append(app, "5"))
    number5_btn.setShortcut('5')

    number6_btn = QPushButton("6")
    grid.addWidget(number6_btn, 2, 8, 1, 1)
    number6_btn.clicked.connect(lambda: append(app, "6"))
    number6_btn.setShortcut('6')

    number7_btn = QPushButton("7")
    grid.addWidget(number7_btn, 1, 6, 1, 1)
    number7_btn.clicked.connect(lambda: append(app, "7"))
    number7_btn.setShortcut('7')

    number8_btn = QPushButton("8")
    grid.addWidget(number8_btn, 1, 7, 1, 1)
    number8_btn.clicked.connect(lambda: append(app, "8"))
    number8_btn.setShortcut('8')

    number9_btn = QPushButton("9")
    grid.addWidget(number9_btn, 1, 8, 1, 1)
    number9_btn.clicked.connect(lambda: append(app, "9"))
    number9_btn.setShortcut('9')


def setup_basic_buttons(grid, app):
    ac_btn = QPushButton("AC")
    grid.addWidget(ac_btn, 0, 6, 1, 1)
    ac_btn.clicked.connect(lambda: clear(app))
    ac_btn.setShortcut('Shift+c')

    back_btn = QPushButton("Br")
    grid.addWidget(back_btn, 0, 7, 1, 1)
    back_btn.clicked.connect(lambda: clear_last(app))

    mod_btn = QPushButton("mod")
    grid.addWidget(mod_btn, 0, 8, 1, 1)
    mod_btn.clicked.connect(lambda: append(app, "%"))
    mod_btn.setShortcut('%')

    divide_btn = QPushButton("/")
    grid.addWidget(divide_btn, 0, 9, 1, 1)
    divide_btn.clicked.connect(lambda: append(app, "/"))
    divide_btn.setShortcut('/')

    multiply_btn = QPushButton("*")
    grid.addWidget(multiply_btn, 1, 9, 1, 1)
    multiply_btn.clicked.connect(lambda: append(app, "*"))
    multiply_btn.setShortcut('*')

    plus_btn = QPushButton("+")
    grid.addWidget(plus_btn, 2, 9, 1, 1)
    plus_btn.clicked.connect(lambda: append(app, "+"))
    plus_btn.setShortcut('+')

    minus_btn = QPushButton("-")
    grid.addWidget(minus_btn, 3, 9, 1, 1)
    minus_btn.clicked.connect(lambda: append(app, "-"))
    minus_btn.setShortcut('-')

    comma_btn = QPushButton(".")
    grid.addWidget(comma_btn, 4, 8, 1, 1)
    comma_btn.clicked.connect(lambda: append(app, "."))
    comma_btn.setShortcut('.')

    eval_btn = QPushButton("=")
    grid.addWidget(eval_btn, 4, 9, 1, 1)
    eval_btn.clicked.connect(lambda: evaluate(app))
    eval_btn.setShortcut('Return')


def setup_controls(app):
    controls_layout = QGridLayout()
    controls_layout.setSizeConstraint(QLayout.SetNoConstraint)
    controls_layout.setContentsMargins(0, 0, 0, 0)
    controls_layout.setSpacing(1)

    setup_number_buttons(controls_layout, app)
    setup_basic_buttons(controls_layout, app)
    setup_extended_operator_buttons(controls_layout, app)
    setup_extended_control_buttons(controls_layout, app)

    controls = QWidget()
    controls.setLayout(controls_layout)

    return controls


def setup_result(app):
    text_edit = QTextEdit()
    text_edit.setObjectName("result")

    text_edit.setAlignment(Qt.AlignRight)
    text_edit.setLineWrapMode(False)
    text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    text_edit.document().setDocumentMargin(0)
    text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)

    h_scrollbar = text_edit.horizontalScrollBar()

    def set_text(text):
        text_edit.setText(text)
        text_edit.setAlignment(Qt.AlignRight)
        h_scrollbar.setValue(0)

    app.result.listen(lambda o, n: set_text(n))

    return text_edit


def setup_formula(app):
    text_edit = QTextEdit(app.empty_formula)
    text_edit.setObjectName("formula")

    text_edit.setAlignment(Qt.AlignRight)
    text_edit.setLineWrapMode(False)
    text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    text_edit.document().setDocumentMargin(0)
    text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)

    h_scrollbar = text_edit.horizontalScrollBar()

    def set_text(text):
        text_edit.setText(text)
        text_edit.setAlignment(Qt.AlignRight)
        h_scrollbar.setValue(h_scrollbar.maximum())

    app.formula.listen(lambda o, n: set_text(n))

    return text_edit


def setup_output(app):
    result = setup_result(app)
    formula = setup_formula(app)

    output_layout = QVBoxLayout()
    output_layout.addWidget(result, 0, Qt.AlignRight)
    output_layout.addWidget(formula, 0, Qt.AlignRight)
    output_layout.setContentsMargins(10, 5, 10, 5)

    output = QWidget()
    output.setObjectName('output')
    output.setLayout(output_layout)

    return output


def main():
    start_time = time()

    qt_app = QApplication(sys.argv)
    qt_app.setStyleSheet("""
        QWidget#root {
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
        QTextEdit#formula, QTextEdit#result {
            background-color: transparent;
            color: white;
            font-weight: light;
            min-width: 560px;
            max-width: 560px;
        }
        QTextEdit#formula {
            max-height: 45px;
            font-size: 30px;
        }
        QTextEdit#result {
            max-height: 20px;
            font-size: 12px;
        }
    """)

    app_icon = QIcon()
    app_icon.addFile('../resources/icon-16x.png', QSize(16, 16))
    app_icon.addFile('../resources/icon-64x.png', QSize(64, 64))
    app_icon.addFile('../resources/icon-128x.png', QSize(128, 128))
    app_icon.addFile('../resources/icon-256x.png', QSize(256, 256))
    qt_app.setWindowIcon(app_icon)

    app = App()

    output = setup_output(app)
    controls = setup_controls(app)

    root_layout = QVBoxLayout()
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.setSpacing(0)
    root_layout.addWidget(output)
    root_layout.addWidget(controls)

    def onKeyPressed(event):
        key = event.key()
        is_shift = event.modifiers() == Qt.ShiftModifier
        is_ctrl = event.modifiers() == Qt.ControlModifier
        is_alt = event.modifiers() == Qt.AltModifier

        if key == Qt.Key_Backspace:
            clear_last(app)
        elif 65 <= key <= 90 and not is_shift and not is_ctrl and not is_alt:
            append(app, chr(key).lower())
        elif key == Qt.Key_Greater:
            append(app, '>')
        elif key == Qt.Key_Less:
            append(app, '<')
        elif key == Qt.Key_Equal:
            append(app, '=')

    root = QWidget()
    root.setObjectName("root")
    root.keyPressEvent = lambda event: onKeyPressed(event)
    root.setLayout(root_layout)
    root.setWindowTitle(app.title.value)
    app.title.listen(lambda o, n: root.setWindowTitle(n))

    window = QMainWindow()
    window.setWindowTitle("Plain Old Calculator")
    window.setCentralWidget(root)

    window.show()
    window.setFixedSize(root.width(), root.height())

    print('Start time:', str(round(time() - start_time, 3)) + 's')
    qt_app.exec()


if __name__ == '__main__':
    sys.exit(main())
