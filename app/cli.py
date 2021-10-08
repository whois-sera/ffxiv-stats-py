import os
import click

def register(app):
    @app.cli.group()
    def xml():
        """Commands relative to ACT xml files"""

        pass

    def import_log():
        """Import ACT logs to sql"""

        pass