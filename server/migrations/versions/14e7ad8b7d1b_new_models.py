"""new models

Revision ID: 14e7ad8b7d1b
Revises: d12d98e3ef72
Create Date: 2023-05-09 09:34:59.801224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14e7ad8b7d1b'
down_revision = 'd12d98e3ef72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_carts_item_id_items', type_='foreignkey')
        batch_op.drop_column('total')

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.drop_constraint('fk_receipts_total_carts', type_='foreignkey')
        batch_op.drop_column('total')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total', sa.FLOAT(), nullable=True))
        batch_op.create_foreign_key('fk_receipts_total_carts', 'carts', ['total'], ['total'])

    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total', sa.FLOAT(), nullable=True))
        batch_op.create_foreign_key('fk_carts_item_id_items', 'items', ['item_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###