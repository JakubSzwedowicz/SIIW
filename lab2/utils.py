from reversi import Piece


def read_board() -> list[list[int]]:
    board = [[0] * 8 for _ in range(8)]
    # board[3][3] = 1
    # board[3][4] = -1
    # board[4][3] = -1
    # board[4][4] = 1
    for row in range(len(board)):
        text = input(f'Enter row {row}:')
        for col, value in enumerate(text.split()):
            if value == '1':
                board[row][col] = Piece.WHITE.value
            elif value == '2':
                board[row][col] = Piece.BLACK.value
            elif value == '0':
                board[row][col] = Piece.NONE.value
            else:
                raise Exception(f'Illegal sign in text input: {value}')
    return board
