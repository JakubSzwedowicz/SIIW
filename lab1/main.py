import dijkstra
from astar import astar
import csv

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
'''

def main():

    pass

def load_csv(filename: str = 'connection_graph.csv') -> dijkstra.Graph:
    with open(filename, 'r') as f:
        writer = csv.writer()

if __name__ == '__main__':
    main()

