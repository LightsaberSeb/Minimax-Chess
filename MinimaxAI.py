# Minimax AI for the chess engine
import Evaluate
import random

random.seed()
class AI:
    def __init__(self, state, moves, game):
        self.game_state = state
        self.moves = moves
        self.game = game
    
    def search(self, color, alpha, beta, depth):
        maximizer = color == "w"
        legal_moves = self.moves.get_legal_moves(color, self.game_state)
        best_moves = []
        best_score = float("-inf") if maximizer else float("inf")
        
        if len(legal_moves) == 0:
            print("No more legal moves")
            return
        
        for move in legal_moves:
            start, end = move
            self.moves.make_move(start[0], start[1], end[0], end[1], self.game_state)
            score = self.minimax(self.game_state.opposite(color), alpha, beta, depth-1)
            self.moves.undo_move(self.game_state)
            
            if maximizer:
                if score > best_score:
                    best_score = score
                    best_moves = [{
                        "start": start,
                        "end": end
                    }]
                elif score == best_score:
                    best_moves.append({
                        "start": start,
                        "end": end
                    })
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_moves = [{
                        "start": start,
                        "end": end
                    }]
                elif score == best_score:
                    best_moves.append({
                        "start": start,
                        "end": end
                    })
                beta = min(beta, best_score)

        return best_moves[0]

    def minimax(self, color, alpha, beta, depth):
        if depth == 0:
            return Evaluate.evaluate(self.game_state)
        
        maximizer = color == "w"
        legal_moves = self.moves.get_legal_moves(color, self.game_state)
        best_score = float("-inf") if maximizer else float("inf")
        
        if len(legal_moves) == 0:
            return Evaluate.evaluate(self.game_state)
        
        for move in legal_moves:
            start, end = move
            self.moves.make_move(start[0], start[1], end[0], end[1], self.game_state)
            score = self.minimax(self.game_state.opposite(color), alpha, beta, depth-1)
            self.moves.undo_move(self.game_state)
        
            if maximizer:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)

            if beta <= alpha:
                break
            
        return best_score
