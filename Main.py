import flet
import random

import MinimaxAI
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
        self.turn = "w"
        self.start = random.randint(0, 1) # 0 for user 1 for minimax
        self.can_castle = {"bk": True, "wk": True}
        self.king_pos = {"bk": (0, 4), "wk": (7, 4)}
        self.check = {"bk": False, "wk": False}
        self.en_passant = None
        self.is_promoting = False
        self.moves = []
    
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
        game.refresh_board()
    
    def opposite(self, color):
        if color == "w":
            return "b"
        else:
            return "w"


class Game:
    def __init__(self):
        # Window settings
        self.app = None
        self.window_size_x = 640
        self.window_size_y = 640
        self.tile_size = self.window_size_x / 8
        self.gui = GUI(self, game_state)

        # Mouse
        self.selected_piece = None
        self.last_selection = None
        self.selected_moves = []

        # Game settings
        self.move_functions = {
            "p": moves.pawn_moves,
            "n": moves.knight_moves,
            "b": moves.bishop_moves,
            "r": moves.rook_moves,
            "q": moves.queen_moves,
            "k": moves.king_moves,
        }

    def on_tile_click(self, row, col):
        if game_state.is_promoting:
            return
        
        piece = game_state.board[row][col]
        self.last_selection = (row, col)

        # Piece selection
        if self.selected_piece is None:
            if piece != "":
                # Cancel the selection if the color doesn't correspond with the turn
                if game_state.turn != piece[0]:
                    return
                
                self.selected_piece = (row, col)
                self.selected_moves = self.move_functions[piece[1]](
                    row, col, game_state
                )
        elif self.selected_piece == self.last_selection:
            self.selected_piece = (
                None  # Cancel the selection if clicking the same piece
            )
            self.selected_moves = []
        else:
            type = "normal"
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

            # Castling
            if piece[1] == "k":
                if abs(col - start_col) == 2:
                    type = "castle"

            # En passant
            if ((row, col) == game_state.en_passant 
                and piece[1] == "p"
                and start_col != col
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
            
            # Moving the piece
            moves.make_move(start_row, start_col, row, col, type, game_state)
            
            if moves.is_on_check(color, game_state):
                moves.undo_move(game_state)
                return
            
            game_state.check[opposite+"k"] = moves.is_on_check(opposite, game_state)
            
            if piece[1] == "k":
                game_state.king_pos[piece] = (row, col)

            self.check_en_passant((row, col), (start_row, start_col))

            self.selected_piece = None
            self.selected_moves = []

        self.refresh_board()

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

game_state = GameState()
game = Game()

flet.run(game.run_app, assets_dir="Assets")
