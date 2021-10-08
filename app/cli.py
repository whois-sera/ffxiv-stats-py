import os
import click
import pandas
from dotenv import load_dotenv

def register(app):
    @app.cli.group()
    def xml():
        """Commands relative to ACT xml files"""

        pass

    @xml.command()
    def import_log():
        """Import ACT logs to sql"""

        pass

    @xml.command()
    def testpath():
        """Show abspath of cli.py file"""

        rootdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        act_files_dir = os.path.join(rootdir, os.environ.get("ACT_FILES_DIR"))
        if os.path.isdir(act_files_dir):
            pass
        else:
            print(f"{act_files_dir} directory does not exist")