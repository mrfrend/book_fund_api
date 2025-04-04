"""changed constraint in book

Revision ID: b372db1d83d9
Revises: 467b4340c066
Create Date: 2024-11-14 17:26:58.459046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b372db1d83d9'
down_revision: Union[str, None] = '467b4340c066'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('keywords',
               existing_type=sa.VARCHAR(length=70),
               nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('keywords',
               existing_type=sa.VARCHAR(length=70),
               nullable=False)

    # ### end Alembic commands ###
