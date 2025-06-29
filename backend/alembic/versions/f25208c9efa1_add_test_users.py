"""add test users

Revision ID: f25208c9efa1
Revises: 322160f5e56a
Create Date: 2025-06-23 18:57:21.292876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f25208c9efa1'
down_revision: Union[str, Sequence[str], None] = '322160f5e56a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    connection.execute(
        sa.text("INSERT INTO users (email, password, full_name, role) VALUES (:email, :password, :full_name, :role)"),
        [
            {
                "email": "user@dimatech.com",
                "password": "$pbkdf2-sha256$29000$.19rLcX433vPuXdujbH23g$/nB.Bhcifc0aoyHjfqL2QDmxGaIXbgUn.Weyegu1I7k",
                "full_name": "Alice",
                "role": "USER"
            },
            {
                "email": "admin@dimatech.com",
                "password": "$pbkdf2-sha256$29000$.19rLcX433vPuXdujbH23g$/nB.Bhcifc0aoyHjfqL2QDmxGaIXbgUn.Weyegu1I7k",
                "full_name": "Charlie",
                "role": "ADMIN"
            },
        ]
    )
    connection.execute(
        sa.text("INSERT INTO accounts (balance, user_id) VALUES (:balance, :user_id)"),
        [
            {"balance": 1000, "user_id": 1},
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM users WHERE email IN (:email1, :email2)"),
        {"email1": "user@dimatech.com", "email2": "admin@dimatech.com"}
    )
    ##
    connection.execute(
        sa.text("DELETE FROM accounts WHERE user_id IN (:email1)"),
        {"email1": "1"}
    )
    # ### end Alembic commands ###
