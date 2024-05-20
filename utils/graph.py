import textwrap
import networkx as nx
from matplotlib import pyplot as plt


def build_graph(G: nx.DiGraph) -> None:
    plt.figure(figsize=(10, 8))
    node_color_map = {
        "Start Node": "lightgreen",
        "Message Node": "lightblue",
        "Condition Node": "lightyellow",
        "End Node": "lightcoral",
    }

    labels = {}
    colors = []
    for node, data in G.nodes(data=True):
        labels[node] = f"{data['label']}\nID: {node}"
        if "message" in data:
            labels[node] += f"\nMessage: {data['message']}"
        if "status" in data:
            labels[node] += f"\nStatus: {data['status']}\nText: {data['text']}"
        if "condition" in data:
            labels[node] += f"\nCondition: {data['condition']}"

        colors.append(node_color_map[data["label"]])

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
        plt.text(
            x,
            y,
            wrapped_text,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=12,
            bbox=dict(
                facecolor=node_color_map[G.nodes[node]["label"]],
                boxstyle="round,pad=0.3",
            ),
        )

    edge_labels = nx.get_edge_attributes(G, "label")

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14)

    # plt.show()
    plt.savefig("workflow_graph.png", bbox_inches="tight")
    plt.close()
