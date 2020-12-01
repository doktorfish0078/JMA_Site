from flask import Flask, render_template, url_for
from werkzeug.utils import redirect

app = Flask(__name__)
user_in = False

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template("index.html", user=user_in)


@app.route('/work_search')
@app.route('/work_search/<int:page>')
def search_work(page=1):
    return render_template("work_search.html", page=page, user=user_in)


@app.route('/employees_search')
def employees_search():
    return render_template("employees_search.html", user=user_in)


@app.route('/create_cv')
def create_cv():
    return render_template("create_cv.html", user=user_in)


@app.route('/create_vacancy')
def create_vacancy():
    return render_template("create_vacancy.html", user=user_in)


@app.route('/authorization')
def authorization():
    return render_template("authorization.html", user=user_in)


@app.route('/registration')
def registration():
    return render_template("registration.html", user=user_in)


@app.route('/profile')
def profile():
    return render_template("profile.html", user=user_in)


@app.route('/welcome')
def user():
    global user_in
    user_in = True
    return redirect("/profile", code=302)


@app.route('/goodbye')
def user_out():
    global user_in
    user_in = False
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=False)