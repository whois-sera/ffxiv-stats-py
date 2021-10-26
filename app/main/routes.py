from flask import jsonify, render_template, request
from app.main import bp
from app.models.role import Role
from app.models.log_entry import LogEntry
from app.models.encounter import Encounter
from app import db
import pandas as pandas
import json
import plotly
import plotly.express as px
from app.main.graph_maker import oneStatAllJobsGraph, oneStatAllJobOfRoleGraph, oneStatOneJobGraph, getJsonVersion, playerJobCompare
import os
import numpy as np
import datetime

imgPath = os.path.join(os.path.dirname(__file__), "static/images")
actPath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "act_files")

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

@bp.route("/best/<stat>/<role>/<player>")
def graph_best(stat, role, player):
    """Render a view that display graphs of mean EncDPS and EncHps for each job of a given role"""

    logs = pandas.read_sql(LogEntry.query
                           .join(Role, (Role.Job == LogEntry.Job))
                           .filter(Role.Role.like(role), LogEntry.Name.like(f"%{player}%"))
                           .order_by(LogEntry.Job)
                           .statement, con=db.engine)

    fig = getJsonVersion(oneStatAllJobOfRoleGraph(logs, stat))

    return fig

@bp.route("/job/<stat>/<job>")
def graph_job(stat, job):
    """Render a view that display graphs of mean EncDPS and EncHPS for a given job"""

    logs = pandas.read_sql(LogEntry.query
                           .filter(LogEntry.Job.like(job))
                           .limit(20)
                           .statement, con=db.engine)

    fig = getJsonVersion(oneStatOneJobGraph(logs, stat))

    return fig

@bp.route("/player/<stat>/<job>/<player>")
def graph_player(stat, job, player):
    """Render a view that display graphs of mean EncDPS and EncHPS for a given job"""

    logs = pandas.read_sql(LogEntry.query
                           .filter(LogEntry.Job.like(job), LogEntry.Name.like(f"%{player}%"))
                           .limit(20)
                           .statement, con=db.engine)

    fig = getJsonVersion(oneStatOneJobGraph(logs, stat))

    return fig

@bp.route("/recap/<stat>/<job>/<player>")
def recap(stat, job, player):
    """"""

    logs = pandas.read_sql(LogEntry.query
                           .filter(LogEntry.Job.like(job))
                           .limit(20)
                           .statement, con=db.engine)

    fig = getJsonVersion(playerJobCompare(logs, stat, player))

    return fig


@bp.route("/upload", methods=["POST"])
def upload():
    """"""
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.xml"
    file = request.files['file']
    if file.filename != '':
        file.save(os.path.join(actPath, filename))

    return jsonify(f"File uploaded as {filename}")


@bp.route("/import")
def logimport():
    """Import all logs from ACT files folder into an sql db, replacing the whole content"""

    rootdir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    act_files_dir = os.path.join(rootdir, os.environ.get("ACT_FILES_DIR"))
    if os.path.isdir(act_files_dir):


        file_list = os.listdir(act_files_dir)
        if len(file_list) > 1:

            # db.session.query(LogEntry).delete()
            db.session.query(Encounter).delete()
            db.session.query(Role).delete()
            db.session.commit()

            for filename in os.listdir(act_files_dir):

                if os.path.isfile(os.path.join(act_files_dir, filename)):

                    filepath = os.path.join(act_files_dir, filename)

                    logs = pandas.read_xml(filepath)

                    # Only teamates
                    logs = logs[logs['Ally'] == 'T']

                    logs["CritTypes"] = "0"
                    logs["ThreatStr"] = "0"

                    # Transform "Carbuncle Blue (Naaru Segawa)" into "Naaru Segawa"
                    logs["Name"] = logs["Name"]\
                        .str.replace("Carbuncle Rubis (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.replace("Demi-Phénix (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.replace("Demi-Bahamut (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.replace("Carbuncle Émeraude (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.replace("Estime (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.replace("Ombre (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.replace("Étoile Terrestre (", "", regex=False)
                    logs["Name"] = logs["Name"]\
                        .str.strip(")")

                    # Some text manipulation
                    logs.replace(to_replace="YOU", value="Naaru Segawa",
                                    limit=None, regex=False, inplace=True)
                    logs.replace(to_replace="--", value="0",
                                    limit=None, regex=False, inplace=True)
                    logs.replace(to_replace=np.nan, value=0,
                                    limit=None, regex=False, inplace=True)
                    logs.replace(to_replace="-", value=0,
                                    limit=None, regex=False, inplace=True)
                    logs.replace(to_replace="∞", value=0,
                                    limit=None, regex=False, inplace=True)
                    logs.replace(to_replace="", value=0,
                                    limit=None, regex=False, inplace=True)

                    # Strip "%" and cast to float
                    logs["DamagePerc"] = (logs["DamagePerc"]
                                            .str.strip("%")).astype(float)
                    logs["HealedPerc"] = (logs["HealedPerc"]
                                            .str.strip("%")).astype(float)
                    logs["CritDamPerc"] = (logs["CritDamPerc"]
                                            .str.strip("%")).astype(float)
                    logs["CritHealPerc"] = (logs["CritHealPerc"]
                                            .str.strip("%")).astype(float)
                    logs["ParryPct"] = (logs["ParryPct"]
                                        .str.strip("%")).astype(float)
                    logs["BlockPct"] = (logs["BlockPct"]
                                        .str.strip("%")).astype(float)
                    logs["OverHealPct"] = (logs["OverHealPct"]
                                            .str.strip("%")).astype(float)
                    logs["DirectHitPct"] = (logs["DirectHitPct"]
                                            .str.strip("%")).astype(float)
                    logs["CritDirectHitPct"] = (logs["CritDirectHitPct"]
                                                .str.strip("%")).astype(float)

                    logs["Job"] = logs["Job"].astype(str)

                    logs["DPS"] = logs["DPS"].astype(float)

                    logs = logs.groupby('Name', as_index=False)\
                        .agg({
                            "EncId": "first", "Ally": "first", "StartTime": "min", "EndTime": "max",
                            "Duration": "max", "CritTypes": "first", "ThreatStr": "first", "Job": "max", "Damage": "sum",
                            "DamagePerc": "sum", "Kills": "sum", "Healed": "sum",  "HealedPerc": "sum", "CritHeals": "sum",
                            "Heals": "sum", "CureDispels": "sum", "PowerDrain": "sum", "PowerReplenish": "sum", "DPS": "sum",
                            "EncDPS": "sum", "EncHPS": "sum", "Hits": "sum", "CritHits": "sum", "Blocked": "sum",
                            "Misses": "sum", "Swings": "sum", "HealsTaken": "sum", "DamageTaken": "sum", "Deaths": "sum",
                            "ToHit": "sum", "CritDamPerc": "sum", "CritHealPerc": "sum", "ThreatDelta": "sum", "ParryPct": "sum",
                            "BlockPct": "sum", "IncToHit": "sum", "OverHealPct": "sum", "DirectHitPct": "sum", "DirectHitCount": "sum",
                            "CritDirectHitCount": "sum", "CritDirectHitPct": "sum"
                        })

                    logs.to_sql("log_entry", con=db.engine,
                                if_exists="append", index=False, method="multi")
                    
                    os.rename(filepath, os.path.join(act_files_dir, "added", filename))

            encounters = pandas.read_sql(db.session.query(LogEntry.EncId)
                                            .distinct()
                                            .statement, con=db.engine)

            encounters.to_sql("encounter", con=db.engine,
                                if_exists="append", index=False, method="multi")

            roles = pandas.DataFrame(
                {
                    "Job": [
                        "Pld", "War", "Drk", "Gnb", "Whm", "Ast", "Sch", "Mnk", "Sam",
                        "Drg", "Nin", "Brd", "Dnc", "Mch", "Rdm", "Blm", "Smn", "Blu",
                    ],
                    "Role": [
                        "Tank", "Tank", "Tank", "Tank", "Healer", "Healer", "Healer", "Melee", "Melee",
                        "Melee", "Melee", "Ranged", "Ranged", "Ranged", "Mage", "Mage", "Mage", "Mage",
                    ],
                    "Meta_role": [
                        "Tank", "Tank", "Tank", "Tank", "Healer", "Healer", "Healer", "DPS", "DPS",
                        "DPS", "DPS", "DPS", "DPS", "DPS", "DPS", "DPS", "DPS", "DPS",
                    ],
                }
            )

            roles.to_sql("role", con=db.engine, if_exists="append",
                            index=False, method="multi")
            
            return jsonify("Import terminé")

        else:
            return jsonify("Aucun fichier en attente d'import")

    else:
        return jsonify(f"{act_files_dir} directory does not exist")


@bp.route("/infos")
def infos():
    number_of_logEntry = LogEntry.query.count()

    rootdir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    act_files_dir = os.path.join(rootdir, os.environ.get("ACT_FILES_DIR"))
    act_added_files_dir = os.path.join(rootdir, os.environ.get("ACT_FILES_DIR"), "added")

    if os.path.isdir(act_added_files_dir):
        file_list = os.listdir(act_added_files_dir)
        number_of_files = len(file_list)
    else:
        number_of_files = "Répertoir non toruvé"

    if os.path.isdir(act_files_dir):
        file_list = os.listdir(act_files_dir)
        if len(file_list) > 1:
            number_of_waiting_files = len(file_list) - 1
        else:
            number_of_waiting_files = 0

    return jsonify({"number_of_logEntry":number_of_logEntry,
                    "number_of_files":number_of_files,
                    "number_of_waiting_files":number_of_waiting_files,
                    })