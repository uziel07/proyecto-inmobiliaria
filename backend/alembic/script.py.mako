"""${message} ${up_revision}"""
from alembic import op
import sqlalchemy as sa
${upgrades if upgrades else 'pass'}
