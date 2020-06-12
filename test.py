import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
import networkx.algorithms.traversal.depth_first_search as dfs
import networkx.algorithms.traversal.breadth_first_search as bfs

g = nx.Graph()
g.add_node(1)
g.add_node(1)
g.add_edge(2, 3)
nx.draw(g, with_labels=True)
plt.show()
