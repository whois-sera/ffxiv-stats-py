from app import create_app, db
from app.models.encounter import Encounter
from app.models.log_entry import LogEntry
from app.models.role import Role
from app import cli

app = create_app()  # Create the app after importing necessary elements like models
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    """Make some elements available in flask shell"""

    return {"db": db, "Encounter": Encounter, "LogEntry": LogEntry, "Role": Role}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
