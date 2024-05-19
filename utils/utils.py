import logging
import time

from dependencies import CommonDB
from nodes import models
from nodes.crud import crud_workflow, crud_message
from nodes.models import ConditionEdges, ConditionEdge
from utils.graph import build_graph

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def execute_workflow(db: CommonDB, workflow_id: int):
    workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )
    start_node = workflow_node.start_node
    message_nodes = workflow_node.message_nodes
    condition_nodes = workflow_node.condition_nodes
    end_nodes = workflow_node.end_nodes

    current_node = start_node
    iteration_count = 0
    num_of_iterations = 20

    start = time.time()

    while current_node and iteration_count < num_of_iterations:
        logger.debug(f"Current node: {current_node}")
        iteration_count += 1

        if isinstance(current_node, models.StartNode):
            logger.debug("Start Node Logic")
            next_node = next(
                (
                    node
                    for node in message_nodes
                    if node.parent_node_id == current_node.id
                ),
                None,
            )
            if not next_node:
                logger.error("No associated message node found for start node")
                break
            current_node = next_node

        elif isinstance(current_node, models.MessageNode):
            logger.debug("Message Node Logic")
            next_node = next(
                (
                    node
                    for node in condition_nodes
                    if node.parent_node_id == current_node.id
                ),
                None,
            )
            if not next_node:
                next_node = next(
                    (
                        end_node
                        for end_node in end_nodes
                        if end_node.parent_node_id == current_node.id
                    ),
                    None,
                )
            if not next_node:
                logger.error(
                    "No associated condition or end node found for message node"
                )
                break
            current_node = next_node

        elif isinstance(current_node, models.ConditionNode):
            logger.debug("Condition Node Logic")
            parent_message_node = next(
                (
                    node
                    for node in message_nodes
                    if node.id == current_node.parent_message_node_id
                ),
                None,
            )
            if parent_message_node:
                if (
                    current_node.condition.split(" ")[-1].lower()
                    == parent_message_node.status.lower()
                ):
                    current_node.edge = ConditionEdge(edge=ConditionEdges.YES)
                else:
                    current_node.edge = ConditionEdge(edge=ConditionEdges.NO)

                next_node = next(
                    (
                        node
                        for node in message_nodes
                        if node.parent_node_id == current_node.id
                        and current_node.edge.edge == ConditionEdges.YES
                    ),
                    None,
                )
                if not next_node:
                    next_node = next(
                        (
                            node
                            for node in condition_nodes
                            if node.parent_node_id == current_node.id
                            and current_node.edge.edge == ConditionEdges.NO
                        ),
                        None,
                    )
                if not next_node:
                    logger.error("No associated node found for condition node")
                    break
                current_node = next_node

        elif isinstance(current_node, models.EndNode):
            logger.debug("End Node Logic")
            current_node = None

        else:
            logger.error(f"Unknown node type: {type(current_node)}")
            break

    if iteration_count >= num_of_iterations:
        logger.error(
            "Reached maximum iterations, possible infinite loop detected"
        )
    else:
        logger.debug("Workflow execution completed")

    end = time.time()
    logger.debug(f"Workflow execution time: {end - start}")

    build_graph(start_node, message_nodes, condition_nodes, end_nodes)
