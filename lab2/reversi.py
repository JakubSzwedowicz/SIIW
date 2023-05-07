from typing import Tuple, List, Optional

import numpy as np


def get_symmetrical_field(field: Tuple[int, int], axis: int) -> Tuple[int, int]:
    '''
    axis = 2: /
             /

    axis = 1: \
               \
    '''
    if axis == 2:
        return 7 - field[0], 7 - field[1]
    else:
        return field[1], field[0]


class GameState:
    def __init__(self, game_state: 'GameState' = None):
        if game_state is None:
            # self.board = np.zeros((8, 8), dtype=int)
            self.board = [[0] * 8 for _ in range(8)]
            self.current_player = 1
            self.board[3][3] = self.board[4][4] = 1
            self.board[3][4] = self.board[4][3] = 2
            self.turn_number = 1
            self.move_watcher: MoveWatcher = MoveWatcher(self.current_player)
        else:
            # self.board = game_state.board.copy()
            self.board = [row[:] for row in game_state.board]
            self.current_player = game_state.current_player
            self.turn_number = game_state.turn_number
            self.move_watcher: MoveWatcher = MoveWatcher(game_state.move_watcher.symm_axis, game_state.move_watcher)
        self.made_move: Optional[Tuple[int, int]] = None

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    moves.append((row, col))
        return moves

    def is_valid_move(self, row, col) -> bool:
        if self.board[row][col] != 0:
            return False
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_row == 0 and d_col == 0:
                    continue
                if self.is_valid_direction(row, col, d_row, d_col):
                    return True
        return False

    def is_valid_direction(self, row, col, d_row, d_col) -> bool:
        opponent = 3 - self.current_player
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
                if self.is_valid_direction(row, col, d_row, d_col):
                    self.flip_direction(row, col, d_row, d_col)
        self.current_player = 3 - self.current_player

    def flip_direction(self, row, col, d_row, d_col) -> None:
        r, c = row + d_row, col + d_col
        while self.board[r][c] != self.current_player:
            self.board[r][c] = self.current_player
            r, c = r + d_row, c + d_col

    def get_winner(self) -> int:
        counts = [0, 0, 0]
        for row in range(8):
            for col in range(8):
                counts[self.board[row][col]] += 1
        if counts[1] > counts[2]:
            return 1
        elif counts[2] > counts[1]:
            return 2
        else:
            return 0

    def print_board(self) -> None:
        print("   0 1 2 3 4 5 6 7 ")
        print("  +-+-+-+-+-+-+-+-+")
        # print("  -----------------")
        for row in range(8):
            print(row, end=" |")
            for col in range(8):
                if self.board[row][col] == 0:
                    print("0", end="|")
                elif self.board[row][col] == 1:
                    print("1", end="|")
                else:
                    print("2", end="|")
            print("\n  +-+-+-+-+-+-+-+-+")
            # print("\n  -----------------")


class MoveWatcher:
    FIRST_MOVE = True

    def __init__(self, first_player: int, move_watcher: 'MoveWatcher' = None):
        '''
        starting board:
                        12
                        21
        axis = 2:
                     /
                    /

        axis = 1:
                    \
                     \
        '''
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

        if self.symm_axis == 1:
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
            if self.symm_axis == 1:
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
                game.current_player = 3 - game.current_player
                continue
        print(f"Player {game.current_player}'s turn")
        game.print_board()
        print(f"Valid moves: {valid_moves}")
        row, col = map(int, input("Enter row and column: ").split())
        if (row, col) in valid_moves:
            game.make_move(row, col)
        else:
            print("Invalid move")
            game.current_player = 3 - game.current_player

    game.print_board()
    winner = game.get_winner()
    if winner == 0:
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")


if __name__ == "__main__":
    main()
