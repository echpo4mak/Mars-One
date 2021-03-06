from flask import Flask
from flask import render_template, redirect, request, abort, url_for
from data import db_session
from flask_login import LoginManager
from data.jobs import Jobs
from data.users import User
from data.departments import Department
# from data.users_resource import UsersResource, UsersListResource
# from data.jobs_resource import JobsResource, JobsListResource
from data.forms import LoginForm, RegisterForm, JobForm, DepartmentForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Api
from requests import get
import user_api
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


# api.add_resource(UsersListResource, '/api/v2/users')
# api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
# api.add_resource(JobsResource, '/api/v2/jobs')
# api.add_resource(JobsListResource, '/api/v2/jobs/<int:job_id>')

def get_object_size(geo_object):
    lower_corner = list(map(float, geo_object['boundedBy']['Envelope']['lowerCorner'].split()))
    upper_corner = list(map(float, geo_object['boundedBy']['Envelope']['upperCorner'].split()))
    return (str(abs(lower_corner[0] - upper_corner[0]) / 2),
            str(abs(lower_corner[1] - upper_corner[1]) / 2))


@app.route("/")
def job_index():
    session = db_session.create_session()
    if current_user.is_authenticated:
        jobs = session.query(Jobs).filter(Jobs.is_finished.is_(False))
    else:
        jobs = session.query(Jobs).filter(Jobs.is_finished.is_(True))
    return render_template("index.html", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.categories.type = form.category.data
        jobs.is_finished = form.is_job_finished.data
        current_user.jobs.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter((Jobs.id == id)).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.categories.type = form.category.data
            jobs.is_finished = form.is_job_finished.data
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter((Jobs.id == id)).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.categories.type = form.category.data
            jobs.is_finished = form.is_job_finished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html', title='Редактирование работы', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments_index")
def departments_index():
    session = db_session.create_session()
    departments = session.query(Department).all()
    return render_template("departments_index.html", departments=departments)


@app.route('/departments', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        current_user.departments.append(department)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('departments.html', title='Добавление департамента',
                           form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        department = session.query(Department).filter((Department.id == id)).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        department = session.query(Department).filter((Department.id == id)).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('departments.html', title='Редактирование департамента', form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    session = db_session.create_session()
    department = session.query(Department).filter((Department.id == id)).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/users_show/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users_show(user_id):
    response = get(f'http://localhost:5000/api/users/{user_id}').json()
    print(response)
    toponym_to_find = response["users"]["address"]
    print(toponym_to_find)

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = get_object_size(toponym)

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        'll': ','.join([toponym_longitude, toponym_lattitude]),
        'spn': ",".join([delta[0], delta[1]]),
        'l': 'sat',
        'pt': ','.join([toponym_longitude, toponym_lattitude, 'flag'])
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    map_file = "static/img/map.png"
    with open(map_file, "wb") as f:
        f.write(response.content)
    return render_template('users_show.html', title='Nostalgy', url_nostalgy=url_for('static', filename='img/map.png'))


def main():
    db_session.global_init("db/mars_explore.sqlite")
    app.register_blueprint(user_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
