from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Extra

from nodes.models import MessageStatuses, ConditionEdges


class StartNodeBase(BaseModel):
    message: str | None = None


class StartNodeCreate(StartNodeBase):
    workflow_id: int | None = None


class StartNode(StartNodeCreate):
    id: int


class MessageNodeBase(BaseModel):
    status: MessageStatuses
    text: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class MessageNodeCreate(MessageNodeBase):
    parent_node_id: int | None = None
    parent_condition_edge_id: int | None = None
    workflow_id: int | None = None


class MessageNode(MessageNodeCreate):
    id: int


class ConditionNodeBase(BaseModel):
    condition: str


class ConditionNodeCreate(ConditionNodeBase):
    parent_node_id: int | None = None
    parent_message_node_id: int | None = None
    workflow_id: int | None = None


class ConditionNode(ConditionNodeCreate):
    id: int


class ConditionEdgeBase(BaseModel):
    edge: ConditionEdges | None = None


class ConditionEdgeCreate(ConditionEdgeBase):
    condition_node_id: int | None = None


class ConditionEdge(ConditionEdgeCreate):
    id: int


class EndNodeBase(BaseModel):
    message: str | None = None


class EndNodeCreate(EndNodeBase):
    parent_message_node_id: int | None = None
    workflow_id: int | None = None


class EndNode(EndNodeCreate):
    id: int


class WorkflowBase(BaseModel):
    name: str


class WorkflowCreate(WorkflowBase):
    pass


class Workflow(WorkflowCreate):
    id: int
    start_node: StartNode | None = None
    message_nodes: list[MessageNode]
    condition_nodes: list[ConditionNode]
    end_nodes: list[EndNode]

    class Config:
        from_attributes = True
