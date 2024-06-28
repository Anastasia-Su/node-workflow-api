from unittest import TestCase
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from nodes.crud import crud_start
from nodes.models import StartNode
from nodes.schemas import StartNodeCreate


class TestCreateNode(TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)

    def tearDown(self):
        pass

    def test_create_start_node(self):
        node_data = StartNodeCreate(
            message="test",
            workflow_id=1,
        )

        result = crud_start.create_start_node(
            db=self.mock_session, node=node_data
        )

        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once()

        self.assertEqual(result.message, node_data.message)
        self.assertEqual(result.workflow_id, node_data.workflow_id)

    @patch("nodes.models.StartNode")
    def test_get_start_node_detail_success(self, MockStartNode):
        mock_node = MagicMock(spec=StartNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        result = crud_start.get_start_node_detail(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(MockStartNode, node_id)
        self.assertEqual(result, mock_node)

    @patch("nodes.models.StartNode")
    def test_get_start_node_detail_not_found(self, MockStartNode):
        self.mock_session.get.return_value = None

        node_id = 1
        result = crud_start.get_start_node_detail(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(MockStartNode, node_id)
        self.assertIsNone(result)

    @patch("nodes.models.StartNode")
    def test_update_start_node(self, MockStartNode):
        mock_node = MagicMock(spec=StartNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        new_node_data = StartNodeCreate(
            message="updated",
            workflow_id=2,
        )

        result = crud_start.update_start_node(
            db=self.mock_session, node_id=node_id, new_node=new_node_data
        )

        self.mock_session.get.assert_called_once_with(MockStartNode, node_id)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_node)

        self.assertEqual(result.message, new_node_data.message)
        self.assertEqual(result.workflow_id, new_node_data.workflow_id)

    @patch("nodes.models.StartNode")
    def test_delete_start_node(self, MockStartNode):
        mock_node = MagicMock(spec=StartNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        result = crud_start.delete_start_node(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(MockStartNode, node_id)
        self.mock_session.delete.assert_called_once_with(mock_node)
        self.mock_session.commit.assert_called_once()

        self.assertEqual(result, mock_node)
