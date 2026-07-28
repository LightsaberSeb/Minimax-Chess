PIECE_VALUES = {
    "p": 100,
    "n": 320,
    "b": 330,
    "r": 500,
    "q": 900,
    "k": 0
}

EVAL_WEIGHTS = {
    "material": 1.0,
    "mobility": 0.2,
    "king_safety": 0.5,
    "center_control": 0.3
}


def evaluate(board):
    score = 0
    
    score += evaluate_material(board)
    
    return score


def evaluate_material(board):
    score = 0
    
    for row in board:
        for piece in row:
            if piece == "":
                continue
            
            color = piece[0]
            piece_type = piece[1]
            
            value = PIECE_VALUES[piece_type]
            
            if color == "w":
                score += value
            elif color == "b":
                score -= value
    
    return score
