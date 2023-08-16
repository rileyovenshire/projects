# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Description: This program takes a matrix as input and outputs a graph visualization using NetworkX and pyplot.

import matplotlib.pyplot as plt
import networkx as nx


def visualize_graph(adjacency_matrix):
    # networkx graph object
    G = nx.Graph()

    num_nodes = len(adjacency_matrix)

    G.add_nodes_from(range(num_nodes))

    # add edges based on the adjacency matrix
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_matrix[i][j] != 0:
                G.add_edge(i, j)

    # draw the graph using NetworkX and pyplot
    pos = nx.spring_layout(G)  # positions of nodes for visualization
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=10, font_color='black')
    plt.title("Graph Visualization")
    plt.show()


# example matrix

G = [
    [0, 2, 3, 20, 1],
    [2, 0, 15, 2, 20],
    [3, 15, 0, 20, 13],
    [20, 2, 20, 0, 9],
    [1, 20, 13, 9, 0],
]

visualize_graph(G)
