import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from application.forms import SignUpForm, LogInForm, UpdateAccountForm
from application.models import User, Post
from flask import current_app as app
from application import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Steve Smith',
        'title': 'Blog Post 01',
        'content': 'First post content',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'David Warner',
        'title': 'Blog Post 02',
        'content': 'Second post content',
        'date_posted': 'April 21, 2020'
    }
]


@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in.", 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", title='SignUp', form=form)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")

    return render_template("login.html", title='LogIn', form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


@app.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.", 'success')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template("account.html", title="Account", image_file=image_file, form=form)
