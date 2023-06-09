"""db change

Revision ID: d12d98e3ef72
Revises: 5904cab3cddd
Create Date: 2023-05-01 11:04:48.113581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd12d98e3ef72'
down_revision = '5904cab3cddd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('inventory', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_items_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], name=op.f('fk_carts_item_id_items')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], name=op.f('fk_receipts_item_id_items')),
    sa.ForeignKeyConstraint(['total'], ['carts.total'], name=op.f('fk_receipts_total_carts')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_receipts_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('characters')
    op.drop_table('comments')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('first_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('avatar', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('verified', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))
        batch_op.drop_column('updated_at')
        batch_op.drop_column('profile_image')
        batch_op.drop_column('display_name')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('display_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('profile_image', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), nullable=True))
        batch_op.drop_column('rating')
        batch_op.drop_column('verified')
        batch_op.drop_column('avatar')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')
        batch_op.drop_column('creation_date')

    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('contents', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_comments_character_id_characters'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_comments_user_id_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('characters',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('age', sa.VARCHAR(), nullable=True),
    sa.Column('race', sa.VARCHAR(), nullable=True),
    sa.Column('gender', sa.VARCHAR(), nullable=True),
    sa.Column('bio_1', sa.VARCHAR(), nullable=True),
    sa.Column('bio_2', sa.VARCHAR(), nullable=True),
    sa.Column('image_1', sa.VARCHAR(), nullable=True),
    sa.Column('image_2', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_characters_user_id_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('receipts')
    op.drop_table('carts')
    op.drop_table('items')
    # ### end Alembic commands ###
