"""${message.rstrip(".!? ")}.

Revision ID: ${up_revision}
% if down_revision:
Revises: ${down_revision | comma,n}
% else:
Revises:
% endif
Create Date: ${create_date}

"""

from collections.abc import Sequence

import sqlalchemy as sa
from advanced_alchemy import types as aa_types
from alembic import op

${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: str | Sequence[str] | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """Apply schema changes, then migrate data."""
    schema_upgrades()
    data_upgrades()


def downgrade() -> None:
    """Revert data changes, then revert the schema."""
    data_downgrades()
    schema_downgrades()


def schema_upgrades() -> None:
    """Apply the schema changes."""
    ${upgrades if upgrades else "pass"}


def schema_downgrades() -> None:
    """Revert the schema changes."""
    ${downgrades if downgrades else "pass"}


def data_upgrades() -> None:
    """Migrate existing data."""
    pass


def data_downgrades() -> None:
    """Revert the data migration."""
    pass
