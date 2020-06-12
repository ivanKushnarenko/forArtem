import time
import networkx as nx
import matplotlib.pyplot as plt

import algorithms as a


gr = open(r'USA-road-d.NY.co\USA-road-d.NY.gr')
G = nx.OrderedDiGraph()
count = 0
repeated = 0
for line in gr:
    count += 1
    if count >= 722500:
        break
    if line == '':
        continue
    if 8 <= count:
        lst = line.split()
        if G.has_edge(int(lst[1]), int(lst[2])):
            repeated += 1
        else:
            G.add_edge(int(lst[1]), int(lst[2]), weight=int(lst[3]))


gr.close()
print(f'line proccessed: {count}')
print('Graph is builded:')
print(f'nodes: {len(G.nodes)}')
print(f'edges: {len(G.edges)}')
print(f'repeated edges: {repeated}')


def test_bfs():
    g1 = nx.complete_graph(10)
    print('with goal: [', end='')
    for v in a.bfs(g1, 0, 4):
        print(v, end=' ')
    print(']')
    print('no goal: [', end='')
    for v in a.bfs(g1, 0):
        print(v, end=' ')
    print(']')
    nx.draw(g1, with_labels=True)
    plt.show()

    g2 = nx.Graph()
    g2.add_nodes_from([i for i in range(10)])
    g2.add_edges_from([(0, 1), (1, 3), (1, 4), (1, 5), (0, 2), (2, 5), (2, 6),
                       (2, 7), (2, 8), (2, 9)])
    print('with goal: [', end='')
    for v in a.bfs(g2, 0, 6):
        print(v, end=' ')
    print(']')
    print('no goal: [', end='')
    for v in a.bfs(g2, 0):
        print(v, end=' ')
    print(']')
    nx.draw(g2, with_labels=True)
    plt.show()

    plt.close()


def test_dfs():
    g1 = nx.complete_graph(4)
    g1.remove_edge(1, 2)
    print('existing:', a.dfs(g1, 0, 3))
    print('not existing:', a.dfs(g1, 0, 20))
    nx.draw(g1, with_labels=True)
    plt.show()

    g2 = nx.Graph()
    g2.add_nodes_from([i for i in range(10)])
    g2.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (4, 5),
                       (4, 8), (2, 6), (2, 7), (3, 7), (7, 9)])
    print('existing:', a.dfs(g2, 0, 5))
    print('not existing:', a.dfs(g2, 0, 14))
    nx.draw(g2, with_labels=True)
    plt.show()

    plt.close()


def test_prim():
    g1 = nx.Graph()
    g1.add_nodes_from([i for i in range(6)])
    g1.add_weighted_edges_from([(0, 2, 4), (0, 4, 8), (1, 2, 3), (1, 4, 5), (1, 3, 6),
                                (2, 5, 12), (3, 5, 9), (4, 5, 1)])
    plt.subplot(121)
    pos = nx.spring_layout(g1)
    nx.draw(g1, pos=pos, with_labels=True)
    plt.subplot(122)
    nx.draw(a.prim(g1, 0), pos=pos, with_labels=True)
    plt.show()


def test_dijkstra():
    g1 = nx.Graph()
    g1.add_nodes_from([i for i in range(6)])
    g1.add_weighted_edges_from([(0, 2, 4), (0, 4, 8), (1, 2, 3), (1, 4, 5), (1, 3, 6),
                                (2, 5, 12), (3, 5, 9), (4, 5, 1)])

    min_paths_dict = a.dijkstra(g1, 0)
    new_nodes = {i: (i, j) for i, j in min_paths_dict.items()}
    nx.relabel_nodes(g1, new_nodes, copy=False)
    pos = nx.spring_layout(g1)
    nx.draw(g1, pos=pos, with_labels=True)
    labels = {(u, v): g1.get_edge_data(u, v).get('weight') for (u, v) in g1.edges}
    nx.draw_networkx_edge_labels(g1, pos=pos, edge_labels=labels)
    plt.show()


time1 = time.time()
for i in a.bfs(G, 1):
    pass
time2 = time.time()
print(f'time = {time2 - time1}')
