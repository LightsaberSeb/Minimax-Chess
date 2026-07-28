# File just to calculate every movement for each of the pieces

# Helpers
def check_move_type(piece: str, srow: int, scol: int, row: int, col: int, state):
    type = "normal"
    
    # Castling
    if piece[1] == "k":
        if abs(col - scol) == 2:
            type = "castle"

    # En passant
    if ((row, col) == state.en_passant 
        and piece[1] == "p"
        and scol != col
        ):
        type = "en passant"
    
    # Promotion
    if piece[1] == "p":
        match piece[0]:
            case "w":
                if row == 0:
                    type = "promotion"
            case "b":
                if row == 7:
                    type = "promotion"
    
    return type

def get_pseudo_moves(color: str, state):
    pseudo_moves = []
    
    for row in range(8):
        for col in range(8):
            piece = state.board[row][col]
            if piece == "":
                continue
            
            if piece[0] == color:
                moves = state.move_functions[piece[1]](row, col, state)
                for move in moves:
                    pseudo_moves.append([(row, col), move])
    
    return pseudo_moves

def get_legal_moves(color: str, state):
    pseudo_moves = get_pseudo_moves(color, state)
    legal_moves = []
    
    for move in pseudo_moves:
        make_move(move[0][0], move[0][1], move[1][0], move[1][1], state)
        
        if not is_on_check(color, state):
            legal_moves.append(move)
        
        undo_move(state)
    return legal_moves

def is_on_check(color: str, state):
    king = color+"k"
    opposite = state.opposite(color)
    row, col = state.king_pos[king]
    
    return is_tile_attacked(row, col, state, opposite)

def make_move(srow: int, scol: int, trow: int, tcol: int, state):
    changes = []
    captured = ""
    piece = state.board[srow][scol]
    type = check_move_type(piece, srow, scol, trow, tcol, state)
    
    match type:
        case "normal":
            if state.board[trow][tcol] != "":
                captured = state.board[trow][tcol]
            
            state.board[trow][tcol] = state.board[srow][scol]
            state.board[srow][scol] = ""
            
            changes.append({
                "from": (srow, scol),
                "target": (trow, tcol),
                "piece": piece,
                "captured": captured,
                "captured_pos": (trow, tcol),
                "type": type
            })
        case "en passant":
            state.board[trow][tcol] = state.board[srow][scol]
            state.board[srow][scol] = ""
            
            color = piece[0]
            if color == "b":
                captured = state.board[trow - 1][tcol]
                captured_pos = (trow - 1, tcol)
                state.board[trow - 1][tcol] = ""
            else:
                captured = state.board[trow + 1][tcol]
                captured_pos = (trow + 1, tcol)
                state.board[trow + 1][tcol] = ""
            
            changes.append({
                "from": (srow, scol),
                "target": (trow, tcol),
                "piece": piece,
                "captured": captured,
                "captured_pos": captured_pos,
                "type": type
            })
        case "castle":
            delta = tcol - scol
            state.board[trow][tcol] = state.board[srow][scol]
            state.board[srow][scol] = ""
            
            changes.append({
                "from": (srow, scol),
                "target": (trow, tcol),
                "piece": piece,
                "captured": "",
                "captured_pos": (trow, tcol),
                "type": type
            })
            
            if delta == 2:
                state.board[trow][5] = state.board[trow][7]
                state.board[trow][7] = ""
                
                changes.append({
                "from": (trow, 7),
                "target": (trow, 5),
                "piece": state.board[trow][5],
                "captured": "",
                "captured_pos": (trow, 5),
                "type": type
                })
            elif delta == -2:
                state.board[trow][3] = state.board[trow][0]
                state.board[trow][0] = ""
                
                changes.append({
                "from": (trow, 0),
                "target": (trow, 3),
                "piece": state.board[trow][3],
                "captured": "",
                "captured_pos": (trow, 3),
                "type": type
                })
        case "promotion":
            if state.board[trow][tcol] != "":
                captured = state.board[trow][tcol]
            
            state.board[trow][tcol] = state.board[srow][scol]
            state.board[srow][scol] = ""
            
            changes.append({
                "from": (srow, scol),
                "target": (trow, tcol),
                "piece": piece,
                "captured": captured,
                "captured_pos": (trow, tcol),
                "type": type
            })
            

    if piece[1] == "k":
        state.king_pos[piece] = (trow, tcol)

    state.moves.append(changes)

def undo_move(state):
    move = state.moves.pop()

    for pos in move:
        srow, scol = pos["from"]
        trow, tcol = pos["target"]
        crow, ccol = pos["captured_pos"]
        piece = pos["piece"]
        captured = pos["captured"]
        
        state.board[trow][tcol] = ""
        state.board[srow][scol] = piece
        state.board[crow][ccol] = captured
        
        if piece[1] == "k":
            state.king_pos[piece] = (srow, scol)

def is_path_clear(srow, scol, trow, tcol,  board):
    step_row = (trow > srow) - (trow < srow)
    step_col = (tcol > scol) - (tcol < scol)
    
    srow += step_row
    scol += step_col
    
    while (srow, scol) != (trow, tcol):
        if board[srow][scol] != "":
            return False
        
        srow += step_row
        scol += step_col
        
    return True

def is_tile_attacked(row: int, col: int, state, attacker: str):
    for prow in range(8):
        for pcol in range(8):
            piece = state.board[prow][pcol]
            
            if piece == "":
                continue
            
            if piece[0] != attacker:
                continue
            
            drow = row - prow
            dcol = col - pcol
            
            match piece[1]:
                case "p":
                    dir = -1 if piece[0] == "w" else 1
                    if drow == dir and abs(dcol) == 1:
                        return True
                case "n":
                    if (abs(drow) == 2 and abs(dcol) == 1) or (abs(drow) == 1 and abs(dcol) == 2):
                        return True
                case "b":
                    if abs(drow) == abs(dcol):
                        if is_path_clear(prow, pcol, row, col, state.board):
                            return True
                case "r":
                    if drow == 0 or dcol == 0:
                        if is_path_clear(prow, pcol, row, col, state.board):
                            return True
                case "q":
                    if (abs(drow) == abs(dcol)) or (drow == 0 or dcol == 0):
                        if is_path_clear(prow, pcol, row, col, state.board):
                            return True
                case "k":
                    if max(abs(drow), abs(dcol)) == 1:
                        return True
    return False


#Moves
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
            and not is_tile_attacked(7, 5, state, "b")
            and not is_tile_attacked(7, 6, state, "b")
        ):
            moves.append((7, 6))
        # Long Castling
        if (
            state.board[7][0] == "wr"
            and state.board[7][3] == ""
            and state.board[7][2] == ""
            and state.board[7][1] == ""
            and not is_tile_attacked(7, 3, state, "b")
            and not is_tile_attacked(7, 2, state, "b")
            and not is_tile_attacked(7, 1, state, "b")
        ):
            moves.append((7, 2))
    else:
        # Short Castling
        if (
            state.board[0][7] == "br"
            and state.board[0][5] == ""
            and state.board[0][6] == ""
            and not is_tile_attacked(0, 5, state, "w")
            and not is_tile_attacked(0, 6, state, "w")
        ):
            moves.append((0, 6))
        # Long Castling
        if (
            state.board[0][0] == "br"
            and state.board[0][3] == ""
            and state.board[0][2] == ""
            and state.board[0][1] == ""
            and not is_tile_attacked(0, 3, state, "w")
            and not is_tile_attacked(0, 2, state, "w")
            and not is_tile_attacked(0, 1, state, "w")
        ):
            moves.append((0, 2))
    
    return moves

def king_moves(row: int, col: int, state):
    moves = []

    piece = state.board[row][col]
    color = piece[0]
    
    opposite = state.opposite(color)
    
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
            
            make_move(row, col, r, c, state)
            attacked = is_tile_attacked(r, c, state, opposite)
            undo_move(state)
            
            if attacked:
                continue
            
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
