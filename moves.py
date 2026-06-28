# File just to calculate every movement for each of the pieces

def rook_moves(row: int, col: int, state):
    moves = []
    
    piece = state.board[row][col]
    color = piece[0]
    
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]
    
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
    
    directions = [
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1)
    ]
    
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
        (-2, -1)
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
    
    directions = {
        "w": (0, -1),
        "b": (0, 1)
    }
    
    start_row = 0
    if color == "w":
        start_row = 6
    else:
        start_row = 1
    
    #Movement logic
    drow, dcol = directions[color]
    
    r = row + drow
    c = col + dcol
    
    if 0 <= r < 8 and 0 <= c < 8:
        target = state.board[r][c]
        
        if target == "":
            if row == start_row:
                pass #Move 2 spaces instead of one
            else:
                pass #Just move one space
            
        # left diagonal and right diagonal capures
        # if color not same as piece and is diagonal to piece: then capture logic
    
    
    
    return moves