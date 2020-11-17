# %%
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy.abc import x
from sympy.solvers.solveset import substitution
from sympy.utilities.lambdify import lambdify, implemented_function
import matplotlib.pyplot as plt, mpld3
from sympy import Function
from sympy import *
import numpy as np
import matplotlib.patches as polyplot


def integral_plot(f, a, b, N, dx):
    
    x = np.linspace(a, b, num=N)
    y = f(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'ro', linewidth=3, color='pink')
    plt.grid(True, linestyle=':')
    plt.title(f'Integral')
    plt.plot(legend=f'x:[{x}]')

    # Make the shaded region
    ix = np.linspace(a, b, num=N)
    iy = f(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    t = tuple(verts)
    p = Polygon(*t)
    plt.Polygon
    poly = polyplot.Polygon(t, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)

    mpld3.show()
    plt.savefig('integral.png')


def f():
    """ESTA FUNCION AGARRA UNA FUNCION COMO UN STRING Y LA TRANSFORMA A UNA EXPRESION DE SYMPY, LA CUAL SE LE HACEN TRANSFORMACIONES PARA QUE CUALQUIER TIPO DE FUNCION MATEMATICA SEA VALIDA AL MOMENTO DE EVALUAR; P.E: x*cos(x!*x)"""
    transformations = (standard_transformations +
                       (implicit_multiplication_application,) + (convert_xor,))
    parsed = parse_expr(input(), evaluate=False,
                        transformations=transformations)
    print(parsed)
    z = symbols('z')

    print(parsed.subs(x, 5))

    return lambdify(x, parsed, 'numpy')


def trapz(f, a, b, N=50):
    x = np.linspace(a, b, N+1)  # N+1 points make N subintervals
    y = f(x)
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)
    print('T', T)
    return T

def simps(f, a, b, N=50):
    dx = (b-a)/N
    x = np.linspace(a, b, N+1)
    y = f(x)
    S = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    return S


if __name__ == "__main__":
    # trapz(f(),1,10,10)
    integral_plot(f(), 1, 10, 10, 0.5)
# %%
