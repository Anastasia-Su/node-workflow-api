from unittest import TestCase
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from src.nodes.crud import crud_condition
from src.nodes.models import ConditionNode
from src.nodes.schemas import ConditionNodeCreate


class TestCreateNode(TestCase):
    def setUp(self):
        self.mock_session = MagicMock(spec=Session)

    def tearDown(self):
        pass

    def test_create_condition_node(self):
        node_data = ConditionNodeCreate(
            condition="status == sent",
            parent_node_id=None,
            parent_message_node_id=None,
            workflow_id=1,
        )

        result = crud_condition.create_condition_node(
            db=self.mock_session, node=node_data
        )

        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once()

        self.assertEqual(result.condition, node_data.condition)
        self.assertEqual(result.workflow_id, node_data.workflow_id)

    @patch("src.nodes.models.ConditionNode")
    def test_get_condition_node_detail_success(self, MockConditionNode):
        mock_node = MagicMock(spec=ConditionNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        result = crud_condition.get_condition_node_detail(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(
            MockConditionNode, node_id
        )
        self.assertEqual(result, mock_node)

    @patch("src.nodes.models.ConditionNode")
    def test_get_condition_node_detail_not_found(self, MockConditionNode):
        self.mock_session.get.return_value = None

        node_id = 1
        result = crud_condition.get_condition_node_detail(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(
            MockConditionNode, node_id
        )
        self.assertIsNone(result)

    @patch("src.nodes.models.ConditionNode")
    def test_update_condition_node(self, MockConditionNode):
        mock_node = MagicMock(spec=ConditionNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        new_node_data = ConditionNodeCreate(
            condition="status == open",
            parent_node_id=None,
            parent_message_node_id=None,
            workflow_id=2,
        )

        result = crud_condition.update_condition_node(
            db=self.mock_session, node_id=node_id, new_node=new_node_data
        )

        self.mock_session.get.assert_called_once_with(
            MockConditionNode, node_id
        )
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(mock_node)

        self.assertEqual(result.condition, new_node_data.condition)
        self.assertEqual(result.workflow_id, new_node_data.workflow_id)

    @patch("src.nodes.models.ConditionNode")
    def test_delete_condition_node(self, MockConditionNode):
        mock_node = MagicMock(spec=ConditionNode)
        self.mock_session.get.return_value = mock_node

        node_id = 1
        result = crud_condition.delete_condition_node(
            db=self.mock_session, node_id=node_id
        )

        self.mock_session.get.assert_called_once_with(
            MockConditionNode, node_id
        )
        self.mock_session.delete.assert_called_once_with(mock_node)
        self.mock_session.commit.assert_called_once()

        self.assertEqual(result, mock_node)
