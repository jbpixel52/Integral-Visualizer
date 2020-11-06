## Vengo corriendo a desearles un feliz jueves! : D
from flask import Flask,redirect,url_for,render_template,request
from sympy.parsing.sympy_parser import parse_expr


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




if __name__== "__main__":
    app.run(debug=True,use_reloader=False)