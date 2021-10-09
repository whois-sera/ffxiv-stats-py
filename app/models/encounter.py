from app import db

class Encounter(db.Model):
    """"""

    id = db.Column(db.Integer, primary_key=True)
    EncId = db.Column(db.String(64), index=True, unique=True)
    
    def __repr__(self):
        return f"Encounter {self.id}"