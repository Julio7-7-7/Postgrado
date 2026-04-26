"""refactor: estandarizando tabla modalidades

Revision ID: 67944a20cf1c
Revises: e672f5c17017
Create Date: 2026-04-26 09:11:00.322220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '67944a20cf1c'
down_revision: Union[str, Sequence[str], None] = 'e672f5c17017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('modalidad', 'modalidades')
    op.add_column('modalidades', sa.Column('descripcion', sa.String(200), nullable=True))
    op.add_column('modalidades', sa.Column('estado', sa.String(20), nullable=False, server_default='activo'))
    op.drop_column('modalidades', 'vigente')
    op.alter_column('modalidades', 'nombre', type_=sa.String(50), existing_nullable=False)
    op.create_unique_constraint('uq_modalidades_nombre', 'modalidades', ['nombre'])
    op.drop_index(op.f('ix_modalidad_id_modalidad'), table_name='modalidades')
    op.create_index(op.f('ix_modalidades_id_modalidad'), 'modalidades', ['id_modalidad'], unique=False)
    op.drop_constraint(op.f('programa_version_edicion_id_modalidad_fkey'), 'programa_version_edicion', type_='foreignkey')
    op.create_foreign_key('programa_version_edicion_id_modalidad_fkey', 'programa_version_edicion', 'modalidades', ['id_modalidad'], ['id_modalidad'])

def downgrade() -> None:
    op.drop_constraint('programa_version_edicion_id_modalidad_fkey', 'programa_version_edicion', type_='foreignkey')
    op.create_foreign_key('programa_version_edicion_id_modalidad_fkey', 'programa_version_edicion', 'modalidades', ['id_modalidad'], ['id_modalidad'])
    op.drop_constraint('uq_modalidades_nombre', 'modalidades', type_='unique')
    op.drop_index(op.f('ix_modalidades_id_modalidad'), table_name='modalidades')
    op.create_index(op.f('ix_modalidad_id_modalidad'), 'modalidades', ['id_modalidad'], unique=False)
    op.drop_column('modalidades', 'estado')
    op.drop_column('modalidades', 'descripcion')
    op.add_column('modalidades', sa.Column('vigente', sa.Boolean(), nullable=False, server_default='true'))
    op.rename_table('modalidades', 'modalidad')
