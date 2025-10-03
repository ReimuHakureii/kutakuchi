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
def polynomial_expression():
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
    num = polynomial_expression() + trigonometric_expression()
    den = polynomial_expression() + (rand_coeff() or 1)
    return num / den

def nested_transcendental_expression():
    var = random.choice(variables)
    expr = sp.sin(sp.exp(var**2)) + sp.log(sp.cos(var) + 2)
    return expr

def piecewise_expression():
    var = random.choice(variables)
    return sp.Piecewise((var**2, var < 0), (sp.sin(var), var >= 0))

def differential_expression():
    var = random.choice(variables)
    f = sp.Function('f')(var)
    return sp.diff(f, var, random.randint(1, 3))

def integral_expression():
    var = random.choice(variables)
    return sp.integrate(random.choice([sp.sin(var), sp.exp(var), var**2]), (var, 0, random.randint(1, 5)))

def mixed_expression():
    return random_expression(max_depth=4)

# Map style to func
styles = {
    "polynomial": polynomial_expression,
    "trigonometric": trigonometric_expression,
    "exponential_log": exponential_log_expression,
    "rational": rational_expression,
    "nested_transcendental": nested_transcendental_expression,
    "piecewise": piecewise_expression,
    "differential": differential_expression,
    "integral": integral_expression,
    "mixed": mixed_expression,
    "random": lambda: random.choice([
        polynomial_expression,
        trigonometric_expression,
        exponential_log_expression,
        rational_expression,
        nested_transcendental_expression,
        piecewise_expression,
        differential_expression,
        integral_expression,
        mixed_expression
    ])()
}

# Gen full eq
def random_equation(style="random")
    if style not in styles:
        raise ValueError(f"Unknown style: {style}")
    lhs = styles[style]()
    rhs = styles[style]()
    return sp.Eq(lhs, rhs)

# Gen sys of eq
def random_system(n=3, style="random"):
    return [random_equation(style) for _ in range(n)]

# Render LaTeX
def render_latex_to_image(latex_str, filename):
    plt.figure(figsize=(0.01, 0.01))
    plt.text(0.5, 0.5, f"${latex_str}$", fontsize=14, ha="center", va="center")
    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight", pad_inches=0.2, dpi=200)
    plt.close()

# Save eq to PDF rendered with math and LaTeX
def save_to_pdf(equations, filename="equations.pdf")
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)

    doc = SimpleDocTemplate(filepath)
    story = []
    styles_pdf = getSampleStyleSheet()
    
    for eq in equations:
        latex_eq = sp.latex(eq)

        # Render math image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            render_latex_to_image(latex_eq, tmpfile.name)
            story.append(Image(tmpfile.name, width=5 * inch, height=0.8 * inch))
        
        # Add LaTeX code as text
        story.append(Paragraph(f"<b>LaTeX:<b> {latex_eq}", styles_pdf["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

    doc.build(story)
    print(f"Equations saved to {filepath}")

if __name__ == "__main__":
    all_equations = []
    
    print("--- Polynomial Equations ---")
    for _ in range(2):
        eq = random_equation("polynomial")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Trigonometric Equations ---")
    for _ in range(2):
        eq = random_equation("trigonometric")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Exponential/Log Equations ---")
    for _ in range(2):
        eq = random_equation("exponential_log")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Rational Equations ---")
    for _ in range(2):
        eq = random_equation("rational")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Nested Transcendental Equations ---")
    for _ in range(2):
        eq = random_equation("nested_transcendental")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Piecewise Equations ---")
    for _ in range(2):
        eq = random_equation("piecewise")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Differential Equations ---")
    for _ in range(2):
        eq = random_equation("differential")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)
        
    print("\n--- Integral Equations ---")
    for _ in range(2):
        eq = random_equation("integral")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Mixed Random Equations ---")
    for _ in range(2):
        eq = random_equation("random")
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    print("\n--- Random System (Mixed) ---")
    for eq in random_system(3, "random"):
        print(eq)
        print("LaTeX:", sp.latex(eq))
        all_equations.append(eq)

    # Save?
    choice = (
        input(
            "\nDo you want to save these equations as a rendered PDF (with LaTeX code)? (y/n):"
        )
        .strip()
        .lower()
    )
    if choice == "y":
        save_to_pdf(all_equations)