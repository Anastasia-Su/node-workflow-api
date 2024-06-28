from unittest import TestCase
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from nodes.crud import crud_message
from nodes.models import MessageNode, MessageStatuses
from nodes.schemas import MessageNodeCreate


class TestCreateNode(TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)

    def tearDown(self):
        pass

    def test_create_message_node(self):
        node_data = MessageNodeCreate(
            status=MessageStatuses.PENDING,
            text="Test message",
            parent_node_id=None,
            parent_condition_edge_id=None,
            workflow_id=1,
        )

        result = crud_message.create_message_node(
            db=self.mock_session, node=node_data
        )

        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once()

        self.assertEqual(result.status, node_data.status)
        self.assertEqual(result.text, node_data.text)
        self.assertEqual(result.workflow_id, node_data.workflow_id)

    @patch("nodes.models.MessageNode")
    def test_get_message_node_detail_success(self, MockMessageNode):
        mock_node = MagicMock(spec=MessageNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        result = crud_message.get_message_node_detail(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(MockMessageNode, node_id)
        self.assertEqual(result, mock_node)

    @patch("nodes.models.MessageNode")
    def test_get_message_node_detail_not_found(self, MockMessageNode):
        self.mock_session.get.return_value = None

        node_id = 1
        result = crud_message.get_message_node_detail(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(MockMessageNode, node_id)
        self.assertIsNone(result)

    @patch("nodes.models.MessageNode")
    def test_update_message_node(self, MockMessageNode):
        mock_node = MagicMock(spec=MessageNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        new_node_data = MessageNodeCreate(
            status=MessageStatuses.SENT,
            text="Updated message",
            parent_node_id=None,
            parent_condition_edge_id=None,
            workflow_id=2,
        )

        result = crud_message.update_message_node(
            db=self.mock_session, node_id=node_id, new_node=new_node_data
        )

        self.mock_session.get.assert_called_once_with(MockMessageNode, node_id)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_node)

        self.assertEqual(result.status, new_node_data.status)
        self.assertEqual(result.text, new_node_data.text)
        self.assertEqual(result.workflow_id, new_node_data.workflow_id)

    @patch("nodes.models.MessageNode")
    def test_delete_message_node(self, MockMessageNode):
        mock_node = MagicMock(spec=MessageNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        result = crud_message.delete_message_node(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(MockMessageNode, node_id)
        self.mock_session.delete.assert_called_once_with(mock_node)
        self.mock_session.commit.assert_called_once()

        self.assertEqual(result, mock_node)
