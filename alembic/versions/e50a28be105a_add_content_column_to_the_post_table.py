"""add content column to the post table

Revision ID: e50a28be105a
Revises: 5ba9a2d07419
Create Date: 2024-10-04 18:08:34.845275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e50a28be105a'
down_revision: Union[str, None] = '5ba9a2d07419'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
