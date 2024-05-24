import logging
import random
import time
import networkx as nx
from networkx import DiGraph

from dependencies import CommonDB
from nodes import models
from nodes.crud import crud_workflow, crud_message, crud_condition_edge
from nodes.models import (
    ConditionEdges,
    MessageStatuses,
)
from utils.helper_funcs_for_utils import (
    exception_no_next_node,
    find_next_node,
    exception_unknown_node_type,
    exception_no_start_node,
)
from utils.graph import build_graph

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def execute_workflow(
    db: CommonDB, workflow_id: int
) -> dict[str, DiGraph | float]:
    workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )
    condition_edges = crud_condition_edge.get_condition_edge_list(db)

    start_node = (
        workflow_node.start_node
        if workflow_node.start_node.id == workflow_id
        else None
    )
    if not start_node:
        exception_no_start_node()

    message_nodes = [
        node
        for node in workflow_node.message_nodes
        if node.workflow_id == workflow_id
    ]
    condition_nodes = [
        node
        for node in workflow_node.condition_nodes
        if node.workflow_id == workflow_id
    ]
    end_nodes = [
        node
        for node in workflow_node.end_nodes
        if node.workflow_id == workflow_id
    ]

    current_node = start_node
    G = nx.DiGraph()
    iteration_count = 0
    num_of_iterations = 50
    start = time.time()

    while current_node and iteration_count < num_of_iterations:
        logger.debug(f"Current node: {current_node}")
        iteration_count += 1

        if isinstance(current_node, models.StartNode):
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

            next_node.status = random.choice(list(MessageStatuses))
            db.commit()
            db.refresh(next_node)

            G.add_edge(current_node.id, next_node.id)
            current_node = next_node

        elif isinstance(current_node, models.MessageNode):
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
                        logger.debug(
                            f"Assigning new status to message node {next_node.id}"
                        )
                        next_node.status = random.choice(list(MessageStatuses))
                        next_node.parent_node_id = current_node.id
                        db.commit()
                        db.refresh(next_node)

            if not next_node:
                exception_no_next_node(current_node=current_node)

            G.add_edge(current_node.id, next_node.id)
            current_node = next_node

        elif isinstance(current_node, models.ConditionNode):
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
                edge_value = (
                    ConditionEdges.YES
                    if current_node.condition.split(" ")[-1].lower()
                    == parent_message_node.status.lower()
                    else ConditionEdges.NO
                )
                condition_edge = next(
                    (
                        condition_edge
                        for condition_edge in condition_edges
                        if condition_edge.condition_node_id == current_node.id
                        and condition_edge.edge == edge_value
                    ),
                    None,
                )

                if not condition_edge:
                    condition_edge = models.ConditionEdge(
                        edge=edge_value, condition_node_id=current_node.id
                    )
                    db.add(condition_edge)
                    db.commit()
                    db.refresh(condition_edge)

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

                G.add_edge(
                    current_node.id, next_node.id, label=condition_edge.edge
                )
                current_node = next_node

        elif isinstance(current_node, models.EndNode):
            logger.debug("End Node Logic")
            G.add_node(
                current_node.id, label="End", message=current_node.message
            )
            current_node = None

        else:
            exception_unknown_node_type(current_node=current_node)

    if iteration_count >= num_of_iterations:
        logger.error(
            "Reached maximum iterations, possible infinite loop detected"
        )
    else:
        logger.debug("Workflow execution completed")

    end = time.time()
    logger.debug(f"Workflow execution time: {end - start}")

    build_graph(G)
    execution_time = end - start

    return {"graph": G, "execution_time": execution_time}
