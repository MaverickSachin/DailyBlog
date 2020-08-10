# DailyBlog
DailyBlog - A personal blog website using Flask, PostgreSQL, Flask-SQLAlchemy, Bootstrap

Windows Powershell:

> $env:FLASK_APP = "run.py"

> $env:FLASK_DEBUG = 1

> $env:FLASK_ENV = "development"

> python -m flask run

> flask run


Windows Command Line:

> $set FLASK_APP="app.py"

>> $set FLASK_DEBUG=1
>
> $set FLASK_ENV=development

> python -m flask run

> flask run


Macintosh Terminal:

> export FLASK_APP=app.py

> export FLASK_ENV=development

> export FLASK_DEBUG=1

> python -m flask run

> flask run

DATABASE_URL="postgresql://<user>:<password>@localhost:5432/<db_name>"

------------

# .env file content

SECRET_KEY="c91831ff9038a0061609c0889d462d21"

FLASK_APP="run.py"

FLASK_DEBUG=1

FLASK_ENV="development"

SQLALCHEMY_DATABASE_URI="postgresql://<user>:<password>@localhost:5432/<database>"

MAIL_SERVER="smtp.googlemail.com"

EMAIL_USER="<gmail_address>"

EMAIL_PASS="<gmail_password>"
