"""изменил default в view_book

Revision ID: b337a51653be
Revises: 2cf3d1b83a20
Create Date: 2024-12-19 11:00:09.506640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b337a51653be'
down_revision: Union[str, None] = '2cf3d1b83a20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('view_book', schema=None) as batch_op:
        batch_op.alter_column('count_view',
               existing_type=sa.INTEGER(),
               server_default=sa.text('1'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('view_book', schema=None) as batch_op:
        batch_op.alter_column('count_view',
               existing_type=sa.INTEGER(),
               server_default=sa.text('0'),
               existing_nullable=False)

    # ### end Alembic commands ###
