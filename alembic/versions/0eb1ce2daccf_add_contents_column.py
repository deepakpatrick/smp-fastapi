"""add contents column

Revision ID: 0eb1ce2daccf
Revises: df9edc7db9a4
Create Date: 2022-01-16 00:50:48.899861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eb1ce2daccf'
down_revision = 'df9edc7db9a4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('social_media_posts', sa.Column('contents',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('social_media_posts','contents')
    pass
