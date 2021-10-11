from flask import jsonify, render_template
from app.main import bp
from app.models.role import Role
from app.models.log_entry import LogEntry
from app import db
import pandas as pandas
import json
import plotly
import plotly.express as px


@bp.route("/")
@bp.route("/home")
def index():
    """"""

    jobs = Role.query.with_entities(Role.Job).all()
    return jsonify(jobs)


@bp.route("/role/<role>")
def graph_role(role):
    """Display a graph that compare mean of EncDPS for each job of a given role"""

    logs = pandas.read_sql(LogEntry.query.join(Role, (Role.Job == LogEntry.Job))
                           .filter(Role.Role.like(role))
                           .order_by(LogEntry.Job)
                           .statement, con=db.engine)
    logs = logs[["Job", "EncDPS"]].groupby("Job").mean()
    fig = px.bar(logs, x=logs.index, y="EncDPS")
    figJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("main/role.html", figJson=figJson, role=role)


@bp.route("/job/<job>")
def test(job):
    """"""

    logs = pandas.read_sql(LogEntry.query
                           .filter(LogEntry.Job.like(job))
                           .statement, con=db.engine)
    logs = logs[["EncId", "EncDPS", "EncHPS"]]
    fig = px.line(logs, x="EncId", y="EncDPS")
    figJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("main/job.html", figJson=figJson, job=job)
