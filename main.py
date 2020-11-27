from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/work_search')
def search_work():
    return render_template("work_search.html")\

@app.route('/employees_search')
def employees_search():
    return render_template("employees_search.html")


@app.route('/user/<string:name>')
def user(name):
    return "Hello, " + name + "!"


if __name__ == '__main__':
    app.run(debug=True)
