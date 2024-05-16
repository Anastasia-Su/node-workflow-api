from nodes import models


def execute_workflow(start_node):
    current_node = start_node
    while current_node:
        if isinstance(current_node, models.StartNode):
            print("Start Node Logic")

            association = current_node.message_node
            current_node = association

        elif isinstance(current_node, models.MessageNode):
            print("Message Node Logic")

            if current_node.status == models.MessageStatuses.SENT:
                association = current_node.condition_node.yes_node
            else:
                association = current_node.condition_node.no_node

            current_node = association

        elif isinstance(current_node, models.ConditionNode):
            print("Condition Node Logic")
            if (
                current_node.condition
                == f"If message status is {models.MessageStatuses.SENT}"
            ):
                association = current_node.yes_node
            else:
                association = current_node.no_node
            current_node = association

        elif isinstance(current_node, models.EndNode):
            print("End Node Logic")
            current_node = None
