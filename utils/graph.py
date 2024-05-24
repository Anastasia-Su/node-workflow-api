import textwrap
import networkx as nx
from matplotlib import pyplot as plt


def build_graph(G: nx.DiGraph) -> None:
    plt.figure(figsize=(10, 8))
    node_color_map = {
        "Start": "lightgreen",
        "Message": "lightblue",
        "Condition": "lightyellow",
        "End": "lightcoral",
    }

    labels = {}
    colors = []
    for node, data in G.nodes(data=True):
        label_parts = [f"ID: {node}", data["label"]]

        if "message" in data:
            label_parts.append(f"Message: {data['message']}")
        if "status" in data:
            label_parts.append(f"Status: {data['status']}")
            label_parts.append(f"Text: {data['text']}")

        if "condition" in data:
            label_parts.append(f"{data['condition']}")

        labels[node] = "\n".join(label_parts)

        colors.append(node_color_map[data["label"]])

    # If you prefer different layout, uncomment one of the following.
    pos = nx.spring_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.spectral_layout(G)

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

    plt.show()
    # plt.savefig("workflow_graph.png", bbox_inches="tight")
    plt.close()
