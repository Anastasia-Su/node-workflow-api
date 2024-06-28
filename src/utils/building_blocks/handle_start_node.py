import logging
import random

from networkx import DiGraph

from database.dependencies import CommonDB
from src.nodes.models import MessageStatuses
from src.utils.building_blocks.helpers_for_building_blocks import (
    find_next_node,
    exception_no_next_node,
)
from src.nodes import models


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def handle_start_node(
    db: CommonDB,
    G: DiGraph,
    current_node: models.StartNode,
    message_nodes: list[models.MessageNode],
) -> models.MessageNode:

    logger.debug("Start Node Logic")

    G.add_node(
        current_node.id,
        label="Start",
        message=current_node.message,
    )

    next_node = find_next_node(
        node_list=message_nodes, current_node=current_node
    )

    if not next_node:
        exception_no_next_node(current_node=current_node)

    # Assign random status to simulate status update in workflow.
    # You can remove this block,
    # or substitute it with your status changing logic.
    next_node.status = random.choice(list(MessageStatuses))
    db.commit()
    db.refresh(next_node)

    G.add_edge(current_node.id, next_node.id)

    return next_node
