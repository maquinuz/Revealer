"""add presentation model

Revision ID: 567a823467d9
Revises: 4b54d3611475
Create Date: 2016-03-25 10:37:31.741742

"""

# revision identifiers, used by Alembic.
revision = '567a823467d9'
down_revision = '4b54d3611475'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('presentation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slideshow_hash', sa.String(length=12), nullable=True),
    sa.Column('slideshow_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['slideshow_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slideshow_hash')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('presentation')
    ### end Alembic commands ###
