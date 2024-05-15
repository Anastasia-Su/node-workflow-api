from pydantic import BaseModel
from sqlalchemy import Enum

from nodes.models import MessageStatuses


#
# class MessageStatuses(str, Enum):
#     PENDING = "PENDING"
#     SENT = "SENT"
#     OPENED = "OPENED"
#


class NodeBase(BaseModel):
    type: str


class NodeCreate(NodeBase):
    pass


class Node(NodeBase):
    id: int


class AssociationBase(BaseModel):
    source_node_id: int
    target_node_id: int


class AssociationCreate(NodeBase):
    pass


class Association(NodeBase):
    id: int


class StartNodeBase(BaseModel):
    id: int
    output_edge_id: int


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
    id: int
    yes_edge_id: int
    no_edge_id: int
    previous_message_id: int


class EndNodeBase(BaseModel):
    id: int
    input_node_id: int

    class Config:
        from_attributes = True
