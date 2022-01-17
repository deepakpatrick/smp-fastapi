"""add foreign key to socialmediapost table

Revision ID: 8403c4fd09cb
Revises: 629f21e42d34
Create Date: 2022-01-16 15:48:33.730923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8403c4fd09cb'
down_revision = '629f21e42d34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('social_media_posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('social_media_posts_users_fk', source_table="social_media_posts", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('social_media_posts_users_fk', table_name="social_media_posts")
    op.drop_column('social_media_posts','owner_id')
    pass
