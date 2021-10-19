from flask import jsonify, render_template
from app.main import bp
from app.models.role import Role
from app.models.log_entry import LogEntry
from app import db
import pandas as pandas
import json
import plotly
import plotly.express as px
from app.main.graph_maker import oneStatAllJobsGraph, oneStatAllJobOfRoleGraph, oneStatOneJobGraph, getJsonVersion
import os

imgPath = os.path.join(os.path.dirname(__file__), "static/images")


@bp.route("/<stat>")
def index(stat):
    """Render a view that display graphs of mean DPS and HPS for each job, sort by role"""

    # Get datas from DB
    logs = pandas.read_sql(LogEntry.query
                           .join(Role, (Role.Job == LogEntry.Job))
                           .with_entities(LogEntry.Job, getattr(LogEntry,stat), Role.Role)
                           .filter(LogEntry.Ally.like("T"))
                           .filter(LogEntry.Job.notlike("0"))
                           .statement,
                           con=db.engine)

    fig = getJsonVersion(oneStatAllJobsGraph(logs, stat))

    return fig


@bp.route("/role/<stat>/<role>")
def graph_role(stat, role):
    """Render a view that display graphs of mean EncDPS and EncHps for each job of a given role"""

    logs = pandas.read_sql(LogEntry.query
                           .join(Role, (Role.Job == LogEntry.Job))
                           .filter(Role.Role.like(role))
                           .order_by(LogEntry.Job)
                           .statement, con=db.engine)

    fig = getJsonVersion(oneStatAllJobOfRoleGraph(logs, stat))

    return fig

@bp.route("/job/<job>")
def graph_job(job):
    """Render a view that display graphs of mean EncDPS and EncHPS for a given job"""

    logs = pandas.read_sql(LogEntry.query
                           .filter(LogEntry.Job.like(job))
                           .statement, con=db.engine)

    fig = getJsonVersion(oneStatOneJobGraph(logs, "EncDPS"))

    return fig


@bp.route("/player/<player>/<job>")
def undef(player, job):
    """"""

    pass
