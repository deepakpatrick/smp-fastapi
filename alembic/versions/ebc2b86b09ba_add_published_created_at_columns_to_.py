"""add published, created_at columns to socialmediaposts table

Revision ID: ebc2b86b09ba
Revises: 8403c4fd09cb
Create Date: 2022-01-16 16:02:35.991124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebc2b86b09ba'
down_revision = '8403c4fd09cb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("social_media_posts",
                    sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE')
                )
    op.add_column("social_media_posts",
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
                    )
    pass


def downgrade():
    op.drop_column('social_media_posts', 'published')
    op.drop_column('social_media_posts', 'created_at')
    pass
