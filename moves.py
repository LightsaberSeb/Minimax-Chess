# File just to calculate every movement for each of the pieces
# Row = x axis
# Column = y axis

# Rook
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

# Bishop
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

# Queen
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

# King
def castling(row: int, col: int, state):
    moves = []
    piece = state.board[row][col]
    color = piece[0]
    
    if not state.can_castle[piece]:
        return []
    
    if color == "w":
        # Short Castling
        if (
            state.board[7][7] == "wr"
            and state.board[7][5] == ""
            and state.board[7][6] == ""
            # Add if the king is in check or the castling square is being attacked
        ):
            moves.append((7, 6))
        # Long Castling
        if (
            state.board[7][0] == "wr"
            and state.board[7][3] == ""
            and state.board[7][2] == ""
            and state.board[7][1] == ""
        ):
            moves.append((7, 2))
    else:
        # Short Castling
        if (
            state.board[0][7] == "br"
            and state.board[0][5] == ""
            and state.board[0][6] == ""
        ):
            moves.append((0, 6))
        # Long Castling
        if (
            state.board[0][0] == "br"
            and state.board[0][3] == ""
            and state.board[0][2] == ""
            and state.board[0][1] == ""
        ):
            moves.append((0, 2))
    
    return moves

def king_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]
    
    directions = [
        (1, 0), 
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1)
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

    moves.extend(castling(row, col, state))

    return moves

# Knight
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

# Pawn
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

    if 0 <= row < 7:
        target = state.board[r][c]
        
        # Movement Logic
        if target == "":
            if (row == start_row) and (state.board[r + i][c] == ""):
                moves.append((r + i, c))

            moves.append((r, c))
        
        # Capture Logic
        if c <= 0:
            target_r = state.board[r][c + 1]
            target_l = ""
        elif 0 <= c < 7:
            target_r = state.board[r][c + 1]
            target_l = state.board[r][c - 1]
        else:
            target_r = ""
            target_l = state.board[r][c - 1]

        if target_r != "":
            if color != target_r[0]:    
                moves.append((r, c + 1))
        if target_l != "":
            if color != target_l[0]:
                moves.append((r, c - 1))

        # En Passant
        right = (r, c + 1)
        left = (r, c - 1)
        if right == state.en_passant or left == state.en_passant:
            moves.append(state.en_passant)

    return moves
