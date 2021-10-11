import os
import click
import pandas as pandas
import lxml
from dotenv import load_dotenv
from app import db
from app.models.log_entry import LogEntry
from app.models.encounter import Encounter
from app.models.role import Role
import numpy as np


def register(app):
    @app.cli.group()
    def xml():
        """Commands relative to ACT xml files"""

        pass

    @xml.command()
    def logimport():
        """Import all logs from ACT files folder into an sql db, replacing the whole content"""

        rootdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        act_files_dir = os.path.join(rootdir, os.environ.get("ACT_FILES_DIR"))
        if os.path.isdir(act_files_dir):

            db.session.query(LogEntry).delete()
            db.session.query(Encounter).delete()
            db.session.query(Role).delete()
            db.session.commit()

            for filename in os.listdir(act_files_dir):
                filepath = os.path.join(act_files_dir, filename)

                logs = pandas.read_xml(filepath)

                logs["DamagePerc"] = logs["DamagePerc"]\
                    .str.strip("%")
                logs["HealedPerc"] = logs["DamagePerc"]\
                    .str.strip("%")
                logs["CritDamPerc"] = logs["CritDamPerc"]\
                    .str.strip("%")
                logs["CritHealPerc"] = logs["CritHealPerc"]\
                    .str.strip("%")
                logs["ParryPct"] = logs["ParryPct"]\
                    .str.strip("%")
                logs["BlockPct"] = logs["BlockPct"]\
                    .str.strip("%")
                logs["OverHealPct"] = logs["OverHealPct"]\
                    .str.strip("%")
                logs["DirectHitPct"] = logs["DirectHitPct"]\
                    .str.strip("%")
                logs["CritDirectHitPct"] = logs["CritDirectHitPct"]\
                    .str.strip("%")

                logs = logs.replace(to_replace="YOU", value="Naaru Segawa",
                                    inplace=False, limit=None, regex=False)
                logs = logs.replace(to_replace="--", value="-",
                                    inplace=False, limit=None, regex=False)
                logs = logs.replace(to_replace=np.nan, value=0,
                                    inplace=False, limit=None, regex=False)
                logs = logs.replace(to_replace="--", value=0,
                                    inplace=False, limit=None, regex=False)
                logs = logs.replace(to_replace="-", value=0,
                                    inplace=False, limit=None, regex=False)
                logs = logs.replace(to_replace="∞", value=0,
                                    inplace=False, limit=None, regex=False)

                logs.to_sql("log_entry", con=db.engine,
                            if_exists="append", index=False, method="multi")

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

        else:
            print(f"{act_files_dir} directory does not exist")
