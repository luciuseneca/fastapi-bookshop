"""rename user role to customer

Revision ID: 7b6f4e2d9a31
Revises: 8f5d1c40ae72
Create Date: 2026-09-16 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7b6f4e2d9a31"
down_revision: Union[str, None] = "8f5d1c40ae72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename the persisted customer role to match the application enum."""
    op.execute(
        "ALTER TYPE client_role_enum RENAME VALUE 'user' TO 'customer'"
    )


def downgrade() -> None:
    """Restore the previous persisted customer role name."""
    op.execute(
        "ALTER TYPE client_role_enum RENAME VALUE 'customer' TO 'user'"
    )
