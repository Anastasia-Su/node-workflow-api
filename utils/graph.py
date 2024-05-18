import textwrap
import networkx as nx
from matplotlib import pyplot
from nodes import models


def graph_build(
    start_node: models.StartNode,
    message_nodes: list[models.MessageNode],
    condition_nodes: list[models.ConditionNode],
    end_nodes: list[models.EndNode],
) -> None:

    G = nx.Graph()
    G.add_node(start_node)
    G.add_nodes_from(message_nodes)
    G.add_nodes_from(condition_nodes)
    G.add_nodes_from(end_nodes)

    node_color_map = {
        models.StartNode: "lightgreen",
        models.MessageNode: "lightblue",
        models.ConditionNode: "lightyellow",
        models.EndNode: "lightcoral",
    }

    labels = {}
    colors = []
    for node in G.nodes:
        if isinstance(node, models.StartNode):
            labels[node] = (
                f"Start Node\nMessage: {node.message}\nID: {node.id}"
            )
            colors.append(node_color_map[models.StartNode])

        elif isinstance(node, models.MessageNode):
            labels[node] = (
                f"Message Node\nStatus: {node.status}\nText: {node.text}\nID: {node.id}"
            )
            colors.append(node_color_map[models.MessageNode])

        elif isinstance(node, models.ConditionNode):
            labels[node] = (
                f"Condition Node\nCondition: {node.condition}\nID: {node.id}"
            )
            colors.append(node_color_map[models.ConditionNode])

        elif isinstance(node, models.EndNode):
            labels[node] = f"End Node\nMessage: {node.message}\nID: {node.id}"
            colors.append(node_color_map[models.EndNode])

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos=pos,
        with_labels=False,
        node_color=colors,
        linewidths=1,
        edgecolors="black",
    )

    for node, (x, y) in pos.items():
        text = labels[node]
        wrapped_text = "\n".join(textwrap.wrap(text, width=15))
        pyplot.text(
            x,
            y,
            wrapped_text,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=10,
            bbox=dict(
                facecolor=node_color_map[type(node)],
                boxstyle="round,pad=0.3",
            ),
        )

    pyplot.show()
    # pyplot.savefig("workflow_graph.png")
