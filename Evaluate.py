import moves

# Values and weighs
MIDGAME_SCORE = 20
ENDGAME_SCORE = 6

PIECE_VALUES = {
    "p": 100,
    "n": 320,
    "b": 330,
    "r": 500,
    "q": 900,
    "k": 0
}
EVAL_WEIGHTS = {
    "material": 1.2,
    "positioning": 1.4,
    "mobility": 1.7,
    "king_safety": 1.2,
    "stacked_pawns": 1.5,
    "rook_value": 1.3,
    "past_pawns": 1.6,
    "king_near_pawns": 1.5,
    "pawn_race": 1.2
}

# Position tables
KNIGHT_TABLE = [
    [-50, -20, -30, -30, -30, -30, -20, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 20, 25, 25, 20, 5, -30],
    [-30, 5, 20, 25, 25, 20, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -20, -30, -30, -30, -30, -20, -50],
]
BISHOP_TABLE = [
    [20, 15, 0, -10, -10, 0, 15, 20],
    [20, 20, 5, -15, -15, 5, 20 ,20],
    [15, 15, 10, -25, -25, 10, 20, 15],
    [0, 0, 10, 10, 10, 10, 0, 0],
    [0, 0, 10, 10, 10, 10, 0, 0],
    [15, 15, 10, -15, -15, 10, 20, 15],
    [20, 20, 5, -10, -10, 5, 20, 20],
    [20, 15, 0, -10, -10, 0, 15, 20],
]
ROOK_TABLE = [
    [15, 15, 15, 15, 15, 15, 15, 15],
    [25, 25 ,25 ,25 ,25 ,25 ,25 ,25],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [10, 10, 10, 10, 10, 10, 10, 10],
]
KING_TABLE = [
    [-50, -50, -50, -50, -50, -50, -50, -50],
    [-50, -50, -50, -50, -50, -50, -50, -50],
    [-50, -50, -50, -50, -50, -50, -50, -50],
    [-50, -50, -50, -50, -50, -50, -50, -50],
    [-30, -30, -30, -30, -30, -30, -30, -30],
    [-10, -10, -10, -10, -10, -10, -10, -10],
    [10, 15, 5, -10, -10, 5, 15, 10],
    [20, 40, 20, 0, 0, 20, 40, 20],
]
ENDGAME_KING_TABLE = [
    [-40, -35, -35, -35, -35, -35, -35, -40],
    [-30, 5, 5, 5, 5, 5, 5, -30],
    [-15, 0, 10, 10, 10, 10, 0, -15],
    [10, 20, 20, 25, 25, 20, 20, 10],
    [0, 10, 10, 25, 25, 10, 10, 0],
    [-15, 0, 10, 10, 10, 10, 0, -15],
    [-30, 5, 5, 5, 5, 5, 5, -30],
    [-40, -35, -35, -35, -35, -35, -35, -40],
]
QUEEN_TABLE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [ -5, 0, 5, 10, 10, 5, 0, -5],
    [ -5, 0, 5, 10,  10, 5, 0, -5],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20],
]
PAWN_TABLE = [
    [-5, -5, -5, -5, -5, -5, -5, -5],
    [-5, -5, -5, -5, -5, -5, -5, -5],
    [0, 0, 10, 15, 15, 10, 0, 0],
    [5, 5, 15, 30, 30, 15, 5, 5],
    [2, 5, 15, 30, 30, 15, 5, 2],
    [-10, 0, 15, 20, 20, 15, 0, -10],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-5, -5, -5, -5, -5, -5, -5, -5],
]
ENDGAME_PAWN_TABLE = [
    [50, 50, 50, 50, 50, 50, 50, 50],
    [40, 40, 40, 40, 40, 40, 40, 40],
    [30, 30, 30, 30, 30, 30, 30, 30],
    [20, 20, 20, 20, 20, 20, 20, 20],
    [10, 10, 10, 10, 10, 10, 10, 10],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [-5, -5, -5, -5, -5, -5, -5, -5],
    [-15, -15, -15, -15, -15, -15, -15, -15],
]

PIECE_SQUARE_TABLES = {
    "p": PAWN_TABLE,
    "n": KNIGHT_TABLE,
    "b": BISHOP_TABLE,
    "r": ROOK_TABLE,
    "q": QUEEN_TABLE,
    "k": KING_TABLE,
}
ENDGAME_PIECE_SQUARE_TABLES = {
    "k": ENDGAME_KING_TABLE,
    "p": ENDGAME_PAWN_TABLE
}

# Evaluation functions
def evaluate(state):
    score = 0
    
    board = state.board
    pawn_data = pawn_files(board)
    phase = get_game_phase(board)
    
    #score += mobility(state) * EVAL_WEIGHTS["mobility"] 
    score += evaluate_material(board) * EVAL_WEIGHTS["material"]
    score += evaluate_piece_positions(board, phase) * EVAL_WEIGHTS["positioning"]
    score += king_safety(state, pawn_data) * EVAL_WEIGHTS["king_safety"]
    score += stacked_pawns(pawn_data) * EVAL_WEIGHTS["stacked_pawns"]
    score += rook_value(board, pawn_data) * EVAL_WEIGHTS["rook_value"]

    if phase > 0.3:
        score += evaluate_passed_pawns(state) * phase * EVAL_WEIGHTS["past_pawns"]
        score += evaluate_king_near_pawns(state) * phase * EVAL_WEIGHTS["king_near_pawns"]
        score += evaluate_pawn_race(state) * phase * EVAL_WEIGHTS["pawn_race"]

    return score

def king_safety(state, pawn_data):
    score = 0
    
    score += evaluate_pawn_shield(state)
    score += evaluate_open_columns(state, pawn_data)
    
    return score

# Helper Functions
def is_passed_pawn(board, row, col, color):
    enemy = "b" if color == "w" else "w"
    direction = 1 if color == "w" else -1

    for dcol in (-1, 0, 1):
        c = col + dcol
        
        if not 0 <= c < 8:
            continue
            
        r = row + direction
        
        while 0 <= r < 8:
            if board[r][c] == enemy + "p":
                return False
            
            r += direction

    return True

def pawn_files(board):
    pawns = {
        "w": [0, 0, 0, 0, 0, 0, 0, 0],
        "b": [0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    for col in range(8):
        for row in range(8):
            piece = board[row][col]
            
            if piece == "":
                continue
            
            if piece[1] != "p":
                continue
            
            pawns[piece[0]][col] += 1
    return pawns

def get_game_phase(board):
    score = 0
    
    for row in board:
        for piece in row:
            if piece == "":
                continue
            
            piece_type = piece[1]
            
            if piece_type == "q":
                score += 4
            elif piece_type == "r":
                score += 2
            elif piece_type in ("b", "n"):
                score += 1
    
    if score >= MIDGAME_SCORE:
        return 0.0
    if score <= ENDGAME_SCORE:
        return 1.0
    
    return (MIDGAME_SCORE - score) / (MIDGAME_SCORE - ENDGAME_SCORE)

def pawn_moves_to_promotion(row, color):
    if color == "w":
        moves = 7 - row
        
        if row == 6:
            moves -= 1
    else:
        moves = row
        
        if row == 1:
            moves -= 1
    return moves

def king_distance(king_pos, pawn_pos):
    return max(
        abs(king_pos[0] - pawn_pos[0]),
        abs(king_pos[1] - pawn_pos[1])
    )

def can_king_intercept(state, king_pos, pawn_pos, pawn_color):
    distance = king_distance(king_pos, pawn_pos)
    pawn_moves = pawn_moves_to_promotion(pawn_pos[0], pawn_color)
    
    if state.turn == pawn_color:
        pawn_moves -= 1
    
    return distance <= pawn_moves

# Evaluation Rules
def evaluate_piece_positions(board, phase):
    score = 0
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            
            if piece == "":
                continue
            
            color = piece[0]
            piece_type = piece[1]
            
            middle_table = PIECE_SQUARE_TABLES[piece_type]
            end_table = ENDGAME_PIECE_SQUARE_TABLES.get(piece_type)

            trow = row if color == "w" else 7 - row

            middle_value = middle_table[trow][col]

            if end_table is None:
                value = middle_value
            else:
                end_value = end_table[trow][col]

                value = (
                    middle_value * (1 - phase)
                    + end_value * phase
                )

            if color == "w":
                score += value
            else:
                score -= value

    return score

def evaluate_material(board):
    score = 0
    
    wb = 0
    bb = 0
    
    for row in board:
        for piece in row:
            if piece == "":
                continue
            
            color = piece[0]
            piece_type = piece[1]
            
            if piece_type == "b":
                if color == "w":
                    wb += 1
                else:
                    bb += 1

            value = PIECE_VALUES[piece_type]
            
            if color == "w":
                score += value
            elif color == "b":
                score -= value
    
    # bishop pair
    if wb >= 2:
        score += 30
    if bb >= 2:
        score -= 30
    
    return score

def mobility(state):
    score = 0
    
    white_moves = len(moves.get_legal_moves("w", state))
    black_moves = len(moves.get_legal_moves("b", state))
    
    difference = white_moves - black_moves
    
    score += difference * 5
    
    return score

def evaluate_pawn_shield(state):
    score = 0
    
    board = state.board
    white_front_pawns = [
            (-1, 0, 8),
            (-1, 1, 12),
            (-1, -1, 8)
    ]
    black_front_pawns = [
            (1, 0, 8),
            (1, 1, 12),
            (1, -1, 8)
    ]
    
    wk_pos = state.king_pos["wk"]
    bk_pos = state.king_pos["bk"]
    
    # white
    for drow, dcol, value in white_front_pawns:
        r = wk_pos[0] + drow
        c = wk_pos[1] + dcol
        
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "wp":
                score += value
    # black
    for drow, dcol, value in black_front_pawns:
        r = bk_pos[0] + drow
        c = bk_pos[1] + dcol
        
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "bp":
                score -= value
    
    return score

def evaluate_open_columns(state, pawns):
    score = 0
    
    wk_col = state.king_pos["wk"][1]
    bk_col = state.king_pos["bk"][1]
    
    wp = pawns["w"]
    bp = pawns["b"]
    
    for dcol in (-1, 0, 1):
        
        # White king
        col = wk_col + dcol
        
        if 0 <= col < 8:
            if wp[col] == 0:
                score -= 15
            
            elif bp[col] > 0:
                score -= 20
        
        # Black king
        col = bk_col + dcol
        
        if 0 <= col < 8:
            if bp[col] == 0:
                score += 15
                
            elif wp[col] > 0:
                score += 20
    return score

def stacked_pawns(pawns):
    score = 0
    
    for count in pawns["w"]:
        if count > 1:
            score -= (count - 1) * 15
    
    for count in pawns["b"]:
        if count > 1:
            score += (count - 1) * 15
    
    return score

def rook_value(board, pawns):
    score = 0
    
    for col in range(8):
        for row in range(8):
            piece = board[row][col]
            
            if piece == "":
                continue
            if piece[1] != "r":
                continue
            
            color = piece[0]
            if color == "w":
                if pawns["w"][col] == 0:
                    score += 25
            else:
                if pawns["b"][col] == 0:
                    score -= 25
    
    return score

def evaluate_passed_pawns(state):
    score = 0
    board = state.board
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            
            if piece == "":
                continue
            
            if piece[1] != "p":
                continue
            
            color = piece[0]
            
            if not is_passed_pawn(board, row, col, color):
                continue
            
            advancement = 7 - row if color == "w" else row
            value = 20 + advancement * 10
            
            score += value if color == "w" else -value
    
    return score

def evaluate_king_near_pawns(state):
    score = 0
    board = state.board
    
    wk_pos = state.king_pos["wk"]
    bk_pos = state.king_pos["bk"]
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            
            if piece == "":
                continue
            if piece[1] != "p":
                continue
        
            color = piece[0]
            
            if not is_passed_pawn(board, row, col, color):
                continue
            
            if color == "w":
                distance = king_distance(wk_pos, (row, col))
                
                score -= max(0, 20 - distance * 2)
                
            else:
                distance = king_distance(bk_pos, (row, col))
                
                score += max(0, 20 - distance * 2)
    return score

def evaluate_pawn_race(state):
    score = 0
    board = state.board
    
    wk_pos = state.king_pos["wk"]
    bk_pos = state.king_pos["bk"]
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            
            if piece == "":
                continue
            if piece[1] != "p":
                continue
            
            color = piece[0]
            
            if not is_passed_pawn(board, row, col, color):
                continue
            
            pawn_pos = (row, col)
            
            if color == "w":
                can_intercept = can_king_intercept(state, bk_pos, pawn_pos, color)
                
                if can_intercept:
                    score -= 10
                else:
                    score += 15
            else:
                can_intercept = can_king_intercept(state, wk_pos, pawn_pos, color)
                
                if can_intercept:
                    score += 10
                else:
                    score -= 15
    return score
