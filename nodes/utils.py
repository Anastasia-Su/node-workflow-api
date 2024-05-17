from dependencies import CommonDB
from nodes import models, crud
from nodes.crud import crud_workflow, crud_condition, crud_message
from nodes.models import ConditionEdges


def execute_workflow(db: CommonDB, workflow_id: int):
    workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )
    start_node = workflow_node.start_node
    messages = workflow_node.message_nodes
    conditions = workflow_node.condition_nodes
    end_node = workflow_node.end_node

    current_node = start_node

    while current_node:
        if isinstance(current_node, models.StartNode):
            print("Start Node Logic")
            association = start_node
            for message in messages:
                if message.parent_id == current_node.id:
                    association = message

            current_node = association

        elif isinstance(current_node, models.MessageNode):
            print("Message Node Logic")

            association = current_node
            for condition in conditions:
                if condition.parent_id == current_node.id:
                    association = condition

                if (
                    current_node.parent_node_id == condition.id
                    and current_node.parent_condition_edge_id
                    == condition.edge.id
                ):
                    if condition.edge == ConditionEdges.YES:
                        association = end_node
                    if condition.edge == ConditionEdges.NO:
                        association = end_node

            current_node = association

        elif isinstance(current_node, models.ConditionNode):
            print("Condition Node Logic")

            association = current_node

            for condition in conditions:
                print(
                    "conditionname", condition.condition.split(" ")[-1].lower()
                )

                if current_node.condition == condition.condition:
                    # TODO: add exception handling
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

            for message in messages:
                if (
                    message.parent_node_id == current_node.id
                    and current_node.edge == ConditionEdges.YES
                ):
                    association = message

            current_node = association

        elif isinstance(current_node, models.EndNode):
            print("End Node Logic")
            current_node = None
