from datetime import datetime, time, date
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
    def __init__(self, name: str, latitude: float, lontitude: float):
        self.name = name
        self.lat = latitude
        self.lon = lontitude

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Edge:
    def __init__(self, start: str, end: str, line: str, departure_time: time,
                 arrival_time: time):
        self.start: str = start
        self.stop: str = end
        self.line: str = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self._time_since_time_zero = None
        self.cost = calc_sec(departure_time, arrival_time)

    def clear_time_since_zero(self):
        self._time_since_time_zero = None

    def time_since_time_zero(self, time_zero: time):
        if self._time_since_time_zero is None:
            self._time_since_time_zero = calc_sec(time_zero, self.departure_time)
        return self._time_since_time_zero

    def __lt__(self, other):
        return self.departure_time < other.departure_time

    def __repr__(self):
        return f'line: "{self.line}", departure bus stop: "{self.start}", departure time: "{self.departure_time}", arrival bus stop: "{self.stop}", arrival time: "{self.arrival_time}'


# class Line:
#     def __init__(self, name: str):
#         self.name = name
#         self.nodes: Set[Node] = set()
#         self.edges: Set[Edge] = set()
#
#     def add_node(self, node: Node):
#         self.nodes.add(node)
#
#     def add_edge(self, edge: Edge):
#         self.edges.add(edge)


class Graph:
    def __init__(self, csv_data: List[Tuple]):
        self.lines: Dict[str, Dict[str, Dict[str, List[Edge]]]] = {} # line : Dict[start_node: [end_node, edges]]
        self.nodes: Dict[str, Node] = {}
        self._build_graph(csv_data)
        self._sort_edges()

    def clear_time_since_zero(self):
        for nodes in self.lines.values():
            for node in nodes.values():
                for edges in node.values():
                    for edge in edges:
                        edge.clear_time_since_zero()

    def _build_graph(self, csv_data: List[Tuple]):
        for row in csv_data:
            start: str = row[indice_start]
            end: str = row[indice_end]
            line: str = row[indice_line]
            start_departure: datetime.time = row[indice_departure_time]
            end_arrival: datetime.time = row[indice_arrival_time]

            edge = Edge(start, end, line, start_departure, end_arrival)
            if line not in self.lines:
                self.lines[line] = {}
                
            if start not in self.lines[line]:
                self.lines[line][start] = {}

            if end not in self.lines[line]:
                self.lines[line][end] = {}

            if end not in self.lines[line][start]:
                self.lines[line][start][end] = []

            self.lines[line][start][end].append(edge)

            if start not in self.nodes:
                self.nodes[start] = Node(start, row[indice_start_lat], row[indice_start_lon])
            if end not in self.nodes:
                self.nodes[end] = Node(end, row[indice_end_lat], row[indice_end_lon])

    def _sort_edges(self):
        for line, nodes in self.lines.items():
            for node, neighbours in nodes.items():
                for neighbour, edges_to_neighbour in neighbours.items():
                    edges_to_neighbour.sort()


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


def print_result(path: List[Edge], start_time: time) -> None:
    start_datetime = datetime.combine(date.today(), start_time)
    end_datetime = datetime.combine(date.today(), path[-1].arrival_time)
    total_time = end_datetime - start_datetime
    line_changes = 0
    if path is not None:
        line_of_prev_edge = path[0].line
        for edge in path:
            if edge.line != line_of_prev_edge:
                line_changes += 1
                line_of_prev_edge = edge.line

    for edge in path:
        print(edge)
    print(f'Whole trip will take {total_time.seconds / 60} minues across {len({edge.line for edge in path})} lines and {line_changes} line changes')
