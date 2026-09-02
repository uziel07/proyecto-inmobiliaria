"""Añade generación automática de UUID para nuevas propiedades."""
from alembic import op
import sqlalchemy as sa

revision = '003_defaults_uuid'
down_revision = '002_catalogo_inmobiliario'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('productos', 'id', server_default=sa.text('uuid_generate_v4()'))


def downgrade() -> None:
    op.alter_column('productos', 'id', server_default=None)
