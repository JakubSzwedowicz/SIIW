from tree import Tree
from algorithms import Algorithm, SolvingAlgorithm, heuristic_game_score, heuristic_favour_number_of_moves, \
    heuristic_favour_corners
import cProfile
import timeit
from utils import read_board


def run_benchmark(alg: Algorithm, tree: Tree, depth: int = 10) -> None:
    try:
        print(f'{"=" * 50}\nRunning algorithm "{alg.alg.name}" and heuristic "{str(alg.heuristic).split()[1]}" with depth {depth}, working... ')
        start = timeit.default_timer()
        alg.traverse_tree(tree, depth)
        end = timeit.default_timer()
        print('Finished!')
        tree.best_nodes[-1].game_state.print_board()
        print(f'Last node: \n{tree.best_nodes[-1]}')
        print(f'The execution took {end - start}[s], visited nodes {alg.visited_nodes}')
    except Exception as ex:
        print(ex)
    # tree.print_tree()


def run_all_benchmarks():
    heurestics = (heuristic_game_score, heuristic_favour_corners, heuristic_favour_number_of_moves)
    solving_algorithms = (SolvingAlgorithm.minimax, SolvingAlgorithm.alpha_beta)
    # board = read_board()
    tree = Tree()
    min_depth = 5
    max_depth = 12
    for depth in range(min_depth, max_depth):
        for alg in solving_algorithms:
            for h in heurestics:
                run_benchmark(Algorithm(h, alg), tree, depth)


def run_profiler():
    alg = Algorithm(heuristic_game_score, SolvingAlgorithm.minimax)
    tree = Tree()
    depth = 10
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    run_benchmark(alg, tree, depth)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()


def main():
    # run_all_benchmarks()
    # Comment above and uncomment the line below to see the profiler output from different function calls
    run_profiler()


if __name__ == '__main__':
    main()
