"""unique Role.role

Revision ID: 3b0b5cd61575
Revises: 39e62730d2db
Create Date: 2023-07-12 09:56:34.399182

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3b0b5cd61575'
down_revision = '39e62730d2db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('passwdv2')
    op.create_unique_constraint('uc_role', 'role', ['role'])
    op.execute("INSERT INTO role (role) VALUES ('administrator')")
    op.execute("INSERT INTO role (role) VALUES ('user')")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uc_role', 'role', type_='unique')
    op.create_table('passwdv2',
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('passwd', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('salt', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], name='passwdv2_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='passwdv2_pkey')
    )
    # ### end Alembic commands ###
