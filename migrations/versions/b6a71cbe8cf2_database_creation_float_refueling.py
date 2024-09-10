"""Database creation float refueling

Revision ID: b6a71cbe8cf2
Revises: ffbf0fa365b1
Create Date: 2024-09-05 13:47:20.328073

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6a71cbe8cf2"
down_revision: Union[str, None] = "ffbf0fa365b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "refueling",
        "quantity",
        existing_type=sa.REAL(),
        type_=sa.Float(precision=2, asdecimal=2, decimal_return_scale=2),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "refueling",
        "quantity",
        existing_type=sa.Float(precision=2, asdecimal=2, decimal_return_scale=2),
        type_=sa.REAL(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
