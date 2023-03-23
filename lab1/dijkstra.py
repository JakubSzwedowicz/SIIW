import heapq
from datetime import datetime
from Utils import Graph, Edge, Criteria, Node
from typing import List, Tuple


def dijkstra(graph: Graph, criteria: Criteria, start: Node):
    costs = {node: float('inf') for node in graph.graph_dict}
    costs[start] = 0
    pq = [(0, start)]
    prev_nodes = {node: None for node in graph.graph_dict}
    while pq:
        curr_cost, curr_node = heapq.heappop(pq)
        if curr_cost > costs[curr_node]:
            continue
        for route in graph.graph_dict[curr_node]:
            if route.time_since_time_zero < curr_cost:
                continue
            waiting_time = route.time_since_time_zero - curr_cost
            new_cost = curr_cost + route.cost + waiting_time
            if new_cost < costs[route.stop]:
                costs[route.stop] = new_cost
                prev_nodes[route.stop] = curr_node
                heapq.heappush(pq, (new_cost, route.stop))
    return costs, prev_nodes


def shortest_path(graph: Graph, start: Node, goal: Node) -> Tuple[float, List[Node]]:
    costs, prev_nodes = dijkstra(graph, Criteria.t, start)
    path: List[Node] = []
    curr_node: Node = goal
    while curr_node is not None:
        path.append(curr_node)
        curr_node = prev_nodes[curr_node]
    path.append(start)
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
