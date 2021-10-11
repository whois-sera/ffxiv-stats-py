from app import db
from dataclasses import dataclass


@dataclass
class LogEntry(db.Model):
    """"""

    id: str
    EncId: str
    Ally: str
    Name: str
    StartTime: str
    EndTime: str
    Duration: str
    Damage: int
    DamagePerc: float
    Kills: int
    Healed: int
    HealedPerc: float
    CritHeals: int
    Heals: int
    CureDispels: int
    PowerDrain: int
    PowerReplenish: int
    DPS: float
    EncDPS: float
    EncHPS: float
    Hits: int
    CritHits: int
    Blocked: int
    Misses: int
    Swings: int
    HealsTaken: int
    DamageTaken: int
    Deaths: int
    ToHit: float
    CritDamPerc: float
    CritHealPerc: float
    CritTypes: str
    ThreatStr: str
    ThreatDelta: int
    Job: str
    ParryPct: float
    BlockPct: float
    IncToHit: float
    OverHealPct: float
    DirectHitPct: float
    DirectHitCount: int
    CritDirectHitCount: int
    CritDirectHitPct: float

    id = db.Column(db.Integer, primary_key=True)
    EncId = db.Column(db.String(64), nullable=False)
    Ally = db.Column(db.String(64), nullable=False)
    Name = db.Column(db.String(64), nullable=False)
    StartTime = db.Column(db.String(64), nullable=False)
    EndTime = db.Column(db.String(64), nullable=False)
    Duration = db.Column(db.String(64), nullable=False)
    Damage = db.Column(db.Integer, nullable=False)
    DamagePerc = db.Column(db.Float(), nullable=False)
    Kills = db.Column(db.Integer, nullable=False)
    Healed = db.Column(db.Integer, nullable=False)
    HealedPerc = db.Column(db.Float(), nullable=False)
    CritHeals = db.Column(db.Integer, nullable=False)
    Heals = db.Column(db.Integer, nullable=False)
    CureDispels = db.Column(db.Integer, nullable=False)
    PowerDrain = db.Column(db.Integer, nullable=False)
    PowerReplenish = db.Column(db.Integer, nullable=False)
    DPS = db.Column(db.Float(), nullable=False)
    EncDPS = db.Column(db.Float(), nullable=False)
    EncHPS = db.Column(db.Float(), nullable=False)
    Hits = db.Column(db.Integer, nullable=False)
    CritHits = db.Column(db.Integer, nullable=False)
    Blocked = db.Column(db.Integer, nullable=False)
    Misses = db.Column(db.Integer, nullable=False)
    Swings = db.Column(db.Integer, nullable=False)
    HealsTaken = db.Column(db.Integer, nullable=False)
    DamageTaken = db.Column(db.Integer, nullable=False)
    Deaths = db.Column(db.Integer, nullable=False)
    ToHit = db.Column(db.Float(), nullable=False)
    CritDamPerc = db.Column(db.Float(), nullable=False)
    CritHealPerc = db.Column(db.Float(), nullable=False)
    CritTypes = db.Column(db.String(64), nullable=False)
    ThreatStr = db.Column(db.String(64), nullable=False)
    ThreatDelta = db.Column(db.Integer, nullable=False)
    Job = db.Column(db.String(64), nullable=False)
    ParryPct = db.Column(db.Float(), nullable=False)
    BlockPct = db.Column(db.Float(), nullable=False)
    IncToHit = db.Column(db.Float(), nullable=False)
    OverHealPct = db.Column(db.Float(), nullable=False)
    DirectHitPct = db.Column(db.Float(), nullable=False)
    DirectHitCount = db.Column(db.Integer, nullable=False)
    CritDirectHitCount = db.Column(db.Integer, nullable=False)
    CritDirectHitPct = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"LogEntry {self.id}"
