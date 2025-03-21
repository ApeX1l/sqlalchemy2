from flask import Flask, make_response, request, session, redirect, render_template, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.login import LoginForm
from forms.news import JobForm
from forms.register import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'sqlalchemy_second'


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    # user = User()
    # user.surname = 'Scott'
    # user.name = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = 'research engineer'
    # user.address = 'module_1'
    # user.email = "scott_chief@mars.org"
    # db_sess.add(user)
    #
    # user = User()
    # user.surname = 'Ильин'
    # user.name = "Дмитрий"
    # user.age = 17
    # user.position = "лейтенант"
    # user.speciality = 'инженер'
    # user.address = 'module_2'
    # user.email = "example1@email.com"
    # db_sess.add(user)
    #
    # user = User()
    # user.surname = 'Петров'
    # user.name = "Олег"
    # user.age = 53
    # user.position = "капитан"
    # user.speciality = 'штурман'
    # user.address = 'module_3'
    # user.email = "module3@yandex.ru"
    # db_sess.add(user)
    #
    # user = User()
    # user.surname = 'Олегов'
    # user.name = "Петр"
    # user.age = 35
    # user.position = "майор"
    # user.speciality = '2-ой штурман'
    # user.address = 'module_4'
    # user.email = "petr_olegov@google.com"
    # db_sess.add(user)

    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Первая новость", content="Первая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    #
    # user = db_sess.query(User).filter(User.id == 2).first()
    # news = News(title="Вторая новость", content="Уже вторая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    #
    # user = db_sess.query(User).filter(User.id == 3).first()
    # news = News(title="Третья новость", content="Уже третья запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    #
    # user = db_sess.query(User).filter(User.id == 4).first()
    # news = News(title="Четвертая новость", content="Уже четвертая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    #
    # db_sess.commit()

    # user = db_sess.query(User).filter(User.id == 5).first()
    # news = News(title="Моя новость", content="Первая запись ilind",
    #             user=user, is_private=False)
    # db_sess.add(news)
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     news = db_sess.query(Jobs).filter(Jobs.user_job == current_user)
    # else:
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
            email=form.email.data
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


if __name__ == '__main__':
    main()
