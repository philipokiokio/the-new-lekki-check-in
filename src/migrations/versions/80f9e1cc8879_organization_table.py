"""Attendance Table

Revision ID: 80f9e1cc8879
Revises: b59eb2cd4e8c
Create Date: 2023-02-05 17:37:00.078276

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "80f9e1cc8879"
down_revision = "b59eb2cd4e8c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer),
        sa.Column("member_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("sunday_service", sa.Boolean(), nullable=True),
        sa.Column("midweek_service", sa.Boolean(), nullable=False),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("attendance")
    pass
