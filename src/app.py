from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import config
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from models.ModelUser import ModelUser

from src.models.entities.users import User

app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return render_template('presentation.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Invalid password..')
                return render_template('auth/login.html')
        else:
            flash('User not found....')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'], request.form['fullname'])
        account = ModelUser.check_user(db, request.form['username'])
        if account:
            flash('El usuario existe')
        elif not request.form['username'] or not request.form['password'] or not request.form['fullname']:
            flash('no puede estar vacio')
        else:
            ModelUser.register(db, user)
            flash('Registed')
            return redirect(url_for('register'))
    return render_template('auth/register.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/protected')
@login_required
def protected():
    return "<h1> Esta es una vista protegida solo para usuarios loggeados</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return 'No se ha encontrado la pagina'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
