import flet

import MinimaxAI
import moves


class GameState:
    def __init__(self):
        self.board = [
            ["br", "bb", "bn", "bq", "bk", "bn", "bb", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wb", "wn", "wq", "wk", "wn", "wb", "wr"],
        ]
        self.turn = 1 # 1 for white and 0 for black
        self.can_castle = {"bk": True, "wk": True}
        self.en_passant = None


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
        piece = game_state.board[row][col]
        self.last_selection = (row, col)

        # Piece selection
        if self.selected_piece is None:
            if piece != "":
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
            start_row, start_col = self.selected_piece

            # Making sure that the move is legal
            if not (row, col) in self.selected_moves:
                return
            
            # Check if the moving piece is one of the kings
            if game_state.board[start_row][start_col] in game_state.can_castle:
                game_state.can_castle[game_state.board[start_row][start_col]] = False

            # Moving the piece
            game_state.board[row][col] = game_state.board[start_row][start_col]
            game_state.board[start_row][start_col] = ""
            
            # Check if castling has happened
            if game_state.board[row][col][1] == "k":
                delta = col - start_col
                
                if delta == 2:
                    #short castle
                    rook = game_state.board[row][7]
                    game_state.board[row][5] = rook
                    game_state.board[row][7] = ""
                elif delta == -2:
                    #long castle
                    rook = game_state.board[row][0]
                    game_state.board[row][3] = rook
                    game_state.board[row][0] = ""
            
            # If en passant has happened then, capture the pawn
            if ((row, col) == game_state.en_passant 
                and game_state.board[row][col][1] == "p"
                and start_col != col
                ):
                color = game_state.board[row][col][0]
                if color == "b":
                    game_state.board[row - 1][col] = ""
                else:
                    game_state.board[row + 1][col] = ""
            
            self.check_en_passant((row, col), (start_row, start_col))

            self.selected_piece = None
            self.selected_moves = []

        self.refresh_board()

    def check_en_passant(self, pos, init_pos):
        row, col = pos
        irow, icol = init_pos
        piece = game_state.board[row][col][1]
        color = game_state.board[row][col][0]

        if 0 <= abs(row) < 7 and 0 <= abs(col) < 7:
            right = game_state.board[row][col + 1]
            left = game_state.board[row][col - 1]
        else:
            return

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

        self.app.add(flet.Stack(controls=[self.build_board()]))
        self.app.update()

    # Run the builder functions for the game
    def build_board(self):
        rows = []
        colors = [flet.Colors.BROWN_100, flet.Colors.BROWN]
        for row in range(8):
            cols = []
            for col in range(8):
                color = colors[(row + col) % 2]

                if self.selected_piece == (row, col):
                    color = flet.Colors.YELLOW

                if (row, col) in self.selected_moves:
                    color = flet.Colors.with_opacity(0.1, flet.Colors.BLUE)

                piece = game_state.board[row][col]
                content = None

                if piece != "":
                    content = flet.Image(
                        src=f"{piece}.png",
                        width=self.tile_size,
                        height=self.tile_size,
                    )

                cols.append(
                    flet.Container(
                        width=self.tile_size,
                        height=self.tile_size,
                        bgcolor=color,
                        content=content,
                        alignment=flet.Alignment.CENTER,
                        on_click=lambda e, r=row, c=col: self.on_tile_click(r, c),
                    )
                )

            rows.append(flet.Row(controls=cols, spacing=0))

        return flet.Column(controls=rows, spacing=0)

    # Run the main app
    def run_app(self, app: flet.Page):
        self.app = app
        app.title = "Chess"

        app.window.width = self.window_size_x + 35 # Maybe increase the size of this in the future for settings tab
        app.window.height = self.window_size_y + 60

        app.window.resizable = False
        app.window.maximizable = False

        self.refresh_board()


board = Game()
game_state = GameState()

flet.run(board.run_app, assets_dir="Assets")
