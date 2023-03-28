import heapq
import math
from Utils import *
from datetime import time
from typing import Callable, Dict, Tuple, List


def astar(graph: Graph, start: str, goal: str, time_zero: time, criteria: Criteria, heurestics: Callable) -> Tuple[float, List[Edge]]:
    return _astar_shortest_path(graph, start, goal, time_zero, criteria, heurestics)


def manhattan_distance(a: Node, b: Node) -> float:
    return abs(a.lat - b.lat) + abs(a.lon - b.lon)


def euclidean_distance(a: Node, b: Node) -> float:
   return math.sqrt((a.lat - b.lat) ** 2 + (a.lon - b.lon) ** 2)


def towncenter_distance(a: Node, b: Node) -> float:
    return euclidean_distance(a, Node("", 0, 0))+euclidean_distance(Node("", 0, 0), b)


def unidimensional_distance(a: Node, b: Node) -> float:
    return max(abs(a.lat - b.lat), abs(a.lon - b.lon))


def cosine_distance(a: Node, b: Node) -> float:
    dot_product = a.lon * b.lon + a.lat * b.lat
    magnitude_a = math.sqrt(a.lon ** 2 + a.lat ** 2)
    magnitude_b = math.sqrt(b.lon ** 2 + b.lat ** 2)
    return 1 - (dot_product / (magnitude_a * magnitude_b))


def chebyshev_distance(a: Node, b: Node) -> float:
    return max(abs(a.lon - b.lon), abs(a.lat - b.lat))


def _astar_shortest_path(graph: Graph, start: str, goal: str, time_zero: time, criteria: Criteria, heurestics: Callable) -> Tuple[float, List[Edge]]:
    costs = None
    edge_to_node = None

    if criteria == Criteria.t:
        costs, edge_to_node = _astar_time(graph, start, goal, time_zero, heurestics)
    elif criteria == Criteria.p:
        costs, edge_to_node = _astar_lines(graph, start, goal, time_zero, heurestics)

    path: List[Edge] = []
    curr_node: str = goal
    while curr_node != start:
        path.append(edge_to_node[curr_node])
        curr_node = edge_to_node[curr_node].start
    path.reverse()
    return costs[goal], path


def _astar_time(graph: Graph, start: str, goal: str, time_zero: time, heurestic_fn) -> Optional[Tuple[Dict[str, float], Dict[str, Edge]]]:
    f_costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    g_costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code

    f_costs[start] = 0
    g_costs[start] = 0
    # Priority, curr_cost (time), curr_node
    pq = [(0, 0, start)]
    while pq:
        _, curr_time, curr_node = heapq.heappop(pq)
        if curr_node == goal:
            return f_costs, edge_to_node

        if curr_time > g_costs[curr_node]:
            continue
        best_new_nodes: Dict[str, (float, float)] = {}
        # Dict[str, Dict[str, Dict[str, List[Edge]]]] = {}  # line : Dict[start_node: [end_node, edges]]
        for line, nodes in graph.lines.items():
            if curr_node in nodes:
                for neighbour, edges in nodes[curr_node].items():
                    for edge in edges:
                        time_since_zero = edge.time_since_time_zero(time_zero)
                        if time_since_zero < curr_time:
                            continue
                        waiting_time = time_since_zero - curr_time
                        new_cost = curr_time + waiting_time + edge.cost
                        if new_cost < g_costs[edge.stop]:
                            g_costs[edge.stop] = new_cost
                            magic_number = 100000
                            f_costs[edge.stop] = new_cost + magic_number * heurestic_fn(graph.nodes[edge.stop], graph.nodes[goal])
                            edge_to_node[edge.stop] = edge
                            heapq.heappush(pq, (f_costs[edge.stop], new_cost, edge.stop))
                            best_new_nodes[edge.stop] = (f_costs[edge.stop], new_cost)
        for node, prio_cost in best_new_nodes.items():
            heapq.heappush(pq, (*prio_cost, node))
    return None


def _astar_lines(graph: Graph, start: str, goal: str, time_zero: time, heurestic_fn) -> Tuple[Dict[str, float], Dict[str, Edge]]:
    f_costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    g_costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code

    f_costs[start] = 0
    g_costs[start] = 0

    # priority, curr_line, node
    pq = [(0, '', start)]
    while pq[0][2] != goal:
        curr_cost_lines, curr_line, curr_node = heapq.heappop(pq)

        best_new_nodes: Dict[str, (float, float)] = {}
        # Dict[str, Dict[str, Dict[str, List[Edge]]]] = {}  # line : Dict[start_node: [end_node, edges]]
        for line, nodes in graph.lines.items():
            if curr_node in nodes:
                for neighbour, edges in nodes[curr_node].items():
                    for edge in edges:
                        g = g_costs[curr_node]
                        if curr_line != edge.line:
                            g += 10

                        if g < g_costs[edge.stop]:
                            g_costs[edge.stop] = g
                            f_costs[edge.stop] = g + heurestic_fn(graph.nodes[edge.stop], graph.nodes[goal])
                            edge_to_node[edge.stop] = edge

                            best_new_nodes[edge.stop] = (f_costs[edge.stop], edge.line)
        for node, prio_cost in best_new_nodes.items():
            heapq.heappush(pq, (*prio_cost, node))
    return f_costs, edge_to_node
