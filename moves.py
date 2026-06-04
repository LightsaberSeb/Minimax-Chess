# File just to calculate every movement for each of the pieces

def rook_moves(row: int, col: int, board: list):
    moves = []
    
    piece = board[row][col]
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
            target = board[r][c]
            
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

def bishop_moves(row: int, col: int, board: list):
    moves = []
    
    piece = board[row][col]
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
            target = board[r][c]
            
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

def queen_moves(row: int, col: int, board: list):
    moves = []
    
    piece = board[row][col]
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
            target = board[r][c]
            
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

def king_moves(row: int, col: int, board: list):
    moves = []
    
    piece = board[row][col]
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
            target = board[r][c]
            
            if target == "":
                moves.append((r, c))
            else:
                if target[0] != color:
                    moves.append((r, c))
    
    
    return moves

def knight_moves(row: int, col: int, board: list):
    moves = []
    return moves

def pawn_moves(row: int, col: int, board: list):
    moves = []
    return moves