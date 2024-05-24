import logging
import time
import networkx as nx
from fastapi import HTTPException
from networkx import DiGraph

from dependencies import CommonDB
from nodes import models, crud
from nodes.crud import (
    crud_workflow,
    crud_message,
    crud_condition_edge,
    crud_condition,
)
from nodes.models import (
    ConditionEdges,
    ConditionEdge,
    EnumConditions,
    MessageStatuses,
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
    # start_node = workflow_node.start_node.id
    #     # message_nodes = workflow_node.message_nodes
    #     # condition_nodes = workflow_node.condition_nodes
    #     # end_nodes = workflow_node.end_nodes

    start_node = (
        workflow_node.start_node
        if workflow_node.start_node.id == workflow_id
        else None
    )

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

    if not start_node:
        raise HTTPException(status_code=404, detail="Start node not found")

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
                label="Start Node",
                message=current_node.message,
            )

            next_node = next(
                (
                    node
                    for node in message_nodes
                    if node.parent_node_id == current_node.id
                ),
                None,
            )

            if not next_node:
                raise HTTPException(
                    status_code=404,
                    detail=f"No associated message node found for start node",
                )

            G.add_edge(current_node.id, next_node.id)
            current_node = next_node

        elif isinstance(current_node, models.MessageNode):
            logger.debug("Message Node Logic")
            G.add_node(
                current_node.id,
                label="Message Node",
                status=current_node.status,
                text=current_node.text,
            )

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
                next_node = next(
                    (
                        node
                        for node in message_nodes
                        if node.parent_node_id == current_node.id
                    ),
                    None,
                )

                first_message_node = next(
                    (
                        node
                        for node in message_nodes
                        if node.parent_node_id == start_node.id
                    ),
                    None,
                )

                if not next_node:
                    # time.sleep(5)

                    first_condition_node = next(
                        (
                            node
                            for node in condition_nodes
                            if node.parent_node_id == first_message_node.id
                        ),
                        None,
                    )

                    first_message_node.status = MessageStatuses.SENT
                    db.commit()
                    db.refresh(first_message_node)

                    next_node = first_condition_node

            if not next_node:
                raise HTTPException(
                    status_code=404,
                    detail=f"No associated condition or end node found for message node",
                )

            G.add_edge(current_node.id, next_node.id)
            current_node = next_node

        elif isinstance(current_node, models.ConditionNode):
            logger.debug("Condition Node Logic")
            G.add_node(
                current_node.id,
                label="Condition Node",
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
                if (
                    # parent_message_node.status.lower()
                    # not in current_node.condition.lower()
                    current_node.condition.split(" ")[-1].lower()
                    == parent_message_node.status.lower()
                ):
                    edge_value = ConditionEdges.YES
                else:
                    edge_value = ConditionEdges.NO

                current_node.edge = next(
                    (
                        condition_edge
                        for condition_edge in condition_edges
                        if condition_edge.condition_node_id == current_node.id
                        and condition_edge.edge == edge_value
                    ),
                    None,
                )

                # if not current_node.edge:
                #     current_node.edge = ConditionEdge(
                #         edge=edge_value,
                #         condition_node_id=current_node.id,
                #     )

                # Find the next node based on the current condition edge
                next_node = next(
                    (
                        node
                        for node in message_nodes
                        if node.parent_node_id == current_node.id
                        and node.parent_condition_edge_id
                        == current_node.edge.id
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
                    raise HTTPException(
                        status_code=404,
                        detail="No associated node found for condition node",
                    )

                # Add the edge to the graph
                G.add_edge(
                    current_node.id, next_node.id, label=current_node.edge.edge
                )
                current_node = next_node

        elif isinstance(current_node, models.EndNode):
            logger.debug("End Node Logic")
            G.add_node(
                current_node.id, label="End Node", message=current_node.message
            )

            current_node = None

        else:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown node type: {type(current_node)}",
            )

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


#
# import logging
# import time
# import networkx as nx
# from fastapi import HTTPException
# from networkx import DiGraph
#
# from dependencies import CommonDB
# from nodes import models, crud
# from nodes.crud import (
#     crud_workflow,
#     crud_message,
#     crud_condition_edge,
#     crud_condition,
# )
# from nodes.models import (
#     ConditionEdges,
#     ConditionEdge,
#     EnumConditions,
#     MessageStatuses,
# )
# from utils.graph import build_graph

#
# def clone_node(node, parent_node_id, workflow_id):
#     if isinstance(node, models.MessageNode):
#         return models.MessageNode(
#             text=node.text,
#             status=node.status,
#             parent_node_id=parent_node_id,
#             workflow_id=workflow_id,
#         )
#     elif isinstance(node, models.ConditionNode):
#         return models.ConditionNode(
#             condition=node.condition,
#             parent_message_node_id=parent_node_id,
#             workflow_id=workflow_id,
#         )
#     elif isinstance(node, models.EndNode):
#         return models.EndNode(
#             message=node.message,
#             parent_node_id=parent_node_id,
#             workflow_id=workflow_id,
#         )
#     else:
#         raise ValueError("Unsupported node type")

#
# def execute_workflow(
#     db: CommonDB, workflow_id: int
# ) -> dict[str, DiGraph | float]:
#     workflow_node = crud_workflow.get_workflow_detail(
#         db=db, node_id=workflow_id
#     )
#     condition_edges = crud_condition_edge.get_condition_edge_list(db)
#
#     start_node = (
#         workflow_node.start_node
#         if workflow_node.start_node.id == workflow_id
#         else None
#     )
#
#     message_nodes = [
#         node
#         for node in workflow_node.message_nodes
#         if node.workflow_id == workflow_id
#     ]
#     condition_nodes = [
#         node
#         for node in workflow_node.condition_nodes
#         if node.workflow_id == workflow_id
#     ]
#     end_nodes = [
#         node
#         for node in workflow_node.end_nodes
#         if node.workflow_id == workflow_id
#     ]
#
#     if not start_node:
#         raise HTTPException(status_code=404, detail="Start node not found")
#
#     current_node = start_node
#
#     G = nx.DiGraph()
#
#     iteration_count = 0
#     num_of_iterations = 20
#
#     start = time.time()
#
#     while current_node and iteration_count < num_of_iterations:
#         logger.debug(f"Current node: {current_node}")
#         iteration_count += 1
#
#         if isinstance(current_node, models.StartNode):
#             logger.debug("Start Node Logic")
#             G.add_node(
#                 current_node.id,
#                 label="Start Node",
#                 message=current_node.message,
#             )
#
#             next_node = next(
#                 (
#                     node
#                     for node in message_nodes
#                     if node.parent_node_id == current_node.id
#                 ),
#                 None,
#             )
#
#             if not next_node:
#                 raise HTTPException(
#                     status_code=404,
#                     detail=f"No associated message node found for start node",
#                 )
#
#             G.add_edge(current_node.id, next_node.id)
#             current_node = next_node
#
#         elif isinstance(current_node, models.MessageNode):
#             logger.debug("Message Node Logic")
#             G.add_node(
#                 current_node.id,
#                 label="Message Node",
#                 status=current_node.status,
#                 text=current_node.text,
#             )
#
#             next_node = next(
#                 (
#                     node
#                     for node in condition_nodes
#                     if node.parent_node_id == current_node.id
#                 ),
#                 None,
#             )
#             if not next_node:
#                 next_node = next(
#                     (
#                         end_node
#                         for end_node in end_nodes
#                         if end_node.parent_node_id == current_node.id
#                     ),
#                     None,
#                 )
#
#             if not next_node:
#                 next_node = next(
#                     (
#                         node
#                         for node in message_nodes
#                         if node.parent_node_id == current_node.id
#                     ),
#                     None,
#                 )
#             first_message_node = next(
#                 (
#                     node
#                     for node in message_nodes
#                     if node.parent_node_id == start_node.id
#                 ),
#                 None,
#             )
#
#             if (
#                 not next_node
#                 and first_message_node.status != MessageStatuses.SENT
#             ):
#                 # time.sleep(5)
#
#                 first_condition_node = next(
#                     (
#                         node
#                         for node in condition_nodes
#                         if node.parent_node_id == first_message_node.id
#                     ),
#                     None,
#                 )
#
#                 first_message_node.status = MessageStatuses.SENT
#                 db.commit()
#                 db.refresh(first_message_node)
#
#                 # if first_condition_node:
#                 #     cloned_condition_node = clone_node(
#                 #         first_condition_node,
#                 #         first_message_node.id,
#                 #         workflow_id,
#                 #     )
#                 #     db.add(cloned_condition_node)
#                 #     db.commit()
#                 #     db.refresh(cloned_condition_node)
#                 if first_condition_node:
#                     # if (
#                     #     first_condition_node.condition.split(" ")[-1].lower()
#                     #     == first_message_node.status.lower()
#                     # ):
#                     #     edge_value = ConditionEdges.YES
#                     # else:
#                     #     edge_value = ConditionEdges.NO
#                     #
#                     # first_condition_node.edge = next(
#                     #     (
#                     #         condition_edge
#                     #         for condition_edge in condition_edges
#                     #         if condition_edge.condition_node_id
#                     #         == current_node.id
#                     #         and condition_edge.edge == edge_value
#                     #     ),
#                     #     None,
#                     # )
#                     #
#                     # if not first_condition_node.edge:
#                     #     current_node.edge = ConditionEdge(
#                     #         edge=edge_value,
#                     #         condition_node_id=current_node.id,
#                     #     )
#
#                     next_node = first_condition_node
#
#             if (
#                 not next_node
#                 and first_message_node.status == MessageStatuses.SENT
#             ):
#                 end_node_created = models.EndNode(
#                     message="End Node Created",
#                     parent_node_id=current_node.id,
#                     workflow_id=workflow_id,
#                 )
#                 db.add(end_node_created)
#                 db.commit()
#                 db.refresh(end_node_created)
#
#                 next_node = end_node_created
#
#             # next_node = first_condition_node
#
#             if not next_node:
#                 raise HTTPException(
#                     status_code=404,
#                     detail=f"No associated condition or end node found for message node",
#                 )
#
#             G.add_edge(current_node.id, next_node.id)
#             current_node = next_node
#
#         elif isinstance(current_node, models.ConditionNode):
#             logger.debug("Condition Node Logic")
#             G.add_node(
#                 current_node.id,
#                 label="Condition Node",
#                 condition=current_node.condition,
#             )
#
#             parent_message_node = next(
#                 (
#                     node
#                     for node in message_nodes
#                     if node.id == current_node.parent_message_node_id
#                 ),
#                 None,
#             )
#
#             if parent_message_node:
#                 if (
#                     current_node.condition.split(" ")[-1].lower()
#                     == parent_message_node.status.lower()
#                 ):
#                     edge_value = ConditionEdges.YES
#                 else:
#                     edge_value = ConditionEdges.NO
#
#                 current_node.edge = next(
#                     (
#                         condition_edge
#                         for condition_edge in condition_edges
#                         if condition_edge.condition_node_id == current_node.id
#                         and condition_edge.edge == edge_value
#                     ),
#                     None,
#                 )
#
#                 if not current_node.edge:
#                     current_node.edge = ConditionEdge(
#                         edge=edge_value,
#                         condition_node_id=current_node.id,
#                     )
#
#                 # Find the next node based on the current condition edge
#                 next_node = next(
#                     (
#                         node
#                         for node in message_nodes
#                         if node.parent_node_id == current_node.id
#                         and node.parent_condition_edge_id
#                         == current_node.edge.id
#                     ),
#                     None,
#                 )
#                 if not next_node:
#                     next_node = next(
#                         (
#                             node
#                             for node in condition_nodes
#                             if node.parent_node_id == current_node.id
#                             and current_node.edge.edge == ConditionEdges.NO
#                         ),
#                         None,
#                     )
#
#                 if not next_node:
#                     raise HTTPException(
#                         status_code=404,
#                         detail=f"No associated node found for condition node {current_node.id}",
#                     )
#
#                     # Add the edge to the graph
#                 G.add_edge(
#                     current_node.id, next_node.id, label=current_node.edge.edge
#                 )
#                 current_node = next_node
#
#         elif isinstance(current_node, models.EndNode):
#             logger.debug("End Node Logic")
#             G.add_node(
#                 current_node.id, label="End Node", message=current_node.message
#             )
#
#             current_node = None
#
#         else:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Unknown node type: {type(current_node)}",
#             )
#
#     if iteration_count >= num_of_iterations:
#         logger.error(
#             "Reached maximum iterations, possible infinite loop detected"
#         )
#     else:
#         logger.debug("Workflow execution completed")
#
#     end = time.time()
#     logger.debug(f"Workflow execution time: {end - start}")
#
#     build_graph(G)
#
#     execution_time = end - start
#
#     return {"graph": G, "execution_time": execution_time}