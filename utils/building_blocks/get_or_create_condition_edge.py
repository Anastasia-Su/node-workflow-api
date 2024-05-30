from dependencies import CommonDB
from nodes import models


def get_or_create_condition_edge(
    db: CommonDB,
    current_node: models.ConditionNode,
    condition_edges: list[models.ConditionEdge],
    parent_message_node: models.MessageNode,
) -> models.ConditionEdge:

    edge_value = (
        models.ConditionEdges.YES
        if current_node.condition.split(" ")[-1].lower()
        == parent_message_node.status.lower()
        else models.ConditionEdges.NO
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

    return condition_edge
