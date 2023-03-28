import heapq
from datetime import datetime
from Utils import Graph, Edge, Criteria
from typing import List, Tuple, Dict


def dijkstra(graph: Graph, criteria: Criteria, start: str) -> Tuple[Dict[str, float], Dict[str, Edge]]:
    costs = {node: float('inf') for node in graph.nodes}
    costs[start] = 0
    pq = [(0, start)]
    edge_to_node = {node: None for node in graph.nodes}
    while pq:
        curr_cost, curr_node = heapq.heappop(pq)
        if curr_cost > costs[curr_node]:
            continue
        for neighbour, edges in graph.nodes[curr_node].items():
            new_node = None
            for edge in edges:
                if edge.time_since_time_zero < curr_cost:
                    continue
                waiting_time = edge.time_since_time_zero - curr_cost
                new_cost = curr_cost + edge.cost + waiting_time
                if new_cost < costs[edge.stop]:
                    costs[edge.stop] = new_cost
                    edge_to_node[edge.stop] = edge
                    new_node = (new_cost, edge.stop)
                    break;
            if new_node is not None:
                heapq.heappush(pq, new_node)
    return costs, edge_to_node


def shortest_path(graph: Graph, start: str, goal: str) -> Tuple[float, List[Edge]]:
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
