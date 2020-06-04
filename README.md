# DailyBlog
DailyBlog - A personal blog website using Flask, PostgreSQL, Flask-SQLAlchemy

Windows Powershell:

> $env:FLASK_APP = "run.py"

> $env:FLASK_DEBUG = 1

> $env:FLASK_ENV = "development"

> python -m flask run
OR
> flask run


Windows Command Line:

> $set FLASK_APP="app.py"

> $set FLASK_DEBUG=1

> $set FLASK_ENV=development

> python -m flask run
OR
> flask run


Macintosh Terminal:

> export FLASK_APP=app.py

> export FLASK_ENV=development

> export FLASK_DEBUG=1

> python -m flask run
OR
> flask run

$env:FLASK_APP = "app.py"

$env:FLASK_DEBUG = 1

$env:FLASK_ENV = "development"


DATABASE_URL="postgresql://<user>:<password>@localhost:5432/<db_name>"
