"""uniqueconstrain driver

Revision ID: 48bc8f16bbaa
Revises: f6ed6f991873
Create Date: 2024-09-26 08:53:05.061328

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "48bc8f16bbaa"
down_revision: Union[str, None] = "f6ed6f991873"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("people_date_uc", "driver", type_="unique")
    op.create_unique_constraint(
        "people_date_uc", "driver", ["id_driver", "id_people", "date_trip"]
    )
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
        existing_type=sa.Float(
            precision=2, asdecimal=2, decimal_return_scale=2
        ),
        type_=sa.REAL(),
        existing_nullable=False,
    )
    op.drop_constraint("people_date_uc", "driver", type_="unique")
    op.create_unique_constraint(
        "people_date_uc", "driver", ["id_people", "date_trip"]
    )
    # ### end Alembic commands ###
