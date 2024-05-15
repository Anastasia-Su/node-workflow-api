from pydantic import BaseModel
from sqlalchemy import Enum


class MessageStatuses(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    OPENED = "OPENED"


class NodeBase(BaseModel):
    id: int
    type: str


class StartNodeBase(BaseModel):
    id: int
    output_edge_id: int


class MessageNodeBase(BaseModel):
    status: MessageStatuses
    text: str

    class Config:
        arbitrary_types_allowed = True


class MessageNode(MessageNodeBase):
    id: int


class MessageNodeCreate(MessageNodeBase):
    pass


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
