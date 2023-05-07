from tree import Tree, Node
from reversi import GameState
from typing import Callable
from enum import Enum


class SolvingAlgorithm(Enum):
    minimax = 0
    alpha_beta = 1


class Algorithm:
    def __init__(self, heuristic: Callable[[GameState], int], solving_alg: SolvingAlgorithm):
        self.heuristic = heuristic
        self.alg = solving_alg
        self.max_depth = 3

    def traverse_tree(self, tree: Tree, depth: int) -> None:
        tree.depth = depth
        self.max_depth = depth
        res = []
        if self.alg == SolvingAlgorithm.minimax:
            value = self._minimax(tree.root, True)
        elif self.alg == SolvingAlgorithm.alpha_beta:
            value = self._alpha_beta(tree.root, -9999999999, 999999999, True)

    def _minimax(self, node: Node, maximizing_player: bool) -> int:
        if node.game_state.turn_number == self.max_depth:
            return node.calculate_heuristic(self.heuristic)

        moves = node.game_state.get_valid_moves()
        if node.game_state.move_watcher.is_board_symmetrical(node.game_state.board):
            # print('\nDetected symmetrical board')
            moves = node.game_state.move_watcher.remove_symmetrical_moves(moves)
            # node.game_state.print_board()

        if len(moves) == 0:
            return node.calculate_heuristic(self.heuristic)

        best_value = 0
        best_node = None
        if maximizing_player:
            best_value = -999999999

            for move in moves:
                new_node = Node(GameState(node.game_state))
                new_node.game_state.make_move(*move)
                child_value = self._minimax(new_node, False)
                if child_value > best_value:
                    best_node = new_node
                    best_value = child_value
        else:
            best_value = 9999999999

            for move in moves:
                new_node = Node(GameState(node.game_state))
                new_node.game_state.make_move(*move)
                child_value = self._minimax(new_node, True)
                if child_value < best_value:
                    best_node = new_node
                    best_value = child_value

        node.best_child = best_node
        node.best_child_heuristic_value = best_value

        return best_value

    def _alpha_beta(self, node: Node, alpha: [int, float], beta: [int, float], maximising_player: bool) -> int:
        if node.game_state.turn_number == self.max_depth:
            return node.calculate_heuristic(self.heuristic)

        moves = node.game_state.get_valid_moves()
        if node.game_state.move_watcher.is_board_symmetrical(node.game_state.board):
            moves = node.game_state.move_watcher.remove_symmetrical_moves(moves)
            node.game_state.print_board()

        if len(moves) == 0:
            return node.calculate_heuristic(self.heuristic)

        best_value = 0
        best_node = None
        if maximising_player:
            best_value = alpha

            for move in moves:
                new_node = Node(GameState(node.game_state))
                new_node.game_state.make_move(*move)
                child_value = self._alpha_beta(new_node, best_value, beta, False)
                if child_value > best_value:
                    best_node = new_node
                    best_value = child_value
                if beta <= best_value:
                    break
        else:
            best_value = beta

            for move in moves:
                new_node = Node(GameState(node.game_state))
                new_node.game_state.make_move(*move)
                child_value = self._alpha_beta(new_node, alpha, best_value, True)
                if child_value < best_value:
                    best_node = new_node
                    best_value = child_value
                if best_value <= alpha:
                    break

        node.best_child = best_node
        node.best_child_heuristic_value = best_value

        return best_value


def heuristic_game_score(game_state: GameState) -> int:
    white = 0
    black = 0
    for row in game_state.board:
        for e in row:
            if e == 1:
                white += 1
            elif e == 2:
                black += 1
    return white - black
