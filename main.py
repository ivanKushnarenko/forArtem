import networkx as nx
import matplotlib.pyplot as plt

import algorithms


# graph1 = nx.Graph()
# graph1.add_nodes_from([i for i in range(5)])
# graph1.add_edges_from([(0, 1), (1, 2), (1, 4), (2, 3), (2, 4)])

graph2 = nx.binomial_tree(5)
pos = nx.shell_layout(graph2)
# nx.draw(graph2, with_labels=True)
# plt.show()


def bfs_demo():
    # pos = nx.kamada_kawai_layout(graph1)
    # plt.subplot(221)
    # nx.draw(graph1, with_labels=True, pos=pos)
    # plt.subplot(222)
    # res_graph = algorithms.path_to_graph(graph1,
    #                                      algorithms.bfs(graph1, 0))
    # edge_labels = {(v, u): res_graph.get_edge_data(v, u).get('weight')
    #                for (v, u) in res_graph.edges
    #                if res_graph.get_edge_data(v, u).get('weight') is not None}
    # nx.draw_networkx_edge_labels(res_graph, pos, edge_labels=edge_labels)
    # nx.draw(res_graph, with_labels=True, pos=pos)

    pos = nx.spring_layout(graph2)
    plt.subplot(121)
    nx.draw(graph2, pos=pos, with_labels=True)
    plt.subplot(122)
    res_G = algorithms.path_to_graph(graph2, algorithms.bfs(graph2, 0))
    edge_labels = {(v, w): res_G.get_edge_data(v, w).get('weight')
                   for (v, w) in res_G.edges
                   if res_G.get_edge_data(v, w).get('weight') is not None}
    nx.draw_networkx_edge_labels(res_G, pos, edge_labels=edge_labels)
    nx.draw(res_G, with_labels=True, pos=pos)


    plt.show()


bfs_demo()
