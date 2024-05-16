from pydantic import BaseModel
from sqlalchemy import Enum

from nodes.models import MessageStatuses


#
# class MessageStatuses(str, Enum):
#     PENDING = "PENDING"
#     SENT = "SENT"
#     OPENED = "OPENED"
#

#
# class NodeBase(BaseModel):
#     type: str
#
#
# class NodeCreate(NodeBase):
#     pass
#
#
# class Node(NodeBase):
#     id: int
#
#
# class AssociationBase(BaseModel):
#     source_node_id: int
#     target_node_id: int
#
#
# class AssociationCreate(NodeBase):
#     pass
#
#
# class Association(NodeBase):
#     id: int
#


class StartNodeBase(BaseModel):
    output_edge_id: int


class StartNodeCreate(StartNodeBase):
    pass


class StartNode(StartNodeBase):
    id: int


class MessageNodeBase(BaseModel):
    status: MessageStatuses
    text: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class MessageNodeCreate(MessageNodeBase):
    pass


class MessageNode(MessageNodeBase):
    id: int


class ConditionNodeBase(BaseModel):
    condition: str
    yes_edge_id: int
    no_edge_id: int


class ConditionNodeCreate(ConditionNodeBase):
    pass


class ConditionNode(ConditionNodeBase):
    id: int


class EndNodeBase(BaseModel):
    input_node_id: int


class EndNodeCreate(EndNodeBase):
    pass


class EndNode(EndNodeBase):
    id: int
