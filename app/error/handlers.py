from flask import render_template
from app import db
from app.error import bp

@bp.errorhandler(404)
def not_found_error(error):
    """Overide default 404 error page"""

    return render_template("error/404.html"), 404


@bp.errorhandler(500)
def internal_error(error):
    """Overide default 500 error page"""

    return render_template("error/500.html"), 500