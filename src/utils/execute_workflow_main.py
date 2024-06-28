import time
import networkx as nx
from networkx import DiGraph

from database.dependencies import CommonDB
from src.nodes import models
from src.nodes.crud import crud_workflow, crud_condition_edge

from src.utils.building_blocks.handle_condition_node import (
    handle_condition_node,
)
from src.utils.building_blocks.handle_end_node import handle_end_node
from src.utils.building_blocks.handle_message_node import handle_message_node
from src.utils.building_blocks.handle_start_node import handle_start_node
from src.utils.building_blocks.helpers_for_building_blocks import (
    exception_unknown_node_type,
    get_node_lists,
    exception_for_infinite_loop,
)
from src.utils.graph import build_graph


def execute_workflow(
    db: CommonDB, workflow_id: int, draw_graph: bool = True
) -> dict[str, DiGraph | float]:
    """Execute workflow function:
    it gets all nodes for the current workflow and navigates them"""

    workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )
    condition_edges = crud_condition_edge.get_condition_edge_list(db)

    start_node, message_nodes, condition_nodes, end_nodes = get_node_lists(
        workflow_node=workflow_node, workflow_id=workflow_id
    )

    current_node = start_node
    G = nx.DiGraph()
    iteration_count = 0

    # `num_of_iterations` is added to prevent infinite loop error.
    # Adjust the number if your workflow is longer.
    num_of_iterations = 50
    start = time.time()

    while current_node and iteration_count < num_of_iterations:
        iteration_count += 1

        if isinstance(current_node, models.StartNode):
            current_node = handle_start_node(
                db=db,
                G=G,
                current_node=current_node,
                message_nodes=message_nodes,
            )

        elif isinstance(current_node, models.MessageNode):
            current_node = handle_message_node(
                db=db,
                G=G,
                current_node=current_node,
                message_nodes=message_nodes,
                condition_nodes=condition_nodes,
                end_nodes=end_nodes,
            )

        elif isinstance(current_node, models.ConditionNode):
            current_node = handle_condition_node(
                db=db,
                G=G,
                current_node=current_node,
                message_nodes=message_nodes,
                condition_nodes=condition_nodes,
                condition_edges=condition_edges,
            )

        elif isinstance(current_node, models.EndNode):
            handle_end_node(G=G, current_node=current_node)
            current_node = None

        else:
            exception_unknown_node_type(current_node=current_node)

    exception_for_infinite_loop(
        iteration_count=iteration_count, num_of_iterations=num_of_iterations
    )

    end = time.time()

    if draw_graph:
        build_graph(G)
    execution_time = end - start

    return {"graph": G, "execution_time": execution_time}
