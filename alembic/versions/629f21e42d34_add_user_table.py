"""add user table

Revision ID: 629f21e42d34
Revises: 0eb1ce2daccf
Create Date: 2022-01-16 00:56:50.316678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '629f21e42d34'
down_revision = '0eb1ce2daccf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                   )
    pass


def downgrade():
    op.drop_table('users')
    pass
