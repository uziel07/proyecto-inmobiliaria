"""Alinea el nombre de la tabla de detalle del carrito con el contrato del sistema."""
from alembic import op

revision = '004_nombre_detalle_carrito'
down_revision = '003_defaults_uuid'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('detalles_carrito', 'detalle_carrito')


def downgrade() -> None:
    op.rename_table('detalle_carrito', 'detalles_carrito')
