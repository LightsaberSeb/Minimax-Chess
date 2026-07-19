import flet

class GUI:
    def __init__(self, main, GameState):
        self.main = main
        self.game_state = GameState
        self.promote_ui = self.build_promotion_ui()
    
    def build_promotion_ui(self):
        return flet.Container(
            bottom=self.main.window_size_y//3,
            alignment=flet.Alignment.TOP_CENTER,
            width=640,
            height=300,
            bgcolor=flet.Colors.with_opacity(0.8, flet.Colors.WHITE_60),
            content=flet.Column(
                controls=[
                    flet.Container(
                        content=flet.Text(
                            "Promote Pawn To:",
                            size=30,
                            weight=flet.FontWeight.BOLD
                        ),
                        alignment=flet.Alignment.CENTER
                    ),
                    flet.Container(
                        expand=True,
                        content=flet.Row(
                            alignment=flet.MainAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                flet.Container(
                                    alignment=flet.Alignment.CENTER,
                                    width=130,
                                    height=130,
                                    content=flet.Image(
                                        src=f"wq.png",
                                        width=130,
                                        height=130,
                                    ),
                                    on_click=lambda e: self.game_state.promoting(self.game_state.moves[-1][0]["target"][0], self.game_state.moves[-1][0]["target"][1], "q"),
                                    bgcolor=flet.Colors.BLUE_200,
                                    ink=True
                                ),
                                flet.Container(
                                    alignment=flet.Alignment.CENTER,
                                    width=130,
                                    height=130,
                                    content=flet.Image(
                                        src=f"wr.png",
                                        width=130,
                                        height=130,
                                    ),
                                    on_click=lambda e: self.game_state.promoting(self.game_state.moves[-1][0]["target"][0], self.game_state.moves[-1][0]["target"][1], "r"),
                                    bgcolor=flet.Colors.BLUE_200,
                                    ink=True
                                ),
                                flet.Container(
                                    alignment=flet.Alignment.CENTER,
                                    width=130,
                                    height=130,
                                    content=flet.Image(
                                        src=f"wb.png",
                                        width=130,
                                        height=130,
                                    ),
                                    on_click=lambda e: self.game_state.promoting(self.game_state.moves[-1][0]["target"][0], self.game_state.moves[-1][0]["target"][1], "b"),
                                    bgcolor=flet.Colors.BLUE_200,
                                    ink=True
                                ),
                                flet.Container(
                                    alignment=flet.Alignment.CENTER,
                                    width=130,
                                    height=130,
                                    content=flet.Image(
                                        src=f"wn.png",
                                        width=130,
                                        height=130,
                                    ),
                                    on_click=lambda e: self.game_state.promoting(self.game_state.moves[-1][0]["target"][0], self.game_state.moves[-1][0]["target"][1], "n"),
                                    bgcolor=flet.Colors.BLUE_200,
                                    ink=True
                                )
                            ]
                        )
                    )
                ]
                ),
            )
    
    # Run the builder functions for the game
    def build_board(self):
        rows = []
        colors = [flet.Colors.BROWN_100, flet.Colors.BROWN]
        for row in range(8):
            cols = []
            for col in range(8):
                color = colors[(row + col) % 2]
                piece = self.game_state.board[row][col]
                content = None

                if self.main.selected_piece == (row, col):
                    color = flet.Colors.YELLOW

                if (row, col) in self.main.selected_moves:
                    color = flet.Colors.BLUE_50

                if piece != "":
                    content = flet.Image(
                        src=f"{piece}.png",
                        width=self.main.tile_size,
                        height=self.main.tile_size,
                    )

                cols.append(
                    flet.Container(
                        width=self.main.tile_size,
                        height=self.main.tile_size,
                        bgcolor=color,
                        content=content,
                        alignment=flet.Alignment.CENTER,
                        on_click=lambda e, r=row, c=col: self.main.on_tile_click(r, c),
                    )
                )

            rows.append(flet.Row(controls=cols, spacing=0))

        return flet.Column(controls=rows, spacing=0)