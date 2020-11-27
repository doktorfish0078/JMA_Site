from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


# @app.route('/search_work')
# def search_work():
#     return render_template("search_work.html")


@app.route('/user/<string:name>')
def user(name):
    return "Hello, " + name + "!"


if __name__ == '__main__':
    app.run(debug=True)
