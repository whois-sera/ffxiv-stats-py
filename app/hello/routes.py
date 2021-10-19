from flask import render_template, jsonify
from app.hello import bp

@bp.route("/hello")
def hello():
    """"""

    return jsonify("I'm Up")
