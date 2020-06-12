""" Module provides some algorithms on graphs. """

import random

import networkx as nx
import numpy as np

from priority_queue import PriorityQueue


def bfs(graph, start, goal=None):

    """
    Implements breadth-first search from start node to goal(if given).

    :param graph: networkx.Graph()
    :param start: vertex to start search from
    :param goal: (optional) vertex where search ends, default: None
                 if default search stops when all vertices are visited
    :return: generator that gives vertices in bfs-order
    :raise KeyError: if 'start' is not in 'graph' or
                     'goal' is provided and is not in 'graph'
    """

    if start not in graph:
        raise KeyError('bfs: Start vertex not in graph')
    if goal is not None and goal not in graph:
        raise KeyError('bfs: Given goal vertex not in graph')

    graph_dict = nx.to_dict_of_lists(graph)
    queue = [start]
    if goal is None:
        for v in queue:
            queue.extend([i for i in graph_dict[v] if i not in queue])
            yield v
    else:
        for v in queue:
            if v == goal:
                yield v
                break
            queue.extend([i for i in graph_dict[v] if i not in queue])
            yield v


def dfs(graph, start, goal=None):

    """
    Implements depth-first search from start node to goal(if given).

    :param graph: networkx.Graph()
    :param start: vertex to start search from
    :param goal: (optional) vertex where search ends, default: None
                 if default search stops when all vertices are visited
    :return: generator that gives vertices in dfs-order
    :raise KeyError: if 'start' is not in 'graph' or
                     'goal' is provided and is not in 'graph'
    """

    if start not in graph:
        raise KeyError('dfs: Start vertex not in graph')
    if goal is not None and goal not in graph:
        raise KeyError('dfs: Given goal vertex not in graph')

    graph_dict = nx.to_dict_of_lists(graph)
    queue = [start]
    visited = []
    while queue:
        v = queue.pop(0)
        if goal is not None and v == goal:
            yield v
            break
        if v in visited:
            continue
        visited.append(v)
        queue[0:0] = [i for i in graph_dict[v] if i not in visited]
        yield v


def prim(graph, start=None):

    """
    Prim's algorithm that builds minimum spanning tree(mst).

    :param graph: networkx.Graph, weighted graph
    :param start: (optional), default:None
                  vertex to start building of mst from
    :return: networkx.Graph, mst
    :raise KeyError: if start is not None and is not in graph
    """

    if start is not None and start not in graph:
        raise KeyError('prim: Start vertex is not in graph')
    graph_dict = nx.to_dict_of_dicts(graph)

    result = nx.Graph()
    result.add_nodes_from(graph.nodes)
    visited = [start if start is not None else random.choice(graph_dict.keys())]
    unvisited = list(graph.nodes)
    unvisited.remove(visited[0])

    while unvisited:
        edges_with_weights = []
        for v in visited:
            adjacent_edges = [(v, u_i, graph_dict[v][u_i]['weight'])
                              for u_i in graph_dict[v] if u_i in unvisited]
            edges_with_weights.extend(adjacent_edges)
        min_edge = _edge_with_min_weight(edges_with_weights)
        result.add_weighted_edges_from([min_edge])
        visited.append(min_edge[1])
        unvisited.remove(min_edge[1])
    return result


def _edge_with_min_weight(list_of_weighted_edges):
    temp = (0, 0, None)
    for i in list_of_weighted_edges:
        if temp[2] is None or i[2] < temp[2]:
            temp = i
    return temp


def dijkstra(graph, start, goal=None, return_length=False):

    """
    Finds shortest paths from 'goal' to every vertex in graph.


    :param graph: networkx.Graph, weighted graph
    :param start: vertex in graph to find paths from
    :param goal: (optional) default: None,
                 vertex for last vertex in path
    :param return_length: (optional), default=False
                        if True: returns lengths of paths alongside path
    :return: if not return_length:
                path dict: keys - vertices of 'graph',
                      values - list with path from 'start' to this vertex
             if return_length: tuple(path dict, length dict)
                length dict: keys - vertices of 'graph',
                      values - length of path from 'start' to this vertex
             if goal is not None:
                returns value of one of those dict for key 'goal'
    :raise KeyError: if start is not in graph or
                            goal is given and is not in graph
    """

    if start not in graph:
        raise KeyError('dijkstra: Start vertex is not in graph')
    if goal is not None and goal not in graph:
        raise KeyError('dijkstra: Given goal vertex is not in graph')
    graph_dict = nx.to_dict_of_dicts(graph)

    visited = {}
    unvisited = {i: float('Inf') for i in graph.nodes}
    unvisited[start] = 0
    paths = {start: [start]}

    while unvisited:
        v = min(unvisited, key=unvisited.get)
        _dijkstra_step(graph_dict, v, visited, unvisited, paths)
        # mark_v = unvisited[v]
        # for u in graph_dict[v]:
        #     if u in visited:
        #         continue
        #     mark = mark_v + graph_dict[v][u]['weight']
        #     if mark < unvisited[u]:
        #         unvisited[u] = mark
        #         paths[u] = paths[v] + [u]
        # visited[v] = unvisited.pop(v)
    if return_length:
        return paths, visited if goal is None else paths[goal], visited[goal]
    return paths if goal is None else paths[goal]


def a_star(graph, start, goal, heuristic):
    assert start in graph and goal in graph,\
        "A*: Start or goal vertex are not in graph"
    dict_g = nx.to_dict_of_dicts(graph)

    queue = PriorityQueue()
    queue.put(start, 0)
    path = []
    marks = {start: 0}

    while queue:
        v = queue.get()
        for u in dict_g[v]:
            if u == goal:
                break
            if u in path:
                continue
            mark = v + dict_g[v][u]['weight']
            if u not in marks or mark < marks[u]:
                marks[u] = mark
            queue.put(u, mark + heuristic(u, goal))
            path.append(v)
    return path


def bidirectional_dijkstra(graph, start, goal, return_length=False):
    assert start in graph and goal in graph, \
        "Bidirectional Dijkstra: Start or goal vertex are not in graph"
    dict_g = nx.to_dict_of_dicts(graph)

    # in variables' names '_f' and '_r' stand for forward and reversed direction
    marks_f = {i: float('Inf') for i in graph.nodes}
    marks_f[start] = 0
    visited_f = {}
    path_f = {start: [start]}

    marks_r = {i: float('Inf') for i in graph.nodes}
    marks_r[goal] = 0
    visited_r = {}
    path_r = {goal: [goal]}

    common_v = None
    while True:
        current_f = min(marks_f, key=marks_f.get)
        _dijkstra_step(dict_g, current_f, visited_f, marks_f, path_f)
        if current_f in visited_r:
            common_v = current_f
            break

        current_r = min(marks_r, key=marks_r.get)
        _dijkstra_step(dict_g, current_r, visited_r, marks_r, path_r)
        if current_r in visited_f:
            common_v = current_r
            break

    min_path = marks_f[common_v] + marks_r[common_v]
    common_edge = None
    for v in visited_f:
        for u in visited_r:
            if u in dict_g[v] and marks_f[v] + dict_g[v][u] + marks_r[u] < min_path:
                min_path = marks_f[v] + dict_g[v][u] + marks_r[u]
                common_edge = (v, u)

    shortest_path = marks_f[common_edge[0]] + marks_r[common_edge[1]][::-1]
    return shortest_path, min_path


def _dijkstra_step(graph_dict, current_v, visited_dict,
                   marks_dict, path_dict):

    """
    :param graph_dict: dict[list], adjacency dict
    :param current_v: current vertex in dijkstra algorithm
    :param visited_dict: keys: already visited vertices
                         values: length of shortest path from start vertex to this
    :param marks_dict: keys: marked, but not visited vertices
                       values: current marks vor vertex
    :param path_dict: keys: vertices
                      values: list of shortest path from start vertex
    """

    mark_v = marks_dict[current_v]
    for next_vertex in graph_dict[current_v]:
        if next_vertex in visited_dict:
            continue
        new_mark = mark_v + graph_dict[current_v][next_vertex]['weight']
        if new_mark < marks_dict[next_vertex]:
            marks_dict[next_vertex] = new_mark
            path_dict[next_vertex] = path_dict[current_v] + [next_vertex]
    visited_dict[current_v] = marks_dict.pop(current_v)
