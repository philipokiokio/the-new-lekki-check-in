"""User Table

Revision ID: b59eb2cd4e8c
Revises: 
Create Date: 2023-02-05 13:56:20.314855

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b59eb2cd4e8c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "members",
        sa.Column("id", sa.Integer),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("password", sa.String, nullable=True),
        sa.Column("phone_number", sa.String, unique=True, nullable=True),
        sa.Column("is_visitor", sa.Boolean),
        sa.Column("visitor_count", sa.Integer, nullable=False),
        sa.Column("is_admin", sa.Boolean, nullable=False),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer),
        sa.Column("member_id", sa.Integer, nullable=False),
        sa.Column("token", sa.String, nullable=False),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="CASCADE"),
    )
    pass


def downgrade() -> None:
    op.drop_constraint("refresh_tokens_member_id_fkey", "refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_table("members")
    pass
