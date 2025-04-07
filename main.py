from flask import Flask, make_response, request, session, redirect, render_template, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from requests import get
from unicodedata import category

import jobs_api
import resources.job_resource
import resources.users_resource
import users_api
from data import db_session
from data.category import Category
from data.jobs import Jobs
from data.departments import Departament
from data.users import User
from draw_map import draw_map
from forms.departments import DepartForm
from forms.login import LoginForm
from forms.news import JobForm
from forms.register import RegisterForm
from get_coords import get_coords
from flask_restful import abort, Api

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'sqlalchemy_second'


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    # ---------------------------------------------------------------------------------
    # category_light = db_sess.query(Category).filter(Category.name == 'light').first()
    # category_medium = db_sess.query(Category).filter(Category.name == 'medium').first()
    # category_hard = db_sess.query(Category).filter(Category.name == 'hard').first()
    #
    # job = db_sess.query(Jobs).filter(Jobs.job == 'deployment of residential modules 1 and 2').first()
    # job.categories.append(category_light)
    # job.categories.append(category_medium)
    # db_sess.add(job)
    #
    # job = db_sess.query(Jobs).filter(Jobs.job == 'настройка оборудования').first()
    # job.categories.append(category_medium)
    # db_sess.add(job)
    #
    # job = db_sess.query(Jobs).filter(Jobs.job == 'управление аппаратом').first()
    # job.categories.append(category_medium)
    # job.categories.append(category_hard)
    # db_sess.add(job)
    #
    # job = db_sess.query(Jobs).filter(Jobs.job == 'Fifth').first()
    # job.categories.append(category_light)
    # db_sess.add(job)
    #
    # job = db_sess.query(Jobs).filter(Jobs.job == 'tr').first()
    # job.categories.append(category_light)
    # db_sess.add(job)
    #
    # job = db_sess.query(Jobs).filter(Jobs.job == 'example').first()
    # job.categories.append(category_light)
    # job.categories.append(category_medium)
    # job.categories.append(category_hard)
    # db_sess.add(job)

    # if category:
    #     for job in category.jobs:
    #         job.categories.remove(category)  # Удаляем связь
    #
    #     # Удаляем саму категорию
    #     db_sess.delete(category)

    api.add_resource(resources.job_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(resources.job_resource.JobsListResource, '/api/v2/jobs')

    api.add_resource(resources.users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(resources.users_resource.UsersListResource, '/api/v2/users')

    db_sess.commit()
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    return render_template("news.html", jobs=news)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.leader_id.data
        job.work_size = form.work.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finish.data
        current_user.news.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('re_news.html', title='Добавление новости',
                           form=form)


@app.route('/addjob/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter((Jobs.team_leader == current_user.id) | (current_user.id == 1),
                                          Jobs.id == id).first()
        if news:
            form.title.data = news.job
            form.leader_id.data = news.team_leader
            form.work.data = news.work_size
            form.collaborators.data = news.collaborators
            form.is_finish.data = news.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter((Jobs.team_leader == current_user.id) | (current_user.id == 1),
                                          Jobs.id == id).first()
        if news:
            news.job = form.title.data
            news.team_leader = form.leader_id.data
            news.work_size = form.work.data
            news.collaborators = form.collaborators.data
            news.is_finished = form.is_finish.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('re_news.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter((Jobs.team_leader == current_user.id) | (current_user.id == 1),
                                      Jobs.id == id).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    depart = db_sess.query(Departament).all()
    return render_template("departments.html", depart=depart)


@app.route('/adddepart', methods=['GET', 'POST'])
@login_required
def add_depart():
    form = DepartForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Departament()
        dep.title = form.title.data
        dep.chief = form.leader_id.data
        dep.members = form.members.data
        dep.email = form.email.data
        current_user.depart.append(dep)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('re_department.html', title='Добавление департамента',
                           form=form)


@app.route('/adddepart/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        depart = db_sess.query(Departament).filter((Departament.chief == current_user.id) | (current_user.id == 1),
                                                   Departament.id == id).first()
        if depart:
            form.title.data = depart.title
            form.leader_id.data = depart.chief
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = db_sess.query(Departament).filter((Departament.chief == current_user.id) | (current_user.id == 1),
                                                   Departament.id == id).first()
        if depart:
            depart.title = form.title.data
            depart.chief = form.leader_id.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('re_department.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Departament).filter((Departament.chief == current_user.id) | (current_user.id == 1),
                                               Departament.id == id).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/users_show/<int:user_id>', methods=['GET'])
def show_city(user_id):
    user = get(f'http://localhost:5000/api/users/{user_id}').json()
    if user:
        user_coords = get_coords(user['user']['city_from'])
        user_coords = ','.join(user_coords.split())
        draw_map(user_coords)
        return render_template('show_city.html', name=user['user']['name'], surname=user['user']['surname'],
                               city=user['user']['city_from'])
    else:
        abort(404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Почта уже зарегистрирована")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
