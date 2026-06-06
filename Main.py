import random
import flet
import moves
import MinimaxAI

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
        self.turn = random.randint(0, 1) # 0 for black, 1 for white
        self.move_functions = {
            "p" : moves.pawn_moves,
            "n" : moves.knight_moves,
            "b" : moves.bishop_moves,
            "r" : moves.rook_moves,
            "q" : moves.queen_moves,
            "k" : moves.king_moves
        }
        self.board = [
            ["br","bb","bn","bq","bk","bn","bb","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wb","wn","wq","wk","wn","wb","wr"],
        ]
        self.can_castle = {
            "bk" : True,
            "wk" : True
        }

    def on_tile_click(self, row, col):
        piece = self.board[row][col]
        self.last_selection = (row, col)
        
        # Piece selection
        if self.selected_piece is None:
            if piece != "":
                self.selected_piece = (row, col)
                self.selected_moves = self.move_functions[piece[1]](row, col, self.board)
        
        elif self.selected_piece == self.last_selection:
            self.selected_piece = None # Cancel the selection if clicking the same piece
            self.selected_moves = []

        else:
            start_row, start_col = self.selected_piece

            # Check if the moving piece is one of the kings
            if self.board[start_row][start_col] in self.can_castle:
                self.can_castle[self.board[start_row][start_col]] = False
            
            # Making sure that the move is legal
            if not (row, col) in self.selected_moves:
                return
            
            # Moving the piece
            self.board[row][col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = ""
            
            self.selected_piece = None
            self.selected_moves = []
        
        self.refresh_board()

    def refresh_board(self):
        self.app.controls.clear()
        
        self.app.add(
            flet.Stack(
                controls=[
                    self.build_board()
                ]
            )
        )
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

                piece = self.board[row][col]
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
                        on_click=lambda e, r=row, c=col:
                            self.on_tile_click(r, c)
                    )
                )

            rows.append(
                flet.Row(
                    controls=cols,
                    spacing=0
                )
            )

        return flet.Column(
            controls=rows,
            spacing=0
        )
        
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

flet.run(board.run_app, assets_dir="Assets")
