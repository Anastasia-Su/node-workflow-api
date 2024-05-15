from enum import auto, StrEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from database import Base


class MessageStatuses(StrEnum):
    PENDING = auto()
    SENT = auto()
    OPENED = auto()


class NodeTypes(StrEnum):
    START = auto()
    MESSAGE = auto()
    CONDITION = auto()
    END = auto()


association_table = Table(
    "association",
    Base.metadata,
    Column("source_id", Integer, ForeignKey("nodes.id")),
    Column("target_id", Integer, ForeignKey("nodes.id")),
)


class Association(Base):
    __tablename__ = "association"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # source_type = Column(Enum(NodeTypes), nullable=False)
    # target_type = Column(Enum(NodeTypes), nullable=False)

    start_id = Column(Integer)
    message_id = Column(Integer)
    condition_id = Column(Integer)
    end_id = Column(Integer)

    start_node = relationship(
        "StartNode",
        foreign_keys=[start_id],
        back_populates="start_associations",
    )
    message_node = relationship(
        "MessageNode",
        foreign_keys=[message_id],
        back_populates="message_associations",
    )
    condition_node = relationship(
        "ConditionNode",
        foreign_keys=[condition_id],
        back_populates="condition_associations",
    )
    end_node = relationship(
        "EndNode", foreign_keys=[end_id], back_populates="end_associations"
    )
    # incoming_nodes = relationship(
    #     "Association",
    #     secondary=association_table,
    #     primaryjoin=id == association_table.c.target_id,
    #     secondaryjoin=id == association_table.c.source_id,
    #     backref="outgoing_nodes",
    # )


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(NodeTypes), nullable=False)

    incoming_associations = relationship(
        "Association",
        foreign_keys="[Association.target_id]",
        back_populates="target_node",
    )

    outgoing_associations = relationship(
        "Association",
        foreign_keys="[Association.source_id]",
        back_populates="source_node",
    )

    __mapper_args__ = {"polymorphic_identity": "node", "polymorphic_on": type}


class StartNode(Node):
    __tablename__ = "start"

    id = Column(
        Integer, ForeignKey("nodes.id"), primary_key=True, autoincrement=True
    )

    output_node_id = Column(Integer, ForeignKey("nodes.id"))
    output_node = relationship(
        "Node", foreign_keys=[output_node_id], uselist=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "start",
        "inherit_condition": id == Node.id,
    }


class MessageNode(Node):
    __tablename__ = "message"

    id = Column(
        Integer, ForeignKey("nodes.id"), primary_key=True, autoincrement=True
    )
    status = Column(Enum(MessageStatuses), nullable=False)
    text = Column(String(511), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "message",
        "inherit_condition": id == Node.id,
    }


class ConditionNode(Node):
    __tablename__ = "condition"

    id = Column(
        Integer, ForeignKey("nodes.id"), primary_key=True, autoincrement=True
    )
    condition = Column(String, nullable=False)

    yes_node_id = Column(Integer, ForeignKey("nodes.id"))
    yes_node = relationship("Node", foreign_keys=[yes_node_id])

    no_node_id = Column(Integer, ForeignKey("nodes.id"))
    no_node = relationship("Node", foreign_keys=[no_node_id])

    previous_message_id = Column(Integer, ForeignKey("message.id"))
    previous_message = relationship(
        "MessageNode", foreign_keys=[previous_message_id]
    )

    __mapper_args__ = {
        "polymorphic_identity": "condition",
        "inherit_condition": id == Node.id,
    }


class EndNode(Node):
    __tablename__ = "end"

    id = Column(
        Integer, ForeignKey("nodes.id"), primary_key=True, autoincrement=True
    )

    input_node_id = Column(Integer, ForeignKey("nodes.id"))
    input_node = relationship("Node", foreign_keys=[input_node_id])

    __mapper_args__ = {
        "polymorphic_identity": "end",
        "inherit_condition": id == Node.id,
    }
