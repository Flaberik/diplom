from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, current_user, login_required

from app import app
from app import db, oid
from app.forms import *
from app.models import User, ROLE_USER


# ---------------------------------------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])


# ---------------------------------------------------------------------#
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


# ---------------------------------------------------------------------#
@app.before_request
def before_request():
    g.user = current_user


# ---------------------------------------------------------------------#
@app.route('/signup', methods=['GET', 'POST'])
def signin():
    form = SignUp()

    if form.validate_on_submit():
        if str(form.pass_one.data) == str(form.pass_two.data):
            flash('registration complite')
            return redirect('/index')
    return render_template('signup.html', title='Sign Up', form=form)


# ---------------------------------------------------------------------#
@app.route('/')
@app.route('/index')
def index():
    user = g.user

    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template("index.html", title="home", posts=posts, user=user)
