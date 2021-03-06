
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
    return render_template("index.html", name=name,eq="Ingrese la ecuacion", punto_a="Ingresa el punto A",punto_b="Ingrese punto B",iteraciones="Ingrese el numero de iteraciones",porcentaje ="Ingrese el %% error deseado")


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
    return render_template('login.html', error=error )


def f(xyz):
    """ESTA FUNCION AGARRA UNA FUNCION COMO UN STRING Y LA TRANSFORMA A UNA EXPRESION DE SYMPY, LA CUAL SE LE HACEN TRANSFORMACIONES PARA QUE CUALQUIER TIPO DE FUNCION MATEMATICA SEA VALIDA AL MOMENTO DE EVALUAR; P.E: x*cos(x!*x)"""
    transformations = (standard_transformations +
                       (implicit_multiplication_application,) + (convert_xor,))
    parsed = parse_expr(xyz, evaluate=True,
                        transformations=transformations)
    x = symbols('x')
    print('se ha parseado tio!')

    return lambdify(x, parsed, 'numpy')


def integral_plot(f, a, b, N):
    temptrap = "%.6f" % (float(trapz(f, a, b, N)))
    temp18 = "%.6f" % (float(simps(f, a, b, N)))
    temp38 = "%.6f" % (float(simpson38(f, a, b, N)))
    text = f"trapecio:{temptrap}  1/8:{temp18}\n3/8:{temp38}"
    x = np.linspace(a, b, num=N)
    y = f(x)
    fig, ax = plt.subplots()
    ax.set_facecolor('#FFDD00')
    ax.plot(x, y, 'ro', linewidth=3, color='pink')
    plt.grid(True, linestyle=':')
    plt.title(f'Integral')
    plt.plot(legend=f'x:[{x}]')    # Make the shaded region
    ax.text(.2, 0.9, f'{text}',
            bbox=dict(facecolor='#808080', alpha=0.5))

    ix = np.linspace(a, b, num=N)
    iy = f(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    t = tuple(verts)
    p = Polygon(*t)
    plt.Polygon

    poly = polyplot.Polygon(t, facecolor='#212121', edgecolor='0.8')
    ax.add_patch(poly)
    # plot.show()
    plt.savefig('static/photos/integral.png')
    calculos = [temptrap, temp18, temp38]
    return calculos


@app.route('/trapz')
def trapz(f, a, b, N):
    x = np.linspace(a, b, N+1)  # N+1 points make N subintervals
    y = f(x)
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)
    print(T)
    return T


def simpson38(f, a, b, n):
    h = (b-a)/n
    suma = 0

    for k in range(2, n, 3):
        x = a+(k-1)*h
        suma = suma+f(x)

    sum1 = 0
    for k in range(3, n+1, 3):
        x = a+(k-1)*h
        sum1 = sum1+f(x)

    sum2 = 0
    for k in range(4, n-1, 3):
        x = a+(k-1)*h
        sum2 = sum2+f(x)

    integration = (f(a)+3*suma+3*sum1+2*sum2+f(b))*3*h/8
    return integration


@app.route('/simps1')
def simps(f, a, b, N):
    dx = (b-a)/N
    x = np.linspace(a, b, N+1)
    y = f(x)
    S = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    print(S)
    return S


def realIntegral(xyz, a, b):

    transformations = (standard_transformations +
                       (implicit_multiplication_application,) + (convert_xor,))
    parsed = parse_expr(xyz, evaluate=True,
                        transformations=transformations)
    x = symbols('x')
    fprime = integrate(parsed, x)
    flambda = lambdify(x, fprime, 'numpy')

    return float(flambda(b)-flambda(a))


def compare(areas, real, porcentage):
    metodos = ['TRAPECIO', 'SIMPSON 1/8', 'SIMPSON 3/8']
    errors = []
    for x in areas:
        errors.append(abs((float(x)-float(real))/float(real))*100)
    best = min(errors)

    output = []
    for i in range(len(metodos)):
        output.append(f'{metodos[i]}: {areas[i]};   %Error: {errors[i]}')
    return output


@app.route('/butt', methods=["GET", "POST"])
def butt():
    a = float(request.form['a'])
    b = float(request.form['b'])
    n = int(request.form['n'])
    ecuacion = request.form['ecuacion']
    tolerancia = float(request.form['porciento'])/100
    if n % 2 == 1:
        n += 1
    n_original = n
    print("tipo de la ecuacion:", type(ecuacion))
    print("tipo de la a:", type(a))
    print("tipo de la b:", type(b))
    print("{} {} {} {}".format(a, b, n, ecuacion))
    print(request.form['button'])
    resultados = integral_plot(f(ecuacion), a, b, n)
    real = (realIntegral(xyz=ecuacion, a=a, b=b))
    lista = compare(areas=resultados, real=real, porcentage=tolerancia)

    if n_original == 69:
        return render_template('index.html', url="static/photos/integral.png", real_area=real, comparacion=lista, nice=true)

    return render_template('index.html', url="static/photos/integral.png", real_area=real, comparacion=lista, eq=ecuacion, punto_a=str(a),punto_b=str(b),iteraciones=str(n),porcentaje =str(tolerancia*100))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
