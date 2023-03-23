from datetime import datetime, time
from typing import Dict, List, Tuple, Set, Optional
import csv
from enum import Enum
from queue import PriorityQueue
import heapq

indice_id = 0
indice_company = 1
indice_line = 2
indice_departure_time = 3
indice_arrival_time = 4
indice_start = 5
indice_end = 6
indice_start_lat = 7
indice_start_lon = 8
indice_end_lat = 9
indice_end_lon = 10


class Criteria(Enum):
    t = 0
    p = 1


def clear_row(row: list) -> list:
    bad_time1: str = row[indice_departure_time]
    bad_time2: str = row[indice_arrival_time]
    bad_time1 = str((int(bad_time1[0:2]) % 24)) + bad_time1[2:]
    bad_time2 = str((int(bad_time2[0:2]) % 24)) + bad_time2[2:]
    return [*row[:indice_departure_time], bad_time1, bad_time2, *row[indice_arrival_time + 1:]]


def load_csv(filename: str = 'connection_graph.csv') -> List[tuple]:
    with open(filename, newline='', encoding='utf-8') as f:
        next(f)
        reader = csv.reader(f, delimiter=',')
        data = []
        for row in reader:
            row = clear_row(row)
            data.append((int(row[indice_id]), str(row[indice_company]), str(row[indice_line]),
                         datetime.strptime(row[indice_departure_time], '%H:%M:%S').time(),
                         datetime.strptime(row[indice_arrival_time], '%H:%M:%S').time(), str(row[indice_start]),
                         str(row[indice_end]),
                         float(row[indice_start_lat]), float(row[indice_start_lon]), float(row[indice_end_lat]),
                         float(row[indice_end_lon])))
        return data


class Node:
    def __init__(self, name: str):
        self.name = name
        self.edges: Dict[Node, Edge] = {}

    def add_edge(self, edge):
        self.edges[edge.stop] = edge

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Edge:
    def __init__(self, time_zero: time, start: Node, end: Node, line, departure_time: time,
                 arrival_time: time):
        self.start: Node = start
        self.stop: Node = end
        self.line: Line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.time_since_time_zero = calc_sec(time_zero, departure_time)
        self.cost = calc_sec(departure_time, arrival_time)
        start.add_edge(self)

    def __hash__(self):
        return hash((self.start, self.stop, self.departure_time))

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop and self.departure_time == other.departure_time

    def __repr__(self):
        return f'line: "{self.line.name}", departure bus stop: "{self.start.name}", departure time: "{self.departure_time}", arrival bus stop: "{self.stop.name}", arrival time: "{self.arrival_time}'


class Line:
    def __init__(self, name: str):
        self.name = name
        self.nodes: Set[Node] = set()
        self.edges: Set[Edge] = set()

    def add_node(self, node: Node):
        self.nodes.add(node)

    def add_edge(self, edge: Edge):
        self.edges.add(edge)


class Graph:
    def __init__(self, csv_data: List[Tuple], time_zero):
        self.edges: Set[Edge] = set()
        self.graph_dict: Dict[Node, List[Tuple[int, Edge]]] = {}
        for row in csv_data:
            start: Node = Node(row[indice_start])
            end: Node = Node(row[indice_end])
            start_departure: datetime.time = row[indice_departure_time]
            end_arrival: datetime.time = row[indice_arrival_time]

            edge = Edge(time_zero, start, end, start_departure, end_arrival)

            start.add_edge(edge)
            self.edges.add(edge)
            heapq.heappush(self.graph_dict[start], (edge.cost + edge.time_since_time_zero, edge))

    def get_node(self, name: str) -> Optional[Node]:
        return self.graph_dict[Node(name)][0][1].start if len(self.graph_dict[Node(name)]) != 0 else None


def calc_sec(start: datetime.time, end: datetime.time) -> int:
    start_sec = (start.hour * 60 + start.minute) * 60 + start.second
    end_sec = (end.hour * 60 + end.minute) * 60 + end.second
    full_sec = 24 * 3600
    if start_sec > end_sec:
        diff = full_sec - (start_sec - end_sec)
        return diff
    else:
        diff = end_sec - start_sec
        return diff
