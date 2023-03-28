import csv
from datetime import time, datetime, date
from typing import List
from enum import Enum
from dijkstra import *
from astar import *
from Utils import *
import timeit

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


def task1(graph: Graph, start: str, end: str, start_time: time) -> None:
    begin_time = timeit.default_timer()
    cost, path = dijkstra(graph, start, end, start_time)
    end_time = timeit.default_timer()
    print_result(path, start_time)
    print(f'Execution of Dijkstra algorithm took: {end_time - begin_time}')


def task2(graph: Graph, start: str, end: str, time_zero: time, criteria: Criteria, heuestics: Callable):
    begin_time = timeit.default_timer()
    cost, path = astar(graph, start, end, time_zero, criteria, heuestics)
    end_time = timeit.default_timer()

    print_result(path, time_zero)
    print(f'Execution of A* algorithm took: {end_time - begin_time}')


def main():
    data = load_csv()
    start_time = time(19, 58, 0)

    graph = Graph(data)
    task1(graph, 'KRZYKI', 'Ramiszów', start_time)

    graph = Graph(data)
    task2(graph, 'KRZYKI', 'Ramiszów', start_time, Criteria.t, manhattan_distance)


if __name__ == '__main__':
    main()
