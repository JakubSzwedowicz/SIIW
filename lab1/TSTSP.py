import random
import math

n_cities = 100
n_dimensions = 7
max_iterations = math.ceil(1.1 * (n_cities ** 2))
turns_improved = 0
improve_thresh = 2 * math.floor(math.sqrt(max_iterations))
tabu_list = []
tabu_tenure = n_cities

'''
paramtry:
    iteracje
    iteracje bez poprawy,
    definicja sąsiedztwa,
    definicje tabu
    dlugosc tabu - 
    definicja aspiracja - może być wyznaczona jako jak długo element nie jest usuwany/przemieszczany i znajduje się już na liście
    rozwiązanie początkowe - ma bardzo duży wpłw na jakośc rozwiązania końcowego. np. jeśli minimalizujemy w jakiejś funkcji sukcesu to możemy utknąć w minimum lokalnym. Jego wybór nie powinien trwać zbyt długo
    
Zagadnienia:
    - Czym jest tak naprawdę zamiana miast: 
    - Definicja sąsiedztwa nie musi być stała przez cały algorytm

Co można zmienić?
    - liczba iteracji bez poprawy zmodyfikować "wtedy kiedy poprawa jest mniejsza niż np. 1%" 
    - liczba iteracji bez poprawek
    - definicja sąsiedztwa - tj. w jaki sposób będę skakał po funkcji. (obecnie oglądam sąsiedztwo, ale mógłbym sprawdzać kilka miejsc w całej przestrzeni)
    - Rozwiązanie początokwe zostawić na koniec (korzystamy z metryki więc funkcja jest dość płaska i amplitudy nie są tak duże)
    - definicja sąsiedztwa: można losować węzeł o najmniejszym koście powrotu do punktu startowego
    - zmodyfikuj kod żeby tylko raz wybierać miasto a potem operuj na tym samym zbiorze żeby poróœnywać rozwiązanie (utwórz funkcję przyjmującą tablicę miast jako parametr)
    
Wskazówka do zadań:
    - Ponieważ warunkiem roztrzygającym jest czas to zamiast liczyć przypadki to liczyć minuty
    - można też wybierać miasta z mniejszego obszaru, następnie dodać miasta z innego przesuniętego obszaru i na końcu dodac jakieś inne.
    - Wskazówka jest taka, że jest 7 wymiarów więc przesunięcie nalezy robić we dwóch wybranych koordynatach
    - Zamiana z ostatnim miastem jest spoko gdy już mamy dość optymalne rozwiązanie - wówczas jest ono przydatne w fine tuningu
    - Nie warto ufać użytkownikowi tzn. trzeba dostosowywac input oraz parametry algorytmu dla inputu. Np. powinna być jakaś minimalna liczba iteracji niezależnie od inputu
    
[0:i].reverse(neighbour[i:j]),m[j+1; -1]
tmp = neighbout
for x in range(i, j):
    tmp[x] = neighbout[n - cities - x]

    '''


def distance(city1, city2):
    return math.sqrt(sum([(city1[i] - city2[i]) ** 2 for i in range(n_dimensions)]))


cities = [[random.randint(0, 100) for j in range(n_dimensions)] for i in range(n_cities)]
distances = [[distance(cities[i], cities[j]) for j in range(n_cities)] for i in range(n_cities)]

total = 0
for i in range(n_cities):
    for j in range(n_cities):
        total += distances[i][j]

# Metryczny problem komiwojażera - powinniśmy znaleźcco najwyżej 2 razy rozwiązanie optymalne (dlatego * 2.2)
aspiration_criteria = (total / (n_cities ** 2)) * 2.2

current_solution = list(range(n_cities))
random.shuffle(current_solution)
best_solution = current_solution[:]
best_solution_cost = sum(
    [distances[current_solution[i]][current_solution[(i + 1) % n_cities]] for i in range(n_cities)])

for iteration in range(max_iterations):
    if turns_improved > improve_thresh:
        break
    best_neighbor = None
    best_neighbor_cost = float('inf')
    coordA, coordB = 0, 0
    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            neighbor = current_solution[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbor_cost = sum([distances[neighbor[i]][neighbor[(i + 1) % n_cities]] for i in range(n_cities)])
            if (i, j) not in tabu_list or neighbor_cost < best_neighbor_cost:
                if neighbor_cost < aspiration_criteria:
                    best_neighbor = neighbor[:]
                    best_neighbor_cost = neighbor_cost
                coordA, coordB = i, j
    if best_neighbor is not None:
        current_solution = best_neighbor[:]
        tabu_list.append((coordA, coordB))

        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
        if best_neighbor_cost < best_solution_cost:
            best_solution = best_neighbor[:]
            best_solution_cost = best_neighbor_cost
            turns_improved = 0
        else:
            turns_improved = turns_improved + 1

    print("Iteration {}: Best solution cost = {}".format(iteration, best_solution_cost))

print("Best solution: {}".format(best_solution))
print("Best solution cost: {}".format(best_solution_cost))
