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
