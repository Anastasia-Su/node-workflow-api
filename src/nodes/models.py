from enum import auto, StrEnum

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from database.database_setup import Base


class MessageStatuses(StrEnum):
    PENDING = auto()
    SENT = auto()
    OPEN = auto()


class NodeTypes(StrEnum):
    START = auto()
    MESSAGE = auto()
    CONDITION = auto()
    CONDITION_EDGE = auto()
    END = auto()


class ConditionEdges(StrEnum):
    YES = auto()
    NO = auto()


class Node(Base):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True, autoincrement=True)
    node_type = Column(Enum(NodeTypes))

    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": node_type,
    }


class ConditionEdge(Base):
    __tablename__ = "condition_edge"

    id = Column(Integer, primary_key=True)
    condition_node_id = Column(
        Integer,
        ForeignKey(
            "condition.id",
            use_alter=True,
            ondelete="CASCADE",
        ),
    )
    edge = Column(Enum(ConditionEdges))


class StartNode(Node):
    __tablename__ = "start"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    message = Column(String(255), nullable=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflow.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    workflow = relationship(
        "Workflow", back_populates="start_node", passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.START,
    }


class MessageNode(Node):
    __tablename__ = "message"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    status = Column(Enum(MessageStatuses), nullable=False)
    text = Column(String(511), nullable=False)

    parent_node_id = Column(
        Integer,
        ForeignKey("node.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    parent_condition_edge_id = Column(
        Integer,
        ForeignKey("condition_edge.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflow.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    workflow = relationship(
        "Workflow", back_populates="message_nodes", passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.MESSAGE,
        "inherit_condition": (id == Node.id),
    }


class ConditionNode(Node):
    __tablename__ = "condition"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    condition = Column(String(255), nullable=False)

    parent_node_id = Column(
        Integer,
        ForeignKey("node.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    parent_message_node_id = Column(
        Integer,
        ForeignKey("message.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    edge = relationship(
        "ConditionEdge",
        uselist=False,
        backref="condition",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflow.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    workflow = relationship(
        "Workflow", back_populates="condition_nodes", passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.CONDITION,
        "inherit_condition": (id == Node.id),
    }


class EndNode(Node):
    __tablename__ = "end"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)

    message = Column(String(255), nullable=True)

    parent_node_id = Column(
        Integer,
        ForeignKey("message.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflow.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    workflow = relationship(
        "Workflow", back_populates="end_nodes", passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.END,
    }


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    start_node = relationship(
        "StartNode",
        back_populates="workflow",
        uselist=False,
    )

    message_nodes = relationship("MessageNode", back_populates="workflow")

    condition_nodes = relationship("ConditionNode", back_populates="workflow")

    end_nodes = relationship("EndNode", back_populates="workflow")
