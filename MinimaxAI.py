# Minimax AI for the chess engine
import Evaluate
import random
class AI:
    def __init__(self, state, moves, game):
        self.game_state = state
        self.moves = moves
        self.game = game
    
    def search(self, color, depth):
        maximizer = color == "w"
        legal_moves = self.moves.get_legal_moves(color, self.game_state)
        best_moves = []
        best_score = float("-inf") if maximizer else float("inf")
        
        for move in legal_moves:
            start, end = move
            self.moves.make_move(start[0], start[1], end[0], end[1], self.game_state)
            score = self.minimax(self.game_state.opposite(color), depth-1)
            self.moves.undo_move(self.game_state)
        
            if maximizer:
                better = score > best_score
                equal = score == best_score
            else:
                better = score < best_score
                equal = score == best_score
            
            if better:
                best_score = score
                best_moves = [{
                    "start": start,
                    "end": end
                }]
            elif equal:
                best_moves.append({
                    "start": start,
                    "end": end
                })
        return random.choice(best_moves)

    def minimax(self, color, depth):
        maximizer = color == "w"
        legal_moves = self.moves.get_legal_moves(color, self.game_state)
        best_score = float("-inf") if maximizer else float("inf")
        
        if depth == 0:
            return Evaluate.evaluate(self.game_state.board)
        
        for move in legal_moves:
            start, end = move
            self.moves.make_move(start[0], start[1], end[0], end[1], self.game_state)
            score = self.minimax(self.game_state.opposite(color), depth-1)
            self.moves.undo_move(self.game_state)
        
            if maximizer:
                better = score > best_score
            else:
                better = score < best_score
            
            if better:
                best_score = score
        return best_score
