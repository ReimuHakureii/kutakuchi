import random
import sympy as sp
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from sympy.printing import latex
import tempfile
import os

# Def symbols
x, y, z = sp.symbols('x y z')
variables = [x, y, z]

# Possible functions and operations
functions = [sp.sin, sp.cos, sp.tan, sp.exp, sp.log, sp.sqrt, sp.sinh, sp.cosh, sp.asin, sp.acos, sp.atan]
operations = [sp.Add, sp.Mul, sp.Pow]

# Random Coeff gen
def rand_coeff():
    return random.randint(-10, 10)

# Gen rand atomic term
def random_atom():
    var = random.choice(variables)
    form = random.choice(["var", "coeff*var", "coeff", "func"])

    if form == "var":
        return var
    elif form == "coeff*var":
        return rand_coeff() * var
    elif form == "coeff":
        return rand_coeff()
    else: 
        # Apply nested functions
        func = random.choice(functions)
        return func(rand_coeff() * var**random.randint(1,3))

# Generate rational / nested expression
def random_expression(depth=0, max_depth=5):
    if depth >= max_depth or random.random() < 0.25:
        return random_atom()
    op = random.choice(operations)
    left = random_expression(depth+1, max_depth)
    right = random_expression(depth+1, max_depth)

    if op == sp.Pow:
        return sp.Pow(left, random.ranint(2, 5))
    elif op == sp.Mul and random.random() < 0.3:
        return left / (right + rand_coeff() or 1)
    return op(left, right)

# Diff styles of eq gens
def polynominal_expression():
    return sum(rand_coeff() * random.choice(variables)**random.randint(1, 6) for _ in range(random.randint(3, 6)))

def trigonometric_expression():
    var = random.choice(variables)
    expr = sum(random.choice([sp.sin, sp.cos, sp.tan, sp.sinh, sp.cosh])(rand_coeff() * var**random.randint(1, 3)) for _ in range(random.randint(2, 5)))
    return expr

def exponential_log_expression():
    var = random.choice(variables)
    expr = sp.exp(rand_coeff() * var**random.randint(1, 3)) + sp.log(var**2 + abs(rand_coeff()) + 1)
    return expr

def rational_expression():
    num = polynominal_expression() + trigonometric_expression()
    den = polynominal_expression() + (rand_coeff() or 1)
    return num / den

def nested_transcendental_expression():
    var = random.choice(variables)
    expr = sp.sin(sp.exp(var**2)) + sp.log(sp.cos(var) + 2)
    return expr

def piecewise_expression():
    var = random.choice(variables)
    return sp.Piecewise((var**2, var < 0), (sp.sin(var), var >= 0))