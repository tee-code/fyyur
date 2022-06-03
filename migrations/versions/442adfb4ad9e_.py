"""empty message

Revision ID: 442adfb4ad9e
Revises: b141bf31d371
Create Date: 2022-06-03 14:00:00.843618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '442adfb4ad9e'
down_revision = 'b141bf31d371'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('Artist', 'seeking_talent')
    op.add_column('Venue', sa.Column('seeking_artist', sa.Boolean(), nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_artist')
    op.add_column('Artist', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###