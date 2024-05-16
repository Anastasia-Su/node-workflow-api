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


class StartNode(Base):
    __tablename__ = "start"

    id = Column(Integer, primary_key=True, autoincrement=True)

    message_node_id = Column(
        Integer, ForeignKey("message.id"), nullable=True, unique=True
    )
    message_node = relationship(
        "MessageNode",
        back_populates="start_node",
        foreign_keys=[message_node_id],
    )


class MessageNode(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(MessageStatuses), nullable=False)
    text = Column(String(511), nullable=False)

    condition_node = relationship(
        "ConditionNode",
        back_populates="message_node",
    )

    start_node = relationship(
        "StartNode",
        back_populates="message_node",
    )

    end_node_id = Column(Integer, ForeignKey("end.id"), nullable=True)
    end_node = relationship(
        "EndNode",
        foreign_keys=[end_node_id],
    )


class ConditionNode(Base):
    __tablename__ = "condition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    condition = Column(String, nullable=False)

    message_node_id = Column(
        Integer, ForeignKey("message.id"), nullable=True, unique=True
    )
    message_node = relationship(
        "MessageNode",
        back_populates="condition_node",
        foreign_keys=[message_node_id],
    )


class EndNode(Base):
    __tablename__ = "end"

    id = Column(Integer, primary_key=True, autoincrement=True)

    message_node_id = Column(Integer, ForeignKey("message.id"), nullable=True)
    # message_node = relationship(
    #     "MessageNode",
    #     back_populates="end_node",
    #     foreign_keys=[message_node_id],
    # )
