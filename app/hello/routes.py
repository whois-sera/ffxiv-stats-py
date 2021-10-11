from flask import render_template
from app.hello import bp

@bp.route("/hello")
def hello():
    """"""

    return render_template("hello/hello.html")
