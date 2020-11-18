import matplotlib.patches as polyplot
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from flask import Flask, redirect, render_template, request, url_for
from sympy import *
from sympy.abc import x
from sympy.parsing.sympy_parser import (convert_xor,
                                        implicit_multiplication_application,
                                        parse_expr, standard_transformations)
from sympy.solvers.solveset import substitution
from sympy.utilities.lambdify import implemented_function, lambdify
mpl.use('Agg')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def parse(expresion):
    return parse_expr(expresion)


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

    print('se ha parseado tio!')

    return lambdify(x, parsed, 'numpy')


def integral_plot(f, a, b, N):
    text = f"trapecio:{trapz(f,a,b,N)}\n1/8:{simps(f,a,b,N)}\n3/8:{simps(f,a,b,N)}"
    temptrap = float(trapz(f, a, b, N))
    temp18 = float(simps(f, a, b, N))
    temp38 = float(simpson38(f,a,b,N))
    x = np.linspace(a, b, num=N)
    y = f(x)
    fig, ax = plt.subplots()
    ax.set_facecolor('#e91e63')
    ax.plot(x, y, 'ro', linewidth=3, color='pink')
    ax.text(.7, 0.8, f'trapecio: {temptrap}',
            bbox=dict(facecolor='#e91e63', alpha=0.5))
    ax.text(.7, 0.7, f'Simpson 1/8: {temp18}',
            bbox=dict(facecolor='#e91e63', alpha=0.5))
    ax.text(.7, 0.6, f'Simpson 3/8: {temp38}',
            bbox=dict(facecolor='#e91e63', alpha=0.5))
    plt.grid(True, linestyle=':')
    plt.title(f'Integral')
    plt.plot(legend=f'x:[{x}]')    # Make the shaded region
    ix = np.linspace(a, b, num=N)
    iy = f(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    t = tuple(verts)
    p = Polygon(*t)
    plt.Polygon

    poly = polyplot.Polygon(t, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)
    # plot.show()
    plt.savefig('static/photos/integral.png')


@app.route('/trapz')
def trapz(f, a, b, N):
    x = np.linspace(a, b, N+1)  # N+1 points make N subintervals
    y = f(x)
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)
    return T


@app.route('/simps1')
def simps(f, a, b, N):
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

    return render_template('index.html', url="static/photos/integral.png")


def simpson38(f, a, b, N):
    h = (b - a) / N
    integration = f(a) + f(b)
    for i in range(1, N):
        k = a + i*h
        if i % 2 == 0:
            integration = integration + 2 * f(k)
        else:
            integration = integration + 3 * f(k)
    integration = integration * 3 * h / 8
    return integration


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
