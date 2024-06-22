"""create users + words + userwords tables

Revision ID: 6e922de058e3
Revises: 
Create Date: 2024-06-22 12:50:27.668602

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6e922de058e3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


op.create_table(
    "users",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("tg_id", sa.BigInteger(), nullable=False),
    sa.Column("username", sa.String(), nullable=False),
    sa.Column("first_name", sa.String(), nullable=True),
    sa.Column("last_name", sa.String(), nullable=True),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    sa.UniqueConstraint("tg_id", name=op.f("uq_users_tg_id")),
)
def upgrade() -> None:
    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("in_russian", sa.String(length=255), nullable=False),
        sa.Column("in_english", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_words")),
    )
    op.create_table(
        "user_words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column(
            "repetition_counter",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_words_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["word_id"],
            ["words.id"],
            name=op.f("fk_user_words_word_id_words"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_words")),
    )


def downgrade() -> None:
    op.drop_table("user_words")
    op.drop_table("words")
    op.drop_table("users")
