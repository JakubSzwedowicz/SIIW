from typing import Tuple, List, Optional
from enum import Enum

import numpy as np


def get_symmetrical_field(field: Tuple[int, int], axis: int) -> Tuple[int, int]:
    '''
    axis = Piece.BLACK.value: /
             /

    axis = Piece.WHITE.value: \
               \
    '''

    if axis == Piece.WHITE.value:
        return field[1], field[0]
    elif axis == Piece.BLACK.value:
        return 7 - field[0], 7 - field[1]
    else:
        raise Exception(f'Illegal axis {axis}!')


class Piece(Enum):
    WHITE = 1
    NONE = 0
    BLACK = -1


class GameState:
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    FIRST_PLAYER = Piece.WHITE.value
    SECOND_PLAYER = Piece.BLACK.value

    def __init__(self, game_state: 'GameState' = None):
        if game_state is None:
            # self.board = np.zeros((8, 8), dtype=int)
            self.board = [[0] * 8 for _ in range(8)]
            self.current_player = GameState.FIRST_PLAYER
            self.board[3][3] = self.board[4][4] = Piece.WHITE.value
            self.board[3][4] = self.board[4][3] = Piece.BLACK.value
            self.turn_number = GameState.FIRST_PLAYER
            self.move_watcher: MoveWatcher = MoveWatcher(self.current_player)
        else:
            # self.board = game_state.board.copy()
            self.board = [row[:] for row in game_state.board]
            self.current_player = game_state.current_player
            self.turn_number = game_state.turn_number
            self.move_watcher: MoveWatcher = MoveWatcher(game_state.move_watcher.symm_axis, game_state.move_watcher)
        self.made_move: Optional[Tuple[int, int]] = None

    def __repr__(self) -> str:
        return f'Turn number: {self.turn_number}, current_player: {self.current_player}, winner: {self._get_winner() if self.is_game_finished() else "None"}, moves_watcher bricked: {self.move_watcher.bricked}, moves_watcher unsymm_moves: {self.move_watcher.unsymmetrical_moves}'

    def get_valid_moves(self, player_piece: int = None) -> List[Tuple[int, int]]:
        temp = self.current_player
        if player_piece is not None:
            self.current_player = player_piece

        moves = []
        for row in range(8):
            for col in range(8):
                if self._is_valid_move(row, col):
                    moves.append((row, col))

        if player_piece is not None:
            self.current_player = temp

        return moves

    def _is_valid_move(self, row, col) -> bool:
        if self.board[row][col] != 0:
            return False
        # for d_row in range(-1, 2):
        #     for d_col in range(-1, 2):
        #         if d_row == 0 and d_col == 0:
        #             continue
        #         if self.is_valid_direction(row, col, d_row, d_col):
        #             return True
        for d_row, d_col in GameState.DIRECTIONS:
            if self._is_valid_direction(row, col, d_row, d_col):
                return True
        return False

    def _is_valid_direction(self, row, col, d_row, d_col) -> bool:
        opponent = -self.current_player
        r, c = row + d_row, col + d_col
        if r < 0 or r >= 8 or c < 0 or c >= 8 or self.board[r][c] != opponent:
            return False
        while 0 <= r < 8 and 0 <= c < 8:
            if self.board[r][c] == 0:
                return False
            if self.board[r][c] == self.current_player:
                return True
            r, c = r + d_row, c + d_col
        return False


    def make_move(self, row, col) -> None:
        self.turn_number += 1
        self.move_watcher.add_move((row, col))
        self.made_move = (row, col)
        self.board[row][col] = self.current_player
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_row == 0 and d_col == 0:
                    continue
                if self._is_valid_direction(row, col, d_row, d_col):
                    self._flip_direction(row, col, d_row, d_col)
        self.current_player = -self.current_player

    def _flip_direction(self, row, col, d_row, d_col) -> None:
        r, c = row + d_row, col + d_col
        while self.board[r][c] != self.current_player:
            self.board[r][c] = self.current_player
            r, c = r + d_row, c + d_col

    def _get_winner(self) -> int:
        result = np.sum(self.board)
        return result / np.positive(result) if result != 0 else 0

    def print_board(self) -> None:
        print("   0 1 2 3 4 5 6 7 ")
        print("  +-+-+-+-+-+-+-+-+")
        # print("  -----------------")
        for row in range(8):
            print(row, end=" |")
            for col in range(8):
                if self.board[row][col] == Piece.NONE.value:
                    print("0", end="|")
                elif self.board[row][col] == Piece.WHITE.value:
                    print("1", end="|")
                else:
                    print("2", end="|")
            print("\n  +-+-+-+-+-+-+-+-+")
            # print("\n  -----------------")

    def is_game_finished(self) -> bool:
        p1_moves = self.get_valid_moves()
        p2_moves = self.get_valid_moves(-self.current_player)
        return (p1_moves == 0) and (p2_moves == 0)


class MoveWatcher:
    FIRST_MOVE = True

    def __init__(self, first_player: int, move_watcher: 'MoveWatcher' = None):
        '''
        starting board:
                        1(-1)
                        (-1)1
        axis = -1:
                     /
                    /

        axis = 1:
                    \
                     \
        '''
        if first_player != -1 and first_player != 1:
            raise Exception(f'Illegal first player: {first_player}')

        self.symm_axis = first_player
        self.bricked: bool = False if move_watcher is None else move_watcher.bricked
        self.unsymmetrical_moves: List[
            Tuple[int, int]] = [] if move_watcher is None else move_watcher.unsymmetrical_moves[:]

    def add_move(self, move: Tuple[int, int]) -> None:
        if self.bricked:
            return
        symm_move = get_symmetrical_field(move, self.symm_axis)
        if symm_move in self.unsymmetrical_moves:
            self.unsymmetrical_moves.remove(symm_move)
        else:
            self.unsymmetrical_moves.append(move)
            if len(self.unsymmetrical_moves) == 6:
                self.bricked = True
                self.unsymmetrical_moves = []

    def is_board_symmetrical(self, board: List[List[int]]) -> bool:
        if len(self.unsymmetrical_moves) != 0 or self.bricked:
            return False

        if self.symm_axis == Piece.WHITE.value:
            for row in range(1, 8):
                for col in range(row):
                    symm_field = get_symmetrical_field((row, col), self.symm_axis)
                    if board[row][col] != board[symm_field[0]][symm_field[1]]:
                        return False
        else:
            for row in range(7):
                for col in range(7 - row):
                    symm_field = get_symmetrical_field((row, col), self.symm_axis)
                    if board[row][col] != board[symm_field[0]][symm_field[1]]:
                        return False
        return True

    def remove_symmetrical_moves(self, moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        res = []
        for move in moves:
            if self.symm_axis == Piece.WHITE:
                if move[1] <= move[0]:
                    res.append(move)
            else:
                if move[1] <= 7 - move[0]:
                    res.append(move)
        if MoveWatcher.FIRST_MOVE:
            MoveWatcher.FIRST_MOVE = False
            return res[:1]
        else:
            return res


def main():
    game = GameState()
    counter = 0
    while True:
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            counter += 1
            if counter == 2:
                break
            else:
                print("No valid moves")
                game.current_player = -game.current_player
                continue
        print(f"Player {game.current_player}'s turn")
        game.print_board()
        print(f"Valid moves: {valid_moves}")
        row, col = map(int, input("Enter row and column: ").split())
        if (row, col) in valid_moves:
            game.make_move(row, col)
        else:
            print("Invalid move")
            game.current_player = -game.current_player

    game.print_board()
    winner = game.get_winner()
    if winner == 0:
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")


if __name__ == "__main__":
    main()
