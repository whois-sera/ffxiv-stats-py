"""empty message

Revision ID: b27a9cac48fd
Revises: 
Create Date: 2021-10-08 13:37:47.373063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b27a9cac48fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('encounter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encId', sa.String(length=64), nullable=True),
    sa.Column('nom', sa.String(length=120), nullable=True),
    sa.Column('duration', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_encounter_encId'), 'encounter', ['encId'], unique=True)
    op.create_table('log_entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encId', sa.String(length=64), nullable=True),
    sa.Column('ally', sa.String(length=64), nullable=True),
    sa.Column('nom', sa.String(length=64), nullable=True),
    sa.Column('startTime', sa.DateTime(), nullable=True),
    sa.Column('endTime', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.String(length=64), nullable=True),
    sa.Column('damage', sa.Integer(), nullable=True),
    sa.Column('damagePerc', sa.Integer(), nullable=True),
    sa.Column('kills', sa.Integer(), nullable=True),
    sa.Column('healed', sa.Integer(), nullable=True),
    sa.Column('healedPerc', sa.Integer(), nullable=True),
    sa.Column('critHeals', sa.Integer(), nullable=True),
    sa.Column('heals', sa.Integer(), nullable=True),
    sa.Column('cureDisplels', sa.Integer(), nullable=True),
    sa.Column('powerDrain', sa.Integer(), nullable=True),
    sa.Column('powerReplanish', sa.Integer(), nullable=True),
    sa.Column('dps', sa.Float(), nullable=True),
    sa.Column('encDps', sa.Float(), nullable=True),
    sa.Column('encHps', sa.Float(), nullable=True),
    sa.Column('hits', sa.Integer(), nullable=True),
    sa.Column('critHits', sa.Integer(), nullable=True),
    sa.Column('blocked', sa.Integer(), nullable=True),
    sa.Column('misses', sa.Integer(), nullable=True),
    sa.Column('swings', sa.Integer(), nullable=True),
    sa.Column('healTaken', sa.Integer(), nullable=True),
    sa.Column('damageTaken', sa.Integer(), nullable=True),
    sa.Column('death', sa.Integer(), nullable=True),
    sa.Column('toHit', sa.Float(), nullable=True),
    sa.Column('critDamagePerc', sa.Integer(), nullable=True),
    sa.Column('critHealPerc', sa.Integer(), nullable=True),
    sa.Column('critTypes', sa.String(length=64), nullable=True),
    sa.Column('threatStr', sa.String(length=64), nullable=True),
    sa.Column('threatDelta', sa.Integer(), nullable=True),
    sa.Column('job', sa.String(length=64), nullable=True),
    sa.Column('ParryPct', sa.Integer(), nullable=True),
    sa.Column('BlockPct', sa.Integer(), nullable=True),
    sa.Column('IncToHit', sa.Float(), nullable=True),
    sa.Column('DirectHitPct', sa.Integer(), nullable=True),
    sa.Column('DirectHitCount', sa.Integer(), nullable=True),
    sa.Column('CritDirectHitCount', sa.Integer(), nullable=True),
    sa.Column('CritDirectHitPct', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log_entry')
    op.drop_index(op.f('ix_encounter_encId'), table_name='encounter')
    op.drop_table('encounter')
    # ### end Alembic commands ###