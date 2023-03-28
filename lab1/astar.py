import heapq
import math
from Utils import *
from datetime import time


def astar(start: str, goal: str, neighbors_fn, heuristic_fn):
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while front:
        _, current = heapq.heappop(front)
        
        if current == goal:
            break
        
        for neighbor in neighbors_fn(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_fn(goal, neighbor)
                heapq.heappush(front, (priority, neighbor))
                came_from[neighbor] = current
    
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    
    return path, cost_so_far[goal]


def astar_time(graph: Graph, criteria: Criteria, start: str, goal: str, heurestic_fn) -> Tuple[Dict[str, float], Dict[str, Edge]]:
    # Dict[str, Dict[str, Dict[str, List[Edge]]]] = {}  # line : Dict[start_node: [end_node, edges]]
    costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    costs[start] = 0
    pq = [(0, 0, start)]
    while pq[0][2] != goal:
        _, curr_cost, curr_node = heapq.heappop(pq)
        if curr_cost > costs[curr_node]:
            continue
        best_new_nodes: Dict[str, (float, float)] = {}
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
                            priority = new_cost + heurestic_fn(graph.nodes[edge.stop], graph.nodes[goal])
                            best_new_nodes[edge.stop] = (priority, new_cost)
        for node, prio_cost in best_new_nodes.items():
            heapq.heappush(pq, (*prio_cost, node))
    return costs, edge_to_node

def astar_lines(graph: Graph, criteria: Criteria, start: str, goal: str, heurestic_fn) -> Tuple[Dict[str, float], Dict[str, Edge]]:
    # Dict[str, Dict[str, Dict[str, List[Edge]]]] = {}  # line : Dict[start_node: [end_node, edges]]
    costs = {node: float('inf') for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    edge_to_node = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code
    line_to_node: Dict[str, Tuple[str, int]] = {node: None for nodes in graph.lines.values() for node in nodes}  # Pythonic code

    costs[start] = 0
    for line, nodes in graph.lines:
        if start in nodes:
            line_to_node[start] = (line, 0)
            break

    pq = [(0, 0, start)]
    while pq[0][2] != goal:
        curr_cost_lines, curr_time, curr_node = heapq.heappop(pq)
        if curr_time > costs[curr_node]:
            continue
        best_new_nodes: Dict[str, (float, float)] = {}
        for line, nodes in graph.lines.items():
            if curr_node in nodes:
                for neighbour, edges in nodes[curr_node].items():
                    for edge in edges:
                        if edge.time_since_time_zero < curr_time or edge.line != line_to_node[curr_node][0]:
                            continue
                        waiting_time = edge.time_since_time_zero - curr_time
                        new_cost = curr_time + edge.cost + waiting_time
                        if new_cost < costs[edge.stop]:
                            costs[edge.stop] = new_cost
                            edge_to_node[edge.stop] = edge
                            priority = new_cost + heurestic_fn(graph.nodes[edge.stop], graph.nodes[goal])
                            best_new_nodes[edge.stop] = (priority, new_cost)
        for node, prio_cost in best_new_nodes.items():
            heapq.heappush(pq, (*prio_cost, node))
    return costs, edge_to_node
    # def a_star_lines(graph: Graph, start: str, goal: str, actual_time: datetime.time):
    #     frontier = PriorityQueue()
    #     frontier.put(start, 0)
    #
    #     came_from: dict[str, (Optional[str], (str, datetime.time))] = {}
    #     cost_so_far: dict[str, float] = {}
    #     time_so_far: dict[str, datetime.time] = {}
    #     line_so_far: dict[str, str] = {}
    #
    #     came_from[start] = None
    #     cost_so_far[start] = 0
    #     time_so_far[start] = actual_time
    #     line_so_far[start] = ""
    #
    #     while not frontier.empty():
    #         current: str = frontier.get()
    #
    #         if current == goal:
    #             break
    #
    #         try:
    #             graph.neighbors(current)
    #         except KeyError:
    #             continue
    #
    #         for next in graph.neighbors(current):
    #             cost_with_route = graph.cost_lines(current, next, time_so_far[current], line_so_far[current])
    #             if cost_with_route is None:
    #                 continue
    #             new_cost = cost_so_far[current] + cost_with_route[0]
    #
    #             if next not in cost_so_far or new_cost < cost_so_far[next]:
    #                 cost_so_far[next] = new_cost
    #                 priority = new_cost + heurisitc(graph, current, next)
    #                 frontier.put(next, priority)
    #                 came_from[next] = current, cost_with_route[1]
    #                 time_so_far[next] = cost_with_route[1][2]
    #                 line_so_far[next] = cost_with_route[1][0]
    #
    #     return came_from, cost_so_far

    # path = []
    # current = goal
    # while current != start:
    #     path.append(current)
    #     current = came_from[current]
    # path.append(start)
    # path.reverse()
    #
    # return path, cost_so_far[goal]


def manhattan_distance(a: Node, b: Node):
    return abs(a.lat - b.lat) + abs(a.lon - b.lon)


def euclidean_distance(a: Node, b: Node):
   return math.sqrt((a.lat - b.lat) ** 2 + (a.lon - b.lon) ** 2)


def towncenter_distance(a, b):
    return euclidean_distance(a, (0, 0, 0, 0, 0, 0, 0))+euclidean_distance((0, 0, 0, 0, 0, 0, 0), b)


def unidimensional_distance(a: Node,b: Node):
    return max(abs(a.lat - b.lat), abs(a.lon - b.lon))


def cosine_distance(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(x ** 2 for x in b))
    return 1 - (dot_product / (magnitude_a * magnitude_b))


def chebyshev_distance(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def astar_time_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[float, List[Edge]]:
    costs, edge_to_node = astar_time(graph, Criteria.t, start, goal, manhattan_distance)
    path: List[Edge] = []
    curr_node: str = goal
    while curr_node != start:
        path.append(edge_to_node[curr_node])
        curr_node = edge_to_node[curr_node].start
    path.reverse()
    return costs[goal], path


if __name__ == '__main__':
    graph = {
    (0, 0, 0, 0, 0, 0, 0): [(1, 1, 1, 1, 1, 1, 1), (1, 2, 3, 4, 5, 6, 7), (4, 5, 6, 7, 8, 9, 10),(5, 6, 7, 8, 6, 5, 1)],
    (1, 2, 3, 4, 5, 6, 7): [(2, 3, 4, 5, 6, 7, 8), (1, 1, 1, 1, 1, 1, 1), (5, 2, 1, 4, 1, 3, 1)],
    (2, 3, 4, 5, 6, 7, 8): [(3, 4, 5, 6, 7, 8, 9), (2, 4, 2, 1, 4, 1, 8), (1, 2, 3, 4, 5, 6, 7),(5, 6, 7, 8, 6, 5, 1),(6, 6, 10, 2, 2, 5, 10), (9, 3, 2, 7, 0, 0, 1), (9, 9, 2, 0, 2, 1, 9)],
    (3, 4, 5, 6, 7, 8, 9): [(4, 5, 6, 7, 8, 9, 10)],
    (4, 5, 6, 7, 8, 9, 10): [],
    (1, 1, 1, 1, 1, 1, 1): [(2, 2, 2, 2, 2, 2, 2), (5, 2, 1, 4, 1, 3, 1), (6, 6, 10, 2, 2, 5, 10), (10, 10, 10, 10, 10, 10, 10)],
    (2, 2, 2, 2, 2, 2, 2): [],
    (5, 2, 1, 4, 1, 3, 1): [(2, 2, 2, 2, 2, 2, 2), (2, 0, 2, 0, 2, 0, 2), (2, 4, 2, 1, 4, 1, 8), (3, 4, 5, 6, 7, 8, 9), (9, 9, 2, 0, 2, 1, 9)],
    (2, 0, 2, 0, 2, 0, 2): [],
    (2, 2, 2, 2, 2, 2, 2): [(2, 3, 4, 5, 6, 7, 8), (2, 2, 2, 2, 2, 2, 2), (4, 5, 6, 7, 8, 9, 10), (5, 6, 7, 8, 6, 5, 1), (10, 10, 10, 10, 10, 10, 10)],
    (3, 3, 2, 0, 1, 0, 1): [(1, 2, 3, 4, 5, 6, 7), (2, 2, 2, 2, 2, 2, 2), (2, 3, 4, 5, 6, 7, 8), (5, 2, 1, 4, 1, 3, 1), (2, 0, 2, 0, 2, 0, 2), (6, 6, 10, 2, 2, 5, 10), (2, 2, 2, 2, 2, 2, 2)],
    (5, 6, 7, 8, 6, 5, 1): [(2, 0, 2, 0, 2, 0, 2), (3, 4, 5, 6, 7, 8, 9)],
    (6, 6, 10, 2, 2, 5, 10): [(2, 0, 2, 0, 2, 0, 2), (1, 1, 1, 1, 1, 1, 1)],
    (2, 4, 2, 1, 4, 1, 8): [(1, 2, 3, 4, 5, 6, 7), (5, 2, 1, 4, 1, 3, 1), (2, 0, 2, 0, 2, 0, 2)],
    (9, 3, 2, 7, 0, 0, 1): [(5, 2, 1, 4, 1, 3, 1), (10, 10, 10, 10, 10, 10, 10)],
    (9, 9, 2, 0, 2, 1, 9): [(2, 0, 2, 0, 2, 0, 2), (10, 10, 10, 10, 10, 10, 10)], 
    (10, 10, 10, 10, 10, 10, 10): [(2, 0, 2, 0, 2, 0, 2), (3, 4, 5, 6, 7, 8, 9)]
}
    
    start = (1, 2, 3, 4, 5, 6, 7)
    goal = (10, 10, 10, 10, 10, 10, 10)
    
    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: manhattan_distance(a, b))
    print(f"Path using Manhattan distance heuristic: {path}")
    print(f"Cost using Manhattan distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: euclidean_distance(a, b))
    print(f"Path using Euclid's distance heuristic: {path}")
    print(f"Cost using Euclid's distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: towncenter_distance(a, b))
    print(f"Path using Towncenter distance heuristic: {path}")
    print(f"Cost using Towncenter distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: unidimensional_distance(a, b))
    print(f"Path using unidimensional distance heuristic: {path}")
    print(f"Cost using unidimensional distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: cosine_distance(a, b))
    print(f"Path using cosine distance heuristic: {path}")
    print(f"Cost using cosine distance heuristic: {cost}")    

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: chebyshev_distance(a, b))
    print(f"Path using Chebyshev distance heuristic: {path}")
    print(f"Cost using Chebyshev distance heuristic: {cost}")    