import logging
import random

from networkx import DiGraph

from dependencies import CommonDB
from nodes.crud import crud_message
from nodes.models import MessageStatuses
from utils.building_blocks.helpers_for_building_blocks import (
    find_next_node,
    exception_no_next_node,
)
from nodes import models


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def handle_message_node(
    db: CommonDB,
    G: DiGraph,
    current_node: models.MessageNode,
    message_nodes: list[models.MessageNode],
    condition_nodes: list[models.ConditionNode],
    end_nodes: list[models.EndNode],
) -> models.MessageNode | models.EndNode | models.ConditionNode:

    logger.debug("Message Node Logic")

    G.add_node(
        current_node.id,
        label="Message",
        status=current_node.status,
        text=current_node.text,
    )
    next_node = find_next_node(
        node_list=condition_nodes, current_node=current_node
    )

    if not next_node:
        next_node = find_next_node(
            node_list=end_nodes, current_node=current_node
        )

    if not next_node:
        next_node = find_next_node(
            node_list=message_nodes, current_node=current_node
        )

        if not next_node:
            # Find next node for the second round of workflow
            next_node = next(
                (
                    node
                    for node in message_nodes
                    if crud_message.get_message_node_detail(
                        db, node.parent_node_id
                    )
                ),
                None,
            )
            if next_node:
                # Assign random status to simulate status update in workflow.
                # You can remove this line, or substitute it with your status changing logic.
                next_node.status = random.choice(list(MessageStatuses))
                next_node.parent_node_id = current_node.id
                db.commit()
                db.refresh(next_node)

    if not next_node:
        exception_no_next_node(current_node=current_node)

    G.add_edge(current_node.id, next_node.id)

    return next_node
