import heapq
from datetime import datetime, time
from Utils import Graph, Edge, Criteria
from typing import List, Tuple, Dict


def dijkstra(graph: Graph, start: str, goal: str, time_zero: time) -> Tuple[float, List[Edge]]:
    return _dijkstra_shortest_path(graph, start, goal, time_zero)


def _dijkstra_shortest_path(graph: Graph, start: str, goal: str, time_zero: time) -> Tuple[float, List[Edge]]:
    costs, edge_to_node = _dijkstra_time(graph, start, time_zero)
    path: List[Edge] = []
    curr_node: str = goal
    while curr_node != start:
        path.append(edge_to_node[curr_node])
        curr_node = edge_to_node[curr_node].start
    path.reverse()
    return costs[goal], path


def _dijkstra_time(graph: Graph, start: str, time_zero: time) -> Tuple[Dict[str, float], Dict[str, Edge]]:
    # Dict[str, Dict[str, Dict[str, List[Edge]]]] = {}  # line : Dict[start_node: [end_node, edges]]
    costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    visited = set()

    pq = [(0, start)]
    while pq:
        curr_cost, curr_node = heapq.heappop(pq)
        if curr_node in visited:
            continue
        else:
            visited.add(curr_node)

        if curr_cost > costs[curr_node]:
            continue
        best_new_nodes = {}
        for line, nodes in graph.lines.items():
            if curr_node in nodes:
                for neighbour, edges in nodes[curr_node].items():
                    for edge in edges:
                        time_since_zero = edge.time_since_time_zero(time_zero)
                        if time_since_zero < curr_cost:
                            continue
                        waiting_time = time_since_zero - curr_cost
                        new_cost = curr_cost + edge.cost + waiting_time
                        if new_cost < costs[edge.stop]:
                            costs[edge.stop] = new_cost
                            edge_to_node[edge.stop] = edge
                            best_new_nodes[edge.stop] = new_cost
        for node, cost in best_new_nodes.items():
            heapq.heappush(pq, (cost, node))
    return costs, edge_to_node
