import timeit
import sys
from typing import Callable
from datetime import time
from dijkstra import dijkstra
from astar import astar, manhattan_distance, euclidean_distance, chebyshev_distance
from Utils import Graph, print_result, Criteria, load_csv

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


def task1(start: str, end: str, start_time: time) -> None:
    data = load_csv()
    graph = Graph(data)
    begin_time = timeit.default_timer()
    cost, path = dijkstra(graph, start, end, start_time)
    end_time = timeit.default_timer()

    print_result(path, start_time)
    print(f'Dijkstra: Cost function "{cost}", execution time "{end_time - begin_time}" seconds', file=sys.stderr)


def task2(start: str, end: str, time_zero: time, criteria: Criteria, heuestics: Callable):
    data = load_csv()
    graph = Graph(data)
    begin_time = timeit.default_timer()
    cost, path = astar(graph, start, end, time_zero, criteria, heuestics)
    end_time = timeit.default_timer()

    print_result(path, time_zero)
    print(f'A* with criteria "{criteria.name}": Cost function "{cost}", execution time "{end_time - begin_time}" seconds', file=sys.stderr)


def main():
    start_time = time(19, 58, 0)
    begin = "Hynka"
    end = 'Malinowskiego'

    task1(begin, end, start_time)
    task2(begin, end, start_time, Criteria.t, manhattan_distance)
    task2(begin, end, start_time, Criteria.t, euclidean_distance)
    task2(begin, end, start_time, Criteria.t, chebyshev_distance)
    task2(begin, end, start_time, Criteria.p, manhattan_distance)


if __name__ == '__main__':
    main()
