# %%
from flask import Flask, redirect, url_for, render_template, request
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify, implemented_function
import matplotlib.pyplot as plot
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy.abc import x
from sympy.solvers.solveset import substitution
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import *
import numpy as np
import matplotlib.patches as polyplot


def parse(expresion):
    return parse_expr(expresion)


app = Flask(__name__)


@app.route("/")
def index(name=None, methods=["GET", "POST"]):
    return render_template("index.html", name=name)


@app.route("/plot")
def graphic():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


def f(xyz):
    """ESTA FUNCION AGARRA UNA FUNCION COMO UN STRING Y LA TRANSFORMA A UNA EXPRESION DE SYMPY, LA CUAL SE LE HACEN TRANSFORMACIONES PARA QUE CUALQUIER TIPO DE FUNCION MATEMATICA SEA VALIDA AL MOMENTO DE EVALUAR; P.E: x*cos(x!*x)"""
    transformations = (standard_transformations +
                       (implicit_multiplication_application,) + (convert_xor,))
    parsed = parse_expr(xyz, evaluate=True,
                        transformations=transformations)
    print(parsed)
    z = symbols('z')

    print('se ha parseado tio!')

    return lambdify(x, parsed, 'numpy')


def integral_plot(f, a, b, N):

    x = np.linspace(a, b, num=N)
    y = f(x)
    #fig = plot.subplots()
    ax = plot.subplots()
    ax.plot(x, y, 'ro', linewidth=3, color='pink')
    plot.grid(True, linestyle=':')
    plot.title(f'Integral')
    plot.plot(legend=f'x:[{x}]')

    # Make the shaded region
    ix = np.linspace(a, b, num=N)
    iy = f(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    t = tuple(verts)
    p = Polygon(*t)
    plot.Polygon
    poly = polyplot.Polygon(t, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)
    plot.show()
    return plot.savefig('static/photos/integral.png')


@app.route('/trapz')
def trapz(f, a, b, N=50):
    x = np.linspace(a, b, N+1)  # N+1 points make N subintervals
    y = f(x)
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)
    return T


@app.route('/simps1')
def simps(f, a, b, N=50):
    dx = (b-a)/N
    x = np.linspace(a, b, N+1)
    y = f(x)
    S = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    return S


@app.route('/butt', methods=["GET", "POST"])
def butt():
    a = float(request.form['a'])
    b = float(request.form['b'])
    n = int(request.form['n'])
    ecuacion = request.form['ecuacion']
    print("tipo de la ecuacion:", type(ecuacion))
    print("tipo de la a:", type(a))
    print("tipo de la b:", type(b))
    print("{} {} {} {}".format(a, b, n, ecuacion))
    print(request.form['button'])
    integral_plot(f(ecuacion), a, b, n)

    return render_template('graph.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
