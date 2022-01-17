"""create posts table

Revision ID: df9edc7db9a4
Revises: 
Create Date: 2022-01-16 00:38:40.315425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df9edc7db9a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('social_media_posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title',sa.String(),nullable=False)    
    )

    pass


def downgrade():
    op.drop_table("social_media_posts")
    pass
