import logging
import time

from dependencies import CommonDB
from nodes import models
from nodes.crud import crud_workflow, crud_message
from nodes.models import ConditionEdges
from utils.graph import graph_build

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

    graph_build(start_node, message_nodes, condition_nodes, end_nodes)

    current_node = start_node
    iteration_count = 0
    num_of_iterations = 20

    start = time.time()

    while current_node and iteration_count < num_of_iterations:
        logger.debug(f"Current node: {current_node}")
        iteration_count += 1

        if isinstance(current_node, models.StartNode):
            print("Start Node Logic")
            association = start_node
            for message in message_nodes:
                if message.parent_node_id == current_node.id:
                    association = message
                    break

            if association is None:
                logger.error("No associated message node found for start node")
                break

            current_node = association
            logger.debug(f"Next node: {current_node}")

        elif isinstance(current_node, models.MessageNode):
            logger.debug("Message Node Logic")

            association = None

            for condition in condition_nodes:
                if condition.parent_node_id == current_node.id:
                    association = condition
                    break

                if (
                    current_node.parent_node_id == condition.id
                    and current_node.parent_condition_edge_id
                    == condition.edge.id
                ):
                    if condition.edge == ConditionEdges.YES:
                        for end_node in end_nodes:
                            if (
                                end_node.parent_message_node_id
                                == current_node.id
                            ):
                                association = end_node
                                break
                    if condition.edge == ConditionEdges.NO:
                        for end_node in end_nodes:
                            if (
                                end_node.parent_message_node_id
                                == current_node.id
                            ):
                                association = end_node
                                break

            if association is None:
                logger.error(
                    "No associated condition node found for message node"
                )
                break

            current_node = association
            logger.debug(f"Next node: {current_node}")

        elif isinstance(current_node, models.ConditionNode):
            logger.debug("Condition Node Logic")
            association = None

            for condition in condition_nodes:

                if current_node.condition == condition.condition:
                    parent_message_node = crud_message.get_message_node_detail(
                        db=db, node_id=current_node.parent_message_node_id
                    )

                    if (
                        condition.condition.split(" ")[-1].lower()
                        == parent_message_node.status.lower()
                    ):
                        current_node.edge.edge = ConditionEdges.YES
                    elif (
                        condition.condition.split(" ")[-1].lower()
                        != parent_message_node.status.lower()
                    ):
                        current_node.edge.edge = ConditionEdges.NO

                if (
                    condition.parent_node_id == current_node.id
                    and current_node.edge == ConditionEdges.NO
                ):
                    association = condition
                    break
            if association is None:
                for message in message_nodes:
                    if (
                        message.parent_node_id == current_node.id
                        and current_node.edge == ConditionEdges.YES
                    ):
                        association = message
                        break

            if association is None:
                logger.error(
                    "No associated message or condition node found for condition node"
                )
                break

            current_node = association
            logger.debug(f"Next node: {current_node}")

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
