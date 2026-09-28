"""create table

Revision ID: a7661b41192e
Revises:
Create Date: 2026-09-28 16:23:06.970694

"""

from typing import Sequence, Union

from sqlalchemy.dialects import postgresql

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7661b41192e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Unicode(255), nullable=False),
        sa.Column("description", sa.Unicode(255), nullable=False),
        sa.Column("content_type", sa.Unicode(50), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.UnicodeText()), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("documents")
