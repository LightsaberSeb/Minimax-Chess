import flet
import random

from MinimaxAI import AI
import moves
from Interface import GUI

class GameState:
    def __init__(self):
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]
        self.user_color = random.choice(["w","b"])
        self.ai_color = "b" if self.user_color == "w" else "w"
        self.turn = "w"
        self.can_castle = {"bk": True, "wk": True}
        self.king_pos = {"bk": (0, 4), "wk": (7, 4)}
        self.check = {"bk": False, "wk": False}
        self.en_passant = None
        self.is_promoting = False
        self.moves = []

        self.move_functions = {
            "p": moves.pawn_moves,
            "n": moves.knight_moves,
            "b": moves.bishop_moves,
            "r": moves.rook_moves,
            "q": moves.queen_moves,
            "k": moves.king_moves,
        }
        
    def change_turn(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"
    
    def promoting(self, row: int, col: int, promote: str):
        piece = self.board[row][col]
        color = piece[0]
        
        self.board[row][col] = color+promote
        self.is_promoting = False
        game.finish_move()
    
    def opposite(self, color):
        if color == "w":
            return "b"
        else:
            return "w"
    
    def get_king_state(self, color: str):
        legal_moves = moves.get_legal_moves(color, self)
        in_check = moves.is_on_check(color, self)
        
        if in_check and len(legal_moves) == 0:
            return "checkmate"
        
        if in_check:
            return "check"
        
        if len(legal_moves) == 0:
            return "stalemate"
        
        return "normal"

class Game:
    def __init__(self):
        # Window settings
        self.app = None
        self.window_size_x = 640
        self.window_size_y = 640
        self.tile_size = self.window_size_x / 8

        # Mouse
        self.selected_piece = None
        self.last_selection = None
        self.selected_moves = []

        # Class instances
        self.gui = GUI(self, game_state)
        self.ai = AI(game_state, moves, self)

    def on_tile_click(self, row, col):
        if game_state.is_promoting:
            return
        
        piece = game_state.board[row][col]
        self.last_selection = (row, col)

        # Piece selection
        if self.selected_piece is None:
            if piece != "":
                # Cancel the selection if the color doesn't correspond with the turn
                if piece[0] != game_state.user_color:
                    return
                
                self.selected_piece = (row, col)
                self.selected_moves = game_state.move_functions[piece[1]](
                    row, col, game_state
                )
        elif self.selected_piece == self.last_selection:
            self.selected_piece = (
                None  # Cancel the selection if clicking the same piece
            )
            self.selected_moves = []
        else:
            start_row, start_col = self.selected_piece
            piece = game_state.board[start_row][start_col]
            color = piece[0]
            opposite = game_state.opposite(color)
            
            # Making sure that the move is legal
            if not (row, col) in self.selected_moves:
                return
            
            # Check if the moving piece is one of the kings
            if game_state.board[start_row][start_col] in game_state.can_castle:
                game_state.can_castle[game_state.board[start_row][start_col]] = False
            
            # Moving the piece
            move = {
                "start": (start_row, start_col),
                "end": (row, col)
            }
            
            self.process_move(move, color, opposite)

        self.refresh_board()

    def process_move(self, move, color, opposite):
        moves.make_move(move["start"][0], move["start"][1], move["end"][0], move["end"][1], game_state)
        
        if game_state.get_king_state(color) == "check":
            moves.undo_move(game_state)
            return
        
        match game_state.get_king_state(opposite):
            case "normal":
                game_state.check[opposite+"k"] = False
            case "check":
                game_state.check[opposite+"k"] = True
            case "checkmate":
                print(f"{opposite} is on checkmate")
            case "stalemate":
                print(f"{opposite} is on stalemate")

        self.check_en_passant((move["end"][0], move["end"][1]), (move["start"][0], move["start"][1]))

        # Check if a pawn is promoting
        if game_state.moves[-1][0]["type"] == "promotion":
            game_state.is_promoting = True
            self.refresh_board()
            return

        self.finish_move()

    def finish_move(self):
        self.selected_piece = None
        self.selected_moves = []
        game_state.change_turn()
        self.refresh_board()
        self.update()
    
    def update(self):
        if game_state.turn == game_state.user_color:
            return
        
        if game_state.turn == game_state.ai_color:
            move = self.ai.search(game_state.ai_color, float("-inf"), float("inf"), 3)
            
            if move is None:
                print("Game Over")
                return
            
            self.process_move(move, game_state.ai_color, game_state.opposite(game_state.ai_color))

    def check_en_passant(self, pos, init_pos):
        row, col = pos
        irow, icol = init_pos
        piece = game_state.board[row][col][1]
        color = game_state.board[row][col][0]
        left = ""
        right = ""

        if col > 0:
            left = game_state.board[row][col - 1]

        if col < 7:
            right = game_state.board[row][col + 1]

        if piece != "p":
            game_state.en_passant = None
            return

        drow = row - irow
        dcol = col - icol
        if dcol != 0 or abs(drow) != 2:
            game_state.en_passant = None
            return
        
        if (right != "" and right[1] == "p" and color != right[0]) or (left != "" and left[1] == "p" and color != left[0]):
            game_state.en_passant = ((irow + row) // 2, col)

    def refresh_board(self):
        self.app.controls.clear()
        
        containers = [self.gui.build_board()]

        if game_state.is_promoting:
            containers.append(self.gui.promote_ui)
        else:
            if self.gui.promote_ui in containers:
                containers.remove(self.gui.promote_ui)

        self.app.add(flet.Stack(controls=containers))
        self.app.update()

    # Run the main app
    def run_app(self, app: flet.Page):
        self.app = app
        app.title = "Chess"

        app.window.width = self.window_size_x + 35 # Maybe increase the size of this in the future for settings tab
        app.window.height = self.window_size_y + 60

        app.window.resizable = False
        app.window.maximizable = False

        self.refresh_board()
        self.update()

game_state = GameState()
game = Game()

flet.run(game.run_app, assets_dir="Assets")
