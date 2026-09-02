"""Completa el catálogo inmobiliario sin eliminar datos existentes."""
from alembic import op
import sqlalchemy as sa

revision = '002_catalogo_inmobiliario'
down_revision = '001_inicial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('categorias', sa.Column('slug', sa.String(100)))
    op.execute("UPDATE categorias SET slug = lower(regexp_replace(regexp_replace(nombre, '[^a-zA-Z0-9 ]', '', 'g'), '[ ]+', '-', 'g'))")
    op.alter_column('categorias', 'slug', nullable=False)
    op.create_unique_constraint('uq_categorias_slug', 'categorias', ['slug'])
    op.create_index('ix_categorias_slug', 'categorias', ['slug'])

    op.add_column('productos', sa.Column('stock', sa.Integer(), server_default='1', nullable=False))
    op.execute("UPDATE productos SET estado = lower(replace(estado, ' ', '_'))")
    op.execute("UPDATE productos SET estado = 'en_oferta' WHERE estado = 'en oferta'")
    op.create_check_constraint('ck_productos_stock_no_negativo', 'productos', 'stock >= 0')
    op.create_check_constraint("ck_productos_estado_valido", 'productos', "estado IN ('disponible', 'en_oferta', 'alquilada', 'reservada')")
    op.execute("UPDATE productos SET imagen_url = '/images/properties/property-placeholder.svg' WHERE imagen_url LIKE 'http%'")

    categories = [
        ('Propiedades comerciales', 'propiedades-comerciales'),
        ('Propiedades en alquiler', 'propiedades-en-alquiler'),
        ('Propiedades en preventa', 'propiedades-en-preventa'),
        ('Terrenos', 'terrenos'),
    ]
    for nombre, slug in categories:
        op.execute(sa.text("INSERT INTO categorias (id, nombre, slug) SELECT uuid_generate_v4(), :nombre, :slug WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE slug = :slug)").bindparams(nombre=nombre, slug=slug))


def downgrade() -> None:
    op.drop_constraint('ck_productos_estado_valido', 'productos', type_='check')
    op.drop_constraint('ck_productos_stock_no_negativo', 'productos', type_='check')
    op.drop_column('productos', 'stock')
    op.drop_index('ix_categorias_slug', table_name='categorias')
    op.drop_constraint('uq_categorias_slug', 'categorias', type_='unique')
    op.drop_column('categorias', 'slug')
