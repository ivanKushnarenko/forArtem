import random
import time

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

g = nx.Graph()
g.add_nodes_from([i for i in range(10)])
g.add_edges_from([(1, 6), (3, 5), (6, 0), (1, 7), (8, 9), (9, 4), (3, 4), (4, 1), (2, 4)])


colors = ['r', 'g', 'y', 'm', 'b']

pos1 = nx.circular_layout(g)
pos2 = nx.circular_layout(g)
fig, ax = plt.subplots()

# nx.draw(g, ax=ax, pos=pos1, with_labels=True, node_color=[random.choice(colors) for i in range(10)])
# plt.show()
# time.sleep(1)
# ax.clear()
# nx.draw(g, ax=ax, pos=pos1, with_labels=True, node_color=[random.choice(colors) for i in range(10)])


def animate(i):
    nx.draw(g, ax=ax, pos=pos1, with_labels=True,
            node_color=[random.choice(colors) for i in range(10)])


animation = FuncAnimation(fig, animate, frames=2, interval=1000, blit=False)
plt.show()
