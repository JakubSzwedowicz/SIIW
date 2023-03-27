import csv
from datetime import time
from typing import List
from enum import Enum
from dijkstra import *
# from astar import *
from Utils import *

'''Deadline na środę 22.03 godzina 7:30

Na sprawko:
    - Nie wrzucać kodu, ale żeby było jasne co w kodzie jest
    - nie pisać o wczytnaiu danych,
    - Opisać preprocessing (np. przedstawienie grafu przy pomocy macierzy sąsiedztwa). Można jednym zdaniem
    - Zamysł algorytmu żeby wykazac jakie parametry są dla nas istotne, jakie przyjmują wartości i dlaczego takie. DLaczego takie sąsiedzwo wybraliśmy, dlaczego jest lepsze od innych - tutaj jest tabelka porównawcza na podstawie testów)
    - Dodać źródła  uzasadniające dlaczego korzystamy z danego kodu, heurystyki, parametróœ - podać uzasadnienie czemu korzystamy z tego a nie tamtego (ale raczej to poróœnując różne źródła)
    - Zestawienie wyników finalnych, czyli wynik testów na zbiorze,
    - poza kodem załączyć niestandardwoe biblioteki (wystarczą requirements.txt),
    - Wszelkie uzasadnienia w sprawku czemu rozwiązanie jest super mile widziane, 
    
Review po 23.03 do sprawek:
    - Robić jak inżynierkę (podobne zasady),
    - podpisywać wykresy, schematy, tabele, pisać uzasadnienie po co jest ta tabela,
    
    
'''




def task1(start: str, end: str, criteria: Criteria, start_time: time) -> None:
    data = load_csv()

    graph = Graph(data, start_time)
    start = graph.get_node(start)
    end = graph.get_node(end)

    cost, path = shortest_path(graph, start, end)
    print_result(cost, path, start_time)


def print_result(cost, path, start_time: time) -> None:
    time = start_time
    previousNode = path[0]
    for node in path[1:]:
        print(previousNode.edges[node])


def task2(graph):
    pass


def main():
    task1('Krzyki', 'Rymarksa', Criteria.t, time(19, 58, 0))
    # task2(graph)
    #   def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):


if __name__ == '__main__':
    main()
