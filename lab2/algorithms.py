from tree import Tree, Node
from reversi import GameState, Piece
from typing import Callable, Optional
from enum import Enum


class SolvingAlgorithm(Enum):
    minimax = 0
    alpha_beta = 1


class Algorithm:
    def __init__(self, heuristic: Callable[[GameState], int], solving_alg: SolvingAlgorithm):
        self.heuristic = heuristic
        self.alg = solving_alg
        self.max_depth = 3
        self.visited_nodes = 0

    def traverse_tree(self, tree: Tree, depth: int) -> None:
        tree.clear()
        tree.depth = depth
        self.max_depth = depth
        self.visited_nodes = 0
        if self.alg == SolvingAlgorithm.minimax:
            value = self._minimax(tree.root, True)
        elif self.alg == SolvingAlgorithm.alpha_beta:
            value = self._alpha_beta(tree.root, -9999999999, 999999999, True)
        tree.generate_results()

    def _minimax(self, node: Node, maximizing_player: bool) -> int:
        self.visited_nodes += 1
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

    def _alpha_beta(self, node: Node, alpha: [int], beta: [int], maximising_player: bool) -> int:
        self.visited_nodes += 1
        if node.game_state.turn_number == self.max_depth:
            return node.calculate_heuristic(self.heuristic)

        moves = node.game_state.get_valid_moves()
        if node.game_state.move_watcher.is_board_symmetrical(node.game_state.board):
            moves = node.game_state.move_watcher.remove_symmetrical_moves(moves)
            # node.game_state.print_board()

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
    # result = 0
    # for row in game_state.board:
    #     for e in row:
    #         if e == 1:
    #             result += 1
    #         elif e == 2:
    #             result -= 1
    # return result

    return sum([sum(row) for row in game_state.board])
    # p1 = np.count_nonzero(game_state.board == 1)
    # p2 = np.count_nonzero(game_state.board == 2)
    # return p1 - p2


def heuristic_favour_corners(game_state: GameState) -> int:
    board_size = len(game_state.board)
    corners = [(0, 0), (0, board_size - 1), (board_size - 1, 0), (board_size - 1, board_size - 1)]
    sum_distances_to_4_corners = 0
    for corner in corners:
        if game_state.board[corner[0]][corner[1]] == Piece.BLACK.value:
            continue
        closest_player_piece = _find_closest_point(corner, game_state.board, game_state.FIRST_PLAYER)
        if closest_player_piece is not None:
            dist = _manhattan_distance(corner, closest_player_piece)
            reversed_dist = (board_size - 1) * 2 - dist
            sum_distances_to_4_corners += reversed_dist
    return sum_distances_to_4_corners


def heuristic_favour_number_of_moves(game_state: GameState) -> int:
    p1_moves = len(game_state.get_valid_moves(game_state.FIRST_PLAYER))
    p2_moves = len(game_state.get_valid_moves(game_state.SECOND_PLAYER))

    return p1_moves - p2_moves


def _find_closest_point(relative_point: tuple[int, int], board: list[tuple[int, int]], player_piece: int) \
        -> Optional[tuple[int, int]]:
    radius = 0
    while radius < len(board):
        upper_left_square_corner = (max(relative_point[0] - radius, 0), max(relative_point[1] - radius, 0))
        upper_right_square_corner = (max(relative_point[0] - radius, 0), min(relative_point[1] + radius, len(board) - 1))
        lower_left_square_corner = (min(relative_point[0] + radius, len(board) - 1), max(relative_point[1] - radius, 0))
        lower_right_square_corner = (
            min(relative_point[0] + radius, len(board) - 1), min(relative_point[1] + radius, len(board) - 1))
        for col in range(upper_left_square_corner[1], upper_right_square_corner[1]):
            if board[upper_left_square_corner[0]][col] == player_piece:
                return upper_left_square_corner[0], col
            if board[lower_left_square_corner[0]][col] == player_piece:
                return lower_left_square_corner[0], col

        for row in range(upper_left_square_corner[0], lower_left_square_corner[0]):
            if board[row][upper_left_square_corner[1]] == player_piece:
                return row, upper_left_square_corner[1]
            if board[row][upper_right_square_corner[1]] == player_piece:
                return row, upper_right_square_corner[1]
        radius += 1
    return None


def _manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
