"""
© 2018 Jakob Rieke

Core Library for mathematical expression parsing in Poc

Todo:
* Use sth different then eval(...) to evaluate expressions (maybe SymPy)
"""

from math import *
import math
from random import random as rand
import parser


def evaluate(formula):
    return eval(parser.expr(formula).compile())


def sqrt(value, n):
    return value ** (1/n)


def sqrt2(value):
    return math.sqrt(value)


def sqrt3(value):
    return value ** (1/3)


def ln(value):
    return math.log(value, math.e)


def deg(value):
    return math.degrees(value)
