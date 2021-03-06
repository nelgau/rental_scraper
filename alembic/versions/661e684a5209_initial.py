"""Initial

Revision ID: 661e684a5209
Revises: 
Create Date: 2019-04-24 18:20:38.881368+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '661e684a5209'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_crawl_at', sa.DateTime(), nullable=True),
    sa.Column('first_seen_at', sa.DateTime(), nullable=True),
    sa.Column('last_seen_at', sa.DateTime(), nullable=True),
    sa.Column('off_market_at', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=True),
    sa.Column('thumbnail_url', sa.String(length=1024), nullable=True),
    sa.Column('referrer_url', sa.String(length=1024), nullable=True),
    sa.Column('neighborhood_id', sa.Integer(), nullable=True),
    sa.Column('neighborhood', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zipcode', sa.String(length=5), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('sqft', sa.Integer(), nullable=True),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('pet_friendly', sa.Boolean(), nullable=True),
    sa.Column('furnished', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rentals_neighborhood'), 'rentals', ['neighborhood'], unique=False)
    op.create_index(op.f('ix_rentals_neighborhood_id'), 'rentals', ['neighborhood_id'], unique=False)
    op.create_index(op.f('ix_rentals_url'), 'rentals', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rentals_url'), table_name='rentals')
    op.drop_index(op.f('ix_rentals_neighborhood_id'), table_name='rentals')
    op.drop_index(op.f('ix_rentals_neighborhood'), table_name='rentals')
    op.drop_table('rentals')
    # ### end Alembic commands ###
