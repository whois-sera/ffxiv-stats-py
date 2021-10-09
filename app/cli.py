import os
import click
import pandas as pandas
import lxml
from dotenv import load_dotenv
from app import db
from app.models.log_entry import LogEntry
from app.models.encounter import Encounter

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
            db.session.commit()
            
            for filename in os.listdir(act_files_dir):
                filepath = os.path.join(act_files_dir, filename)

                logs = pandas.read_xml(filepath)

                logs["DamagePerc"] = logs["DamagePerc"].str.strip("%")
                logs["HealedPerc"] = logs["DamagePerc"].str.strip("%")
                logs["CritDamPerc"] = logs["CritDamPerc"].str.strip("%")
                logs["CritHealPerc"] = logs["CritHealPerc"].str.strip("%")
                logs["ParryPct"] = logs["ParryPct"].str.strip("%")
                logs["BlockPct"] = logs["BlockPct"].str.strip("%")
                logs["OverHealPct"] = logs["OverHealPct"].str.strip("%")
                logs["DirectHitPct"] = logs["DirectHitPct"].str.strip("%")
                logs["CritDirectHitPct"] = logs["CritDirectHitPct"].str.strip("%")

                logs.to_sql("log_entry", con=db.engine, if_exists="append", index=False, method="multi")

            encounters = pandas.read_sql(db.session.query(LogEntry.EncId).distinct().statement, con=db.engine)
            encounters.to_sql("encounter", con=db.engine, if_exists="append", index=False, method="multi")

        else:
            print(f"{act_files_dir} directory does not exist")