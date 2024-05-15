from enum import auto, StrEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from database import Base


class MessageStatuses(StrEnum):
    PENDING = auto()
    SENT = auto()
    OPENED = auto()


association_table = Table(
    "association",
    Base.metadata,
    Column("source_id", Integer, ForeignKey("nodes.id")),
    Column("target_id", Integer, ForeignKey("nodes.id")),
)


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)

    incoming_nodes = relationship(
        "Node",
        secondary=association_table,
        primaryjoin=id == association_table.c.target_id,
        secondaryjoin=id == association_table.c.source_id,
        backref="outgoing_nodes",
    )

    __mapper_args__ = {"polymorphic_identity": "node", "polymorphic_on": type}


class StartNode(Base):
    __tablename__ = "start"

    id = Column(Integer, ForeignKey("nodes.id"), primary_key=True)

    output_node_id = Column(Integer, ForeignKey("nodes.id"))
    output_node = relationship(
        "Node", foreign_keys=[output_node_id], uselist=False
    )

    __mapper_args__ = {"polymorphic_identity": "start"}


class MessageNode(Base):
    __tablename__ = "message"

    id = Column(Integer, ForeignKey("nodes.id"), primary_key=True)
    status = Column(Enum(MessageStatuses), nullable=False)
    text = Column(String(511), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "message"}


class ConditionNode(Base):
    __tablename__ = "condition"

    id = Column(Integer, ForeignKey("nodes.id"), primary_key=True)
    condition = Column(String, nullable=False)

    yes_node_id = Column(Integer, ForeignKey("nodes.id"))
    yes_node = relationship("Node", foreign_keys=[yes_node_id])

    no_node_id = Column(Integer, ForeignKey("nodes.id"))
    no_node = relationship("Node", foreign_keys=[no_node_id])

    previous_message_id = Column(Integer, ForeignKey("message.id"))
    previous_message = relationship("MessageNode")

    __mapper_args__ = {"polymorphic_identity": "condition"}


class EndNode(Base):
    __tablename__ = "end"

    id = Column(
        Integer, ForeignKey("nodes.id"), primary_key=True, autoincrement=True
    )

    input_node_id = Column(Integer, ForeignKey("nodes.id"))
    input_node = relationship("Node", foreign_keys=[input_node_id])

    __mapper_args__ = {"polymorphic_identity": "end"}
