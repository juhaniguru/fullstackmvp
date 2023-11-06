"""alter password

Revision ID: 1cbf8c43e4dd
Revises: 6003e5038eaa
Create Date: 2023-10-25 21:01:15.908402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1cbf8c43e4dd'
down_revision: Union[str, None] = '6003e5038eaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(table_name='user', column_name='password',
                    existing_type=sa.String(length=255),
                    type_=sa.String(length=256),
                    existing_nullable=False)


def downgrade() -> None:
    op.alter_column(table_name='user', column_name='password',
                    existing_type=sa.String(length=256),
                    type_=sa.String(length=255),
                    existing_nullable=False)
