#%%
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy.abc import x
from sympy.solvers.solveset import substitution
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function
from sympy import *
import numpy as np

def f():
    """ESTA FUNCION AGARRA UNA FUNCION COMO UN STRING Y LA TRANSFORMA A UNA EXPRESION DE SYMPY, LA CUAL SE LE HACEN TRANSFORMACIONES PARA QUE CUALQUIER TIPO DE FUNCION MATEMATICA SEA VALIDA AL MOMENTO DE EVALUAR; P.E: x*cos(x!*x)"""
    transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
    parsed = parse_expr(input(),evaluate=False,transformations=transformations)
    print(parsed)
    z = symbols('z')
    
    print(parsed.subs(x,5))
          
    return lambdify(x,parsed,'numpy')
    
def trapz(f, a, b, N=50):
    x = np.linspace(a, b, N+1)  # N+1 points make N subintervals
    y = f(x)
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)
    print('T',T)
    return T


if __name__ == "__main__":
   trapz(f(),1,10,10)