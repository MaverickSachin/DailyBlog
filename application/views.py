from flask import render_template, flash, redirect, url_for
from application.forms import SignUpForm, LogInForm
from .models import User, Post
from flask import current_app as app


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
@app.route("/index/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('index'))
    return render_template("signup.html", form=form)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        if form.email.data == "MaverickSachin@gmail.com" and form.password.data == "password123":
            flash("You have been logged in!", "success")
            return redirect(url_for('index'))
        else:
            flash("Login unsuccessful. Please check username and password.", "danger")

    return render_template("login.html", form=form)