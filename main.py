from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/work_search')
@app.route('/work_search/<int:page>')
def search_work(page=1):
    return render_template("work_search.html", page=page)


@app.route('/employees_search')
def employees_search():
    return render_template("employees_search.html")

@app.route('/create_cv')
def create_cv():
    return render_template("create_cv.html")

@app.route('/create_vacancy')
def create_vacancy():
    return render_template("create_vacancy.html")

@app.route('/authorization')
def authorization():
    return render_template("authorization.html")

@app.route('/registration')
def registration():
    return render_template("registration.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/user/<string:name>')
def user(name):
    return "Hello, " + name + "!"


if __name__ == '__main__':
    app.run(debug=True)
