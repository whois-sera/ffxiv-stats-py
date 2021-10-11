from app import db
from sqlalchemy import PrimaryKeyConstraint
from dataclasses import dataclass

@dataclass
class Role(db.Model):

    Job: str
    Role: str
    Meta_role: str

    Job = db.Column(db.String(10), primary_key=True)
    Role = db.Column(db.String(10), primary_key=True)
    Meta_role = db.Column(db.String(10))
    PrimaryKeyConstraint('job', 'role', name='role_pk')

    def __repr__(self):
        return f"Role {self.id}"
