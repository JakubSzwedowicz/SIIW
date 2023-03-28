import heapq
from datetime import datetime
from Utils import Graph, Edge, Criteria
from typing import List, Tuple, Dict


class CriteriaEnforcer:
    def __init__(self, criteria: Criteria, graph: Graph, start: str):
        self.criteria = criteria
        self.edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code
        if self.criteria == Criteria.t:
            self._init_by_time(graph, start)
        elif self.criteria == Criteria.p:
            self._init_by_lines(graph, start)
        else:
            raise Exception(f'Critical error with invalid criteria value: "{criteria}"!')

    def _init_by_time(self, graph: Graph, start: str):
        self.costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
        self.costs[start] = 0


    def _init_by_lines(self, graph: Graph, start: str):
        self.costs = {node: int(1000000) for nodes in graph.lines.values() for node in nodes}  # Pythonic code
        self.lines_to_node: Dict[str: List[str]] = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code
        self.costs[start] = 0

    # def compare_is_left_lower(self, left: Edge, right: [float, str]) -> bool:
    #     if self.criteria == Criteria.t:
    #         return left.time_since_time_zero < right
    #     elif self.criteria == Criteria.p:
    #         return left.


def dijkstra(graph: Graph, criteria: Criteria, start: str) -> Tuple[Dict[str, float], Dict[str, Edge]]:
    # Dict[str, Dict[str, Dict[str, List[Edge]]]] = {}  # line : Dict[start_node: [end_node, edges]]
    costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    pq = [(0, start)]
    while pq:
        curr_cost, curr_node = heapq.heappop(pq)
        if curr_cost > costs[curr_node]:
            continue
        best_new_nodes = {}
        for line, nodes in graph.lines.items():
            if curr_node in nodes:
                for neighbour, edges in nodes[curr_node].items():
                    for edge in edges:
                        if edge.time_since_time_zero < curr_cost:
                            continue
                        waiting_time = edge.time_since_time_zero - curr_cost
                        new_cost = curr_cost + edge.cost + waiting_time
                        if new_cost < costs[edge.stop]:
                            costs[edge.stop] = new_cost
                            edge_to_node[edge.stop] = edge
                            best_new_nodes[edge.stop] = new_cost
        for node, cost in best_new_nodes.items():
            heapq.heappush(pq, (cost, node))
    return costs, edge_to_node


def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[float, List[Edge]]:
    costs, edge_to_node = dijkstra(graph, Criteria.t, start)
    path: List[Edge] = []
    curr_node: str = goal
    while curr_node != start:
        path.append(edge_to_node[curr_node])
        curr_node = edge_to_node[curr_node].start
    path.reverse()
    return costs[goal], path


def manhattan_dist(graph: Graph, node, goal):
    distance, path = shortest_path(graph, node, goal)
    return distance, path


# edges = [
#         ('A', 'B', 2), ('A', 'C', 4), ('B', 'D', 3), ('C', 'D', 1),
#         ('C', 'E', 7), ('D', 'F', 5), ('E', 'F', 4), ('E', 'G', 2),
#         ('F', 'H', 1), ('G', 'H', 2)
# ]
# gg = Graph(edges)
# distance, path = manhattan_dist(gg.graph_dict, 'A', 'H')
# print("Shortest distance:", distance)
# print("Shortest path:", path)
