"""empty message

Revision ID: 4de7f8ee3ae3
Revises: 
Create Date: 2024-04-28 13:38:16.533846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4de7f8ee3ae3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('company', 'address', existing_type=sa.String(100), nullable=True)


def downgrade() -> None:
    op.alter_column('company', 'address', existing_type=sa.String(100), nullable=False)
