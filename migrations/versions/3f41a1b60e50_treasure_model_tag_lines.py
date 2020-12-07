"""treasure model, tag lines

Revision ID: 3f41a1b60e50
Revises: 86ea1338caa3
Create Date: 2020-12-07 11:14:32.517460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f41a1b60e50'
down_revision = '86ea1338caa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('treasure', sa.Column('tag_line_1', sa.String(length=100), nullable=True))
    op.add_column('treasure', sa.Column('tag_line_2', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('treasure', 'tag_line_2')
    op.drop_column('treasure', 'tag_line_1')
    # ### end Alembic commands ###
