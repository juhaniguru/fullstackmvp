"""add phone_number

Revision ID: 6003e5038eaa
Revises: 
Create Date: 2023-10-25 20:50:40.362913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6003e5038eaa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('phone_number', sa.String(30), nullable=True))



def downgrade() -> None:
    op.drop_column('user', 'phone_number')
