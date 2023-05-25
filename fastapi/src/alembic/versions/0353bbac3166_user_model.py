"""user model

Revision ID: 0353bbac3166
Revises: 
Create Date: 2023-05-24 20:11:38.373163

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0353bbac3166"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, index=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
