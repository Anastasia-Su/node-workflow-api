from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from enum import auto, Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAEnum
from sqlalchemy.orm import relationship

from starlette.testclient import TestClient

from dependencies import get_db
from main import app
from tests.load_mock_data_for_tests import load_mock_data, insert_mock_data

Base = declarative_base()

from enum import auto, StrEnum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base


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
    id = Column(Integer, primary_key=True)
    node_type = Column(Enum(NodeTypes))

    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": node_type,
    }


class ConditionEdge(Base):
    __tablename__ = "condition_edge"

    id = Column(Integer, primary_key=True, autoincrement=True)
    condition_node_id = Column(Integer, ForeignKey("condition.id"))
    edge = Column(Enum(ConditionEdges))


class StartNode(Node):
    __tablename__ = "start"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    message = Column(String(255), nullable=True)

    workflow_id = Column(Integer, ForeignKey("workflow.id"), nullable=True)

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
    parent_condition_edge_id = Column(
        Integer, ForeignKey("condition_edge.id"), nullable=True
    )

    workflow_id = Column(Integer, ForeignKey("workflow.id"), nullable=True)
    workflow = relationship(
        "Workflow",
        back_populates="message_nodes",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.MESSAGE,
        "inherit_condition": (id == Node.id),
    }


class ConditionNode(Node):
    __tablename__ = "condition"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    condition = Column(String, nullable=False)

    parent_node_id = Column(Integer, ForeignKey("node.id"), nullable=True)
    parent_message_node_id = Column(
        Integer, ForeignKey("message.id"), nullable=True
    )
    edge = relationship("ConditionEdge", uselist=False, backref="condition")

    workflow_id = Column(Integer, ForeignKey("workflow.id"), nullable=True)

    workflow = relationship(
        "Workflow",
        back_populates="condition_nodes",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.CONDITION,
        "inherit_condition": (id == Node.id),
    }


class EndNode(Node):
    __tablename__ = "end"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)

    message = Column(String(255), nullable=True)

    parent_node_id = Column(Integer, ForeignKey("message.id"), nullable=True)

    workflow_id = Column(Integer, ForeignKey("workflow.id"), nullable=True)

    workflow = relationship(
        "Workflow",
        back_populates="end_nodes",
    )

    __mapper_args__ = {
        "polymorphic_identity": NodeTypes.END,
    }


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    start_node = relationship(
        "StartNode", back_populates="workflow", uselist=False
    )

    message_nodes = relationship(
        "MessageNode",
        back_populates="workflow",
    )

    condition_nodes = relationship(
        "ConditionNode",
        back_populates="workflow",
    )

    end_nodes = relationship(
        "EndNode",
        back_populates="workflow",
    )


#
# # Create an in-memory SQLite database engine
# engine = create_engine(
#     "sqlite:///:memory:", connect_args={"check_same_thread": False}
# )
#
# # Create a sessionmaker bound to the engine
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # Create tables in the in-memory database
# Base.metadata.create_all(bind=engine)
#
# # Create a scoped session
# db = scoped_session(SessionLocal)

# Mock data instances
# mock_data_start_node = Node(id=1, node_type=NodeTypes.START)
# mock_data_start = StartNode(id=1, message="Starting", workflow_id=1)
#
# mock_data_start2_node = Node(id=2, node_type=NodeTypes.START)
# mock_data_start2 = StartNode(id=2, message="Starting", workflow_id=1)
#
# mock_data_existing_node = Node(id=3, node_type=NodeTypes.MESSAGE)
# mock_data_existing = MessageNode(
#     id=3,
#     status=MessageStatuses.PENDING,
#     text="Existing message node",
#     parent_node_id=1,
#     parent_condition_edge_id=0,
#     workflow_id=1,
# )
#
# mock_data_existing2_node = Node(id=4, node_type=NodeTypes.MESSAGE)
# mock_data_existing2 = MessageNode(
#     id=4,
#     status=MessageStatuses.PENDING,
#     text="Existing message node 2",
#     parent_node_id=2,
#     parent_condition_edge_id=0,
#     workflow_id=1,
# )

# Add mock data to the session
# db.add_all(
#     [
#         mock_data_start_node,
#         mock_data_start,
#         mock_data_start2_node,
#         mock_data_start2,
#         mock_data_existing_node,
#         mock_data_existing,
#         mock_data_existing2_node,
#         mock_data_existing2,
#     ]
# )
#
#
# data = load_mock_data("mock_db.json")
# insert_mock_data(db, data)
# db.commit()
#
#
# # Override the get_db dependency in your app
# def override_get_db():
#     try:
#         yield db
#     finally:
#         db.remove()
#
#
# app.dependency_overrides[get_db] = override_get_db
#
# # Create a TestClient
# client = TestClient(app)
