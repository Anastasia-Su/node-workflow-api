import logging

from networkx import DiGraph
from src.nodes.models import EndNode


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def handle_end_node(G: DiGraph, current_node: EndNode) -> None:
    logger.debug("End Node Logic")
    G.add_node(current_node.id, label="End", message=current_node.message)
