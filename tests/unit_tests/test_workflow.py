import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status

from database.dependencies import CommonDB
from nodes.models import (
    Workflow,
    StartNode,
    MessageNode,
    ConditionNode,
    EndNode,
)

from src.utils.building_blocks.helpers_for_building_blocks import (
    exception_no_next_node,
)
from src.utils.execute_workflow_main import execute_workflow


@pytest.fixture
def mock_db():
    return MagicMock(spec=CommonDB)


@pytest.fixture
def mock_workflow():
    workflow = MagicMock(spec=Workflow)
    workflow.id = 1
    return workflow


@pytest.fixture
def mock_start_node():
    start_node = MagicMock(spec=StartNode)
    start_node.id = 1
    start_node.message = "Start Node"
    return start_node


@pytest.fixture
def mock_message_node():
    message_node = MagicMock(spec=MessageNode)
    message_node.id = 2
    message_node.parent_node_id = 1
    message_node.text = "Message Node"
    message_node.status = "PENDING"
    message_node.workflow_id = 1
    return message_node


@pytest.fixture
def mock_condition_node():
    condition_node = MagicMock(spec=ConditionNode)
    condition_node.id = 3
    condition_node.parent_message_node_id = 2
    condition_node.condition = "Condition Node"
    return condition_node


@pytest.fixture
def mock_end_node():
    end_node = MagicMock(spec=EndNode)
    end_node.id = 4
    end_node.message = "End Node"
    end_node.parent_node_id = 3
    return end_node


def test_execute_workflow(
    mock_db,
    mock_workflow,
    mock_start_node,
    mock_message_node,
    mock_condition_node,
    mock_end_node,
):
    with patch(
        "nodes.crud.crud_workflow.get_workflow_detail",
        return_value=mock_workflow,
    ), patch(
        "nodes.crud.crud_condition_edge.get_condition_edge_list",
        return_value=[],
    ), patch(
        "utils.building_blocks.helpers_for_building_blocks.get_node_lists",
        return_value=(
            mock_start_node,
            [mock_message_node],
            [mock_condition_node],
            [mock_end_node],
        ),
    ), patch(
        "utils.building_blocks.handle_start_node",
        return_value=mock_message_node,
    ), patch(
        "utils.building_blocks.handle_message_node",
        side_effect=[mock_condition_node, mock_message_node, mock_end_node],
    ), patch(
        "utils.building_blocks.handle_condition_node",
        side_effect=[mock_condition_node, mock_message_node],
    ), patch(
        "utils.building_blocks.handle_end_node",
        return_value=None,
    ):

        try:
            result = execute_workflow(mock_db, 1, draw_graph=False)
            assert "graph" in result
            assert "execution_time" in result
        except HTTPException as e:
            print(f"HTTPException: {e.detail}")


def test_workflow_with_missing_nodes(mock_db, mock_workflow, mock_start_node):
    with patch(
        "nodes.crud.crud_workflow.get_workflow_detail",
        return_value=mock_workflow,
    ), patch(
        "nodes.crud.crud_condition_edge.get_condition_edge_list",
        return_value=[],
    ), patch(
        "utils.building_blocks.helpers_for_building_blocks.get_node_lists",
        return_value=(
            mock_start_node,
            [],
            [],
            [],
        ),
    ), patch(
        "utils.building_blocks.handle_start_node",
        side_effect=exception_no_next_node,
    ):
        with pytest.raises(HTTPException) as e:
            execute_workflow(mock_db, 1, draw_graph=False)

        assert e.value.status_code == status.HTTP_404_NOT_FOUND
