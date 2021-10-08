from app import db

class Encounter(db.Model):
    """"""

    id = db.Column(db.Integer, primary_key=True)
    encId = db.Column(db.String(64), index=True, unique=True)
    nom = db.Column(db.String(120))
    duration = db.Column(db.String(120))
    
    def __repr__(self):
        return f"Encounter {self.id}"