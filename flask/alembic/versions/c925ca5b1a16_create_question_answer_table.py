"""create question_answer table

Revision ID: c925ca5b1a16
Revises: 
Create Date: 2024-07-22 08:29:44.224237

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c925ca5b1a16"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "question_answer",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("question", sa.String(200), nullable=False),
        sa.Column("answer", sa.String(200), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("question_answer")
