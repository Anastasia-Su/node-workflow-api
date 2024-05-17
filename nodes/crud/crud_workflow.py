import json

from sqlalchemy.orm import Session
from nodes import models, schemas


def get_workflow_list(db: Session) -> list[models.Workflow]:
    return db.query(models.Workflow).all()


def get_workflow_detail(db: Session, node_id: int) -> models.Workflow:
    node = db.query(models.Workflow).get(node_id)

    message_node_ids_list = [
        int(id_str) for id_str in node.message_node_ids[1:-1].split(",")
    ]
    condition_node_ids_list = [
        int(id_str) for id_str in node.condition_node_ids[1:-1].split(",")
    ]
    node.message_node_ids = message_node_ids_list
    node.condition_node_ids = condition_node_ids_list

    return node


def create_workflow(
    db: Session, node: schemas.WorkflowCreate
) -> models.Workflow:

    message_node_ids_str = ",".join(map(str, node.message_node_ids))
    condition_node_ids_str = ",".join(map(str, node.condition_node_ids))

    db_node = models.Workflow(
        start_node_id=node.start_node_id,
        message_node_ids=json.dumps(node.message_node_ids),
        condition_node_ids=json.dumps(node.condition_node_ids),
        end_node_id=node.end_node_id,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    # TODO: double check it
    message_node_ids_list = [
        int(id_str) for id_str in message_node_ids_str.split(",")
    ]
    condition_node_ids_list = [
        int(id_str) for id_str in condition_node_ids_str.split(",")
    ]

    # Update the workflow node object with the lists
    db_node.message_node_ids = message_node_ids_list
    db_node.condition_node_ids = condition_node_ids_list

    return db_node


def update_workflow(
    db: Session, node_id: int, new_node: schemas.WorkflowCreate
):

    node = db.get(models.Workflow, node_id)
    # message_node_ids_str = ",".join(map(str, node.message_node_ids))
    # condition_node_ids_str = ",".join(map(str, node.condition_node_ids))
    #
    # print(message_node_ids_str)
    print(node.message_node_ids)
    print(node.condition_node_ids)

    # new_node.message_node_ids = message_node_ids_str
    # new_node.condition_node_ids = condition_node_ids_str

    if node:
        node.start_node_id = new_node.start_node_id
        node.message_node_ids = json.dumps(new_node.message_node_ids)
        node.condition_node_ids = json.dumps(new_node.condition_node_ids)
        node.end_node_id = new_node.end_node_id

        db.commit()
        db.refresh(node)

        message_node_ids_list = [
            int(id_str) for id_str in node.message_node_ids[1:-1].split(",")
        ]
        condition_node_ids_list = [
            int(id_str) for id_str in node.condition_node_ids[1:-1].split(",")
        ]

        # Update the workflow node object with the lists
        node.message_node_ids = message_node_ids_list
        node.condition_node_ids = condition_node_ids_list

    return node


def delete_workflow(db: Session, node_id: int):
    node = db.get(models.Workflow, node_id)
    if node:
        db.delete(node)
        db.commit()

    return node
