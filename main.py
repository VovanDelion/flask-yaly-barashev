from flask import redirect, url_for, flash, render_template, abort, request, Flask
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session, global_init
from data.users import User
from data.jobs import Jobs, Department, Category
from forms.users import LoginForm, RegisterForm
from forms.jobs import JobsCreateForm
from forms.departments import DepartmentForm
from api.jobs import blueprint as jobs_blueprint

from api.users_resource import UsersResource, UsersListResource
from api.jobs_resource import JobsResource, JobsListResource


app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "my secret key"
app.register_blueprint(jobs_blueprint)
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


@app.route('/jobs/create', methods=['GET', 'POST'])
@login_required
def create_job():
    form = JobsCreateForm()
    form.categories.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        job = Jobs()
        for cat_id in form.categories.data:
            category = Category.query.get(cat_id)
            job.categories.append(category)

        db.session.add(job)
        db.session.commit()
        flash('Работа создана', 'success')
        return redirect(url_for('jobs_list'))

    return render_template('jobs_create.html', form=form)


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    if current_user.id != job.team_leader and current_user.id != 1:
        abort(403)

    form = JobsCreateForm()

    if form.validate_on_submit():
        job.job = form.name.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        db.session.commit()
        flash('Работа успешно обновлена', 'success')
        return redirect(url_for('jobs_list'))

    if request.method == 'GET':
        form.name.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished

    return render_template('jobs_create.html',
                           title='Редактирование работы',
                           form=form)


@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    if current_user.id != job.team_leader and current_user.id != 1:
        flash('У вас нет прав для удаления этой работы', 'danger')
        return redirect(url_for('jobs_list'))

    try:
        db.session.delete(job)
        db.session.commit()
        flash('Работа успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении работы', 'danger')

    return redirect(url_for('jobs_list'))


@app.route('/departments')
def departments_list():
    deps = db.session.query(Department).all()
    return render_template('departments_list.html', departments=deps)


@app.route('/departments/create', methods=['GET', 'POST'])
@login_required
def create_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db.session.add(dep)
        db.session.commit()
        flash('Департамент создан', 'success')
        return redirect(url_for('departments_list'))
    return render_template('department_edit.html', form=form, title='Создание департамента')


@app.route('/departments/edit/<int:dep_id>', methods=['GET', 'POST'])
@login_required
def edit_department(dep_id):
    dep = Department.query.get_or_404(dep_id)
    if current_user.id != dep.chief and current_user.id != 1:
        abort(403)

    form = DepartmentForm()
    if form.validate_on_submit():
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('departments_list'))

    if request.method == 'GET':
        form.title.data = dep.title
        form.chief.data = dep.chief
        form.members.data = dep.members
        form.email.data = dep.email

    return render_template('department_edit.html', form=form, title='Редактирование департамента')


@app.route('/departments/delete/<int:dep_id>', methods=['POST'])
@login_required
def delete_department(dep_id):
    dep = Department.query.get_or_404(dep_id)
    if current_user.id != dep.chief and current_user.id != 1:
        abort(403)

    db.session.delete(dep)
    db.session.commit()
    flash('Департамент удален', 'success')
    return redirect(url_for('departments_list'))


api.add_resource(UsersListResource, '/api/v2/users')

api.add_resource(UsersResource, '/api/v2/users/<int:news_id>')

api.add_resource(JobsListResource, '/api/v2/jobs')
api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')

global_init("db/database.sqlite")
app.run('localhost', 8080, debug=True)