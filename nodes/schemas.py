from pydantic import BaseModel

from nodes.models import MessageStatuses


class StartNodeBase(BaseModel):
    pass


class StartNodeCreate(StartNodeBase):
    pass


class StartNode(StartNodeBase):
    id: int
    message_node_id: int


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
    end_node_id: int


class ConditionNodeBase(BaseModel):
    condition: str


class ConditionNodeCreate(ConditionNodeBase):
    pass


class ConditionNode(ConditionNodeBase):
    id: int
    message_node_id: int


class EndNodeBase(BaseModel):
    pass


class EndNodeCreate(EndNodeBase):
    pass


class EndNode(EndNodeBase):
    id: int
    message_node_id: int


class WorkflowNodeBase(BaseModel):
    pass


class WorkflowNodeCreate(WorkflowNodeBase):
    pass


class WorkflowNode(WorkflowNodeBase):
    id: int
    start_node_id: int
    message_node_id: int
    condition_node_id: int
    end_node_id: int
