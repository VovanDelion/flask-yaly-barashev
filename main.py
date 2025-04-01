from flask import *
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from data.db_session import create_session, global_init
from data.users import User
from data.jobs import Jobs
from forms.users import LoginForm, RegisterForm
from forms.jobs import JobsCreateForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user(uid):
    return create_session().query(User).get(uid)


@app.route('/')
@app.route('/jobs_list')
def jobs_list():
    sess = create_session()
    jobs = sess.query(Jobs).all()
    return render_template('jobs_list.html', title='Список работ',
                           jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = create_session()
        user = sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        sess = create_session()
        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password.data)

        sess.add(user)
        sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create', methods=['GET', 'POST'])
@login_required
def jobs_create():
    form = JobsCreateForm()
    msg = ""
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.name.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        sess = create_session()
        sess.add(job)
        sess.commit()
        msg = "Успешно!"
        return redirect("/jobs_list")
    return render_template("jobs_create.html", title="Добавить работу",
                           message=msg,
                           form=form)


global_init("db/database.sqlite")
app.run('localhost', 8080, debug=True)