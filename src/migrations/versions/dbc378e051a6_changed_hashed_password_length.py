"""changed hashed_password length

Revision ID: dbc378e051a6
Revises: 74c42d832036
Create Date: 2024-11-19 18:15:18.718046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbc378e051a6'
down_revision: Union[str, None] = '74c42d832036'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('hashed_password',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=60),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('hashed_password',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
