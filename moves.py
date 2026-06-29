# File just to calculate every movement for each of the pieces
# Row = x axis
# Column = y axis


def rook_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for drow, dcol in directions:
        r = row + drow
        c = col + dcol

        while 0 <= r < 8 and 0 <= c < 8:
            target = state.board[r][c]

            # Empty tile
            if target == "":
                moves.append((r, c))
            else:
                # Enemy piece
                if target[0] != color:
                    moves.append((r, c))
                break

            r += drow
            c += dcol

    return moves


def bishop_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]

    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for drow, dcol in directions:
        r = row + drow
        c = col + dcol

        while 0 <= r < 8 and 0 <= c < 8:
            target = state.board[r][c]

            # Empty Tile
            if target == "":
                moves.append((r, c))
            else:
                # Enemy Piece
                if target[0] != color:
                    moves.append((r, c))
                break

            r += drow
            c += dcol

    return moves


def queen_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    for drow, dcol in directions:
        r = row + drow
        c = col + dcol

        while 0 <= r < 8 and 0 <= c < 8:
            target = state.board[r][c]

            # Empty Tile
            if target == "":
                moves.append((r, c))
            else:
                # Enemy Piece
                if target[0] != color:
                    moves.append((r, c))
                break

            r += drow
            c += dcol

    return moves


# STILL NEED TO ADD CASTLING
def king_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    for drow, dcol in directions:
        r = row + drow
        c = col + dcol

        if 0 <= r < 8 and 0 <= c < 8:
            target = state.board[r][c]

            if target == "":
                moves.append((r, c))
            else:
                if target[0] != color:
                    moves.append((r, c))

    return moves


def knight_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]

    directions = [
        (1, 2),
        (-1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, 1),
        (-2, -1),
    ]

    for drow, dcol in directions:
        r = row + drow
        c = col + dcol

        if 0 <= r < 8 and 0 <= c < 8:
            target = state.board[r][c]

            if target == "":
                moves.append((r, c))
            else:
                if target[0] != color:
                    moves.append((r, c))

    return moves


def pawn_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]

    directions = {"w": [(-1, 0), -1], "b": [(1, 0), 1]}

    start_row = 0
    if color == "w":
        start_row = 6
    else:
        start_row = 1

    # Movement logic
    drow, dcol = directions[color][0]
    i = directions[color][1]

    r = row + drow
    c = col + dcol

    if 0 <= r < 8 and 0 <= c < 8:
        target = state.board[r][c]
        target_r = state.board[r][c + 1]
        target_l = state.board[r][c - 1]

        # Movement Logic
        if target == "":
            if (row == start_row) and (state.board[r + i][c] == ""):
                moves.append((r + i, c))

            moves.append((r, c))

        # Capture Logic
        if target_r != "":
            moves.append((r, c + 1))
        if target_l != "":
            moves.append((r, c - 1))

        # En Passant
        # check first if the pawn can be en passanted
        # check for both left and right to see if the en passant tile is nearby
        # if it is, add it as a capture move

    return moves
