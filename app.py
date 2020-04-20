from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
