"""create initial schema

Revision ID: xxxxxxxxxxxx
Revises: 
Create Date: 2024-05-15 HH:MM:SS.SSSSSS

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'xxxxxxxxxxxx'  # this will be auto-generated
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create dog_facts table
    op.create_table(
        'dog_facts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('dog_facts')
    op.drop_table('users')