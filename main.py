import io
import random
from flask import Flask,redirect,url_for,render_template,request, Response
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


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
parse('x**2')

@app.route("/experiment_matplotlib.png")
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__== "__main__":
    app.run(debug=True,use_reloader=False)