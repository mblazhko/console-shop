"""add user app

Revision ID: b28d9986ef57
Revises: 4cb577fe7721
Create Date: 2023-09-24 17:50:06.002618

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b28d9986ef57'
down_revision: Union[str, None] = '4cb577fe7721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('oauth_account',
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('oauth_name', sa.String(length=100), nullable=False),
    sa.Column('access_token', sa.String(length=1024), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=True),
    sa.Column('refresh_token', sa.String(length=1024), nullable=True),
    sa.Column('account_id', sa.String(length=320), nullable=False),
    sa.Column('account_email', sa.String(length=320), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth_account_account_id'), 'oauth_account', ['account_id'], unique=False)
    op.create_index(op.f('ix_oauth_account_oauth_name'), 'oauth_account', ['oauth_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_oauth_account_oauth_name'), table_name='oauth_account')
    op.drop_index(op.f('ix_oauth_account_account_id'), table_name='oauth_account')
    op.drop_table('oauth_account')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
