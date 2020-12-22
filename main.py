from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
user_in = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return "Ads %r" % self.id


class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return "Ads %r" % self.id


# отслеживание главной страницы
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template("index.html", user=user_in)


# отслеживание адреса поиска работ
@app.route('/work_search')
def search_work():
    vacancies = Vacancy.query.all()
    text_search = request.args.get('search')
    sort_filter = request.args.get('sortFilter')
    if text_search:
        vacancies = Vacancy.query.filter(text_search == Vacancy.title).all()
    if sort_filter:
        if sort_filter == 'byname':
            vacancies = Vacancy.query.order_by(Vacancy.title.desc()).all()
        elif sort_filter == 'bypricedesc':
            vacancies = Vacancy.query.order_by(Vacancy.price.desc()).all()
        elif sort_filter == 'bypriceasc':
            vacancies = Vacancy.query.order_by(Vacancy.price.asc()).all()
        elif sort_filter == 'bydate':
            vacancies = Vacancy.query.order_by(Vacancy.date.desc()).all()

    return render_template("work_search.html", user=user_in, vacancies=vacancies)


# отслеживание адреса поиска вакансий
@app.route('/employees_search')
def employees_search():
    cvs = CV.query.all()
    text_search = request.args.get('search')
    sort_filter = request.args.get('sortFilter')
    if text_search:
        cvs = CV.query.filter(text_search == CV.title).all()
    if sort_filter:
        if sort_filter == 'byname':
            cvs = CV.query.order_by(CV.title.desc()).all()
        elif sort_filter == 'bypricedesc':
            cvs = CV.query.order_by(CV.price.desc()).all()
        elif sort_filter == 'bypriceasc':
            cvs = CV.query.order_by(CV.price.asc()).all()
        elif sort_filter == 'bydate':
            cvs = CV.query.order_by(CV.date.desc()).all()
    return render_template("employees_search.html", user=user_in, cvs=cvs)


# Форма создания резюме
@app.route('/create_cv', methods=['POST', 'GET'])
def create_cv():
    if request.method == "POST":
        title = request.form['cv_name']
        description = request.form['text']
        location = request.form['location']
        price = request.form['price']

        cv = CV(title=title, description=description, location=location, price=price)
        try:
            db.session.add(cv)
            db.session.commit()
            return redirect('/employees_search')
        except:
            return "При добавлении объявления произошла ошибка"
    else:
        return render_template("create_cv.html", user=user_in)


# Форма создания вакансии
@app.route('/create_vacancy', methods=['POST', 'GET'])
def create_vacancy():
    if request.method == "POST":
        title = request.form['vacancy_name']
        description = request.form['text']
        location = request.form['location']
        price = request.form['price']

        vacancy = Vacancy(title=title, description=description, location=location, price=price)
        try:
            db.session.add(vacancy)
            db.session.commit()
            return redirect('/work_search')
        except:
            return "При добавлении объявления произошла ошибка"
    else:
        return render_template("create_vacancy.html", user=user_in)


# Форма авторизации
@app.route('/authorization')
def authorization():
    return render_template("authorization.html", user=user_in)


# Форма регистрации
@app.route('/registration')
def registration():
    return render_template("registration.html", user=user_in)


# Профиль, мои резюме и вакансии
@app.route('/profile')
@app.route('/profile/<string:my>')
def profile(my=None):
    if my:
        path = my
        if my == 'my_cv':
            cvs = CV.query.all()
            return render_template("profile.html", user=user_in, ads=cvs, path=path)
        elif my == 'my_vacancy':
            vacancies = Vacancy.query.all()
            return render_template("profile.html", user=user_in, ads=vacancies, path=path)
    else:
        return render_template("profile.html", user=user_in)


# Удаление объявления из личного кабинета
@app.route('/profile/<string:my>/<int:id>/ad_delete')
def delete_ad(id, my=None):
    ad_deteled = None
    if my:
        if my == 'my_cv':
            ad_deteled = CV.query.get_or_404(id)
        elif my == 'my_vacancy':
            ad_deteled = Vacancy.query.get_or_404(id)
        try:
            db.session.delete(ad_deteled)
            db.session.commit()
            return redirect('/profile/{}'.format(my))
        except:
            return "При удалении объявления произошла ошибка"


# Редактирование объявления из личного кабинета
@app.route('/profile/<string:my>/<int:id>/ad_redaction', methods=['POST', 'GET'])
def update_ad(id, my=None):
    ad_redaction = None
    if my:
        if my == 'my_cv':
            ad_redaction = CV.query.get_or_404(id)
        elif my == 'my_vacancy':
            ad_redaction = Vacancy.query.get_or_404(id)

    if request.method == 'POST':
        ad_redaction.title = request.form['vacancy_name']
        ad_redaction.description = request.form['text']
        ad_redaction.location = request.form['location']
        ad_redaction.price = request.form['price']
        try:
            db.session.commit()
            return redirect('/profile/{}'.format(my))
        except:
            return "При удалении объявления произошла ошибка"
    else:
        return render_template("update_vacancy.html", user=user_in, ad=ad_redaction)


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
