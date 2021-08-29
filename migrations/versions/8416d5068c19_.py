"""empty message

Revision ID: 8416d5068c19
Revises: 6a9277ec3083
Create Date: 2021-08-29 10:31:10.297782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8416d5068c19'
down_revision = '6a9277ec3083'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('todos_list_id_fkey', 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'todolists', ['list_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key('todos_list_id_fkey', 'todos', 'todolists', ['list_id'], ['id'])
    # ### end Alembic commands ###