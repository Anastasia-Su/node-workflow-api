from enum import StrEnum

from pydantic import BaseModel

from nodes.models import MessageStatuses


class StartNodeBase(BaseModel):
    message: str | None = None


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
    parent_node_id: int | None = None


class MessageNode(MessageNodeCreate):
    id: int


class ConditionNodeBase(BaseModel):
    condition: str
    edge: StrEnum


class ConditionNodeCreate(ConditionNodeBase):
    parent_node_id: int | None = None
    parent_message_node_id: int | None = None


class ConditionNode(ConditionNodeCreate):
    id: int


class EndNodeBase(BaseModel):
    message: str | None = None


class EndNodeCreate(EndNodeBase):
    parent_message_node_id: int | None = None


class EndNode(EndNodeCreate):
    id: int


class WorkflowBase(BaseModel):
    pass


class WorkflowCreate(WorkflowBase):
    start_node_id: int
    message_node_ids: list[int]
    condition_node_ids: list[int]
    end_node_id: int


class Workflow(WorkflowCreate):
    id: int
