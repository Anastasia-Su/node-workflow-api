from enum import auto, StrEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from database import Base


workflow_message_association = Table(
    "workflow_message_association",
    Base.metadata,
    Column("workflow_id", Integer, ForeignKey("workflow.id")),
    Column("message_node_id", Integer, ForeignKey("message.id")),
)

workflow_condition_association = Table(
    "workflow_condition_association",
    Base.metadata,
    Column("workflow_id", Integer, ForeignKey("workflow.id")),
    Column("condition_node_id", Integer, ForeignKey("condition.id")),
)


class MessageStatuses(StrEnum):
    PENDING = auto()
    SENT = auto()
    OPENED = auto()


class NodeTypes(StrEnum):
    START = auto()
    MESSAGE = auto()
    CONDITION = auto()
    END = auto()


class ConditionEdges(StrEnum):
    YES = auto()
    NO = auto()


class Node(Base):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    node_type = Column(Enum(NodeTypes))

    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": node_type,
    }


class StartNode(Node):
    __tablename__ = "start"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    message = Column(String(255), nullable=True)

    # message_node_id = Column(Integer, ForeignKey("message.id"), nullable=True)
    # message_node = relationship(
    #     "MessageNode",
    #     back_populates="start_node",
    #     foreign_keys=[message_node_id],
    # )

    workflow = relationship(
        "Workflow",
        back_populates="start_node",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.START,
    }


class MessageNode(Node):
    __tablename__ = "message"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    status = Column(Enum(MessageStatuses), nullable=False)
    text = Column(String(511), nullable=False)

    parent_node_id = Column(Integer, ForeignKey("node.id"), nullable=True)

    # condition_node = relationship(
    #     "ConditionNode",
    #     back_populates="message_node",
    # )
    #
    # start_node = relationship(
    #     "StartNode",
    #     back_populates="message_node",
    # )

    workflow = relationship(
        "Workflow",
        secondary=workflow_message_association,
        backref="workflow_message_nodes",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.MESSAGE,
        "inherit_condition": (id == Node.id),
    }


class ConditionNode(Node):
    __tablename__ = "condition"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    condition = Column(String, nullable=False)

    # message_node_id = Column(Integer, ForeignKey("message.id"), nullable=True)

    parent_node_id = Column(Integer, ForeignKey("node.id"), nullable=True)
    parent_message_node_id = Column(
        Integer, ForeignKey("message.id"), nullable=True
    )
    edge = Column(Enum(ConditionEdges), nullable=True)

    # message_node = relationship(
    #     "MessageNode",
    #     back_populates="condition_node",
    #     # foreign_keys=[message_node_id],
    # )

    workflow = relationship(
        "Workflow",
        secondary=workflow_condition_association,
        backref="workflow_condition_nodes",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.CONDITION,
        "inherit_condition": (id == Node.id),
    }


class EndNode(Node):
    __tablename__ = "end"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)

    message = Column(String(255), nullable=True)

    # message_node_id = Column(Integer, ForeignKey("message.id"), nullable=True)
    parent_message_node_id = Column(
        Integer, ForeignKey("message.id"), nullable=True
    )

    message_node = relationship(
        "MessageNode",
        # back_populates="end_node",
        foreign_keys=[parent_message_node_id],
    )

    workflow = relationship(
        "Workflow",
        back_populates="end_node",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.END,
    }


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, index=True)

    start_node_id = Column(Integer, ForeignKey("start.id"))
    start_node = relationship(
        "StartNode",
        back_populates="workflow",
        foreign_keys=[start_node_id],
    )

    message_node_ids = Column(String)
    message_nodes = relationship(
        "MessageNode",
        primaryjoin="Workflow.id == workflow_message_association.c.workflow_id",
        secondary=workflow_message_association,
        secondaryjoin="MessageNode.id == workflow_message_association.c.message_node_id",
        backref="workflows",
        # foreign_keys=[message_node_ids],
    )

    condition_node_ids = Column(String)
    condition_nodes = relationship(
        "ConditionNode",
        primaryjoin="Workflow.id == workflow_condition_association.c.workflow_id",
        secondary=workflow_condition_association,
        secondaryjoin="ConditionNode.id == workflow_condition_association.c.condition_node_id",
        backref="workflows",
        # foreign_keys=[condition_node_ids],
    )

    end_node_id = Column(Integer, ForeignKey("end.id"))
    end_node = relationship("EndNode", back_populates="workflow")
