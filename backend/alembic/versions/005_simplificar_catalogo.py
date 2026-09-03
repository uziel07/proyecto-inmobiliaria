"""Elimina tablas de compras no utilizadas por la plataforma."""
from alembic import op


revision = '005_simplificar_catalogo'
down_revision = '004_nombre_detalle_carrito'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # El catálogo y los clientes son el alcance actual de Nido Capital.
    op.drop_table('detalles_pedido')
    op.drop_table('pedidos')
    op.drop_table('detalle_carrito')
    op.drop_table('carritos')


def downgrade() -> None:
    raise NotImplementedError('La eliminación de tablas no se revierte automáticamente.')
