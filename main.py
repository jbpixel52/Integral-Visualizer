
## Vengo corriendo a desearles un feliz jueves! : D
from flask import Flask,redirect,url_for,render_template,request
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function
import matplotlib.pyplot as plot

def parse(expresion):
    return parse_expr(expresion)


app= Flask(__name__)

@app.route("/")
def index(name=None, methods=["GET","POST"]):
    return render_template("index.html",name=name)

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


equation_parsed = parse('x**2')


def funcion(x):
    return x+1
    
def integral_plot(f,a,b,N,dx):
    x = np.linspace(a, b, num=N)
    y = f(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'ro', linewidth=3,color='pink') 
    plt.grid(True,linestyle=':')
    plt.title(f'Integral')
    plt.plot(legend=f'x:[{x}]')
    
    # Make the shaded region
    ix = np.linspace(a, b,num=N)
    iy = f(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)
    plt.show()


def trapz(f, a, b, N=50):
    x = np.linspace(a, b, N+1)  # N+1 points make N subintervals
    y = f(x)
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)
    return T

def simps(f, a, b, N=50):
    dx = (b-a)/N
    x = np.linspace(a, b, N+1)
    y = f(x)
    S = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    return S




if __name__== "__main__":
    app.run(debug=True,use_reloader=False)