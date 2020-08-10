from flask import render_template, flash, redirect, url_for, request, Blueprint
from application.users.forms import (
    SignUpForm,
    LogInForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm
)
from .models import User
from application.posts.models import Post
from application import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from application.users.utils import send_reset_email, save_picture


users = Blueprint('users', __name__)


@users.route("/signup/", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in.", 'success')
        return redirect(url_for('users.login'))
    return render_template("users/signup.html", title='SignUp', form=form)


@users.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")

    return render_template("users/login.html", title='LogIn', form=form)


@users.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account/", methods=["GET", "POST"])
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

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=f'images/profile_pictures/{current_user.image_file}')
    return render_template("users/account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>/")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template("users/user_posts.html", user=user, posts=posts)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))

    return render_template("users/reset_request.html", title='Reset Password', form=form)


@users.route("/reset_password/<token>/", methods=["GET", "POST"])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token.", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated! You are now able to log in.", 'success')
        return redirect(url_for('users.login'))

    return render_template("users/reset_token.html", title="Reset Password", form=form)
