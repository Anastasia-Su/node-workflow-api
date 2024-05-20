"""'initial_migration'

Revision ID: ece12cecdab6
Revises: 
Create Date: 2024-05-19 22:20:04.695916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ece12cecdab6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('condition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('condition', sa.String(), nullable=False),
    sa.Column('parent_node_id', sa.Integer(), nullable=True),
    sa.Column('parent_message_node_id', sa.Integer(), nullable=True),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['parent_message_node_id'], ['message.id'], ),
    sa.ForeignKeyConstraint(['parent_node_id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('condition_edge',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('condition_node_id', sa.Integer(), nullable=True),
    sa.Column('edge', sa.Enum('YES', 'NO', name='conditionedges'), nullable=True),
    sa.ForeignKeyConstraint(['condition_node_id'], ['condition.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'SENT', 'OPEN', name='messagestatuses'), nullable=False),
    sa.Column('text', sa.String(length=511), nullable=False),
    sa.Column('parent_node_id', sa.Integer(), nullable=True),
    sa.Column('parent_condition_edge_id', sa.Integer(), nullable=True),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['parent_condition_edge_id'], ['condition_edge.id'], ),
    sa.ForeignKeyConstraint(['parent_node_id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('node_type', sa.Enum('START', 'MESSAGE', 'CONDITION', 'CONDITION_EDGE', 'END', name='nodetypes'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workflow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_workflow_id'), 'workflow', ['id'], unique=False)
    op.create_table('end',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('parent_node_id', sa.Integer(), nullable=True),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['parent_node_id'], ['message.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('start',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('start')
    op.drop_table('end')
    op.drop_index(op.f('ix_workflow_id'), table_name='workflow')
    op.drop_table('workflow')
    op.drop_table('node')
    op.drop_table('message')
    op.drop_table('condition_edge')
    op.drop_table('condition')
    # ### end Alembic commands ###