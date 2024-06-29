import logging

from networkx import DiGraph

from database.dependencies import CommonDB
from src.nodes.models import ConditionEdges
from src.utils.building_blocks.get_or_create_condition_edge import (
    get_or_create_condition_edge,
)
from src.utils.building_blocks.helpers_for_building_blocks import (
    exception_no_next_node,
)
from src.nodes import models


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def handle_condition_node(
    db: CommonDB,
    G: DiGraph,
    current_node: models.ConditionNode,
    message_nodes: list[models.MessageNode],
    condition_nodes: list[models.ConditionNode],
    condition_edges: list[models.ConditionEdge],
) -> models.ConditionNode | models.MessageNode:

    logger.debug("Condition Node Logic")
    G.add_node(
        current_node.id,
        label="Condition",
        condition=current_node.condition,
    )

    parent_message_node = next(
        (
            node
            for node in message_nodes
            if node.id == current_node.parent_message_node_id
        ),
        None,
    )

    if parent_message_node:
        condition_edge = get_or_create_condition_edge(
            db=db,
            current_node=current_node,
            condition_edges=condition_edges,
            parent_message_node=parent_message_node,
        )

        next_node = next(
            (
                node
                for node in message_nodes
                if node.parent_node_id == current_node.id
                and node.parent_condition_edge_id == condition_edge.id
            ),
            None,
        )
        if not next_node:
            next_node = next(
                (
                    node
                    for node in condition_nodes
                    if node.parent_node_id == current_node.id
                    and condition_edge.edge == ConditionEdges.NO
                ),
                None,
            )

        if not next_node:
            exception_no_next_node(current_node=current_node)

        G.add_edge(current_node.id, next_node.id, label=condition_edge.edge)

        return next_node
