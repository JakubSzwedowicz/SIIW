from reversi import *
from typing import Callable, Optional


class Node:
    def __init__(self, game_state: GameState):
        self.children: List[Node] = []
        self.game_state: GameState = game_state
        self.best_child: Optional[Node] = None
        self.best_child_heuristic_value: Optional[int] = None
        self.heuristic_value: Optional[int] = None

    def add_child(self, child) -> None:
        self.children.append(child)

    def calculate_heuristic(self, heuristic_func: Callable[[GameState], int]) -> int:
        self.heuristic_value = heuristic_func(self.game_state)
        return self.heuristic_value


class Tree:
    def __init__(self):
        self.root: Node = Node(GameState())
        self.best_moves: List[Tuple[int, int]] = []
        self.best_nodes: List[Node] = []
        self.depth = 0

    def generate_results(self) -> None:
        self.best_moves = []
        self.best_nodes = []

        node = self.root
        while node is not None:
            self.best_nodes.append(node)
            self.best_moves.append(node.game_state.made_move)
            node = node.best_child

    def print_tree(self, amount: Optional[int] = float('inf')) -> None:
        for node in self.best_nodes:
            print(f'Turn number: {node.game_state.turn_number}, current_player: {node.game_state.current_player}, moves_watcher bricked: {node.game_state.move_watcher.bricked}, child_heuristic: {node.best_child_heuristic_value}, heuristic: {node.heuristic_value}, moves_watcher unsymm_moves: {node.game_state.move_watcher.unsymmetrical_moves}')
            node.game_state.print_board()


