import tkinter as tk
from tkinter import messagebox
from GameClasses import Board, Move, Minimax, PlayerType, PieceType, Piece
from PIL import Image, ImageTk, ImageDraw

class SimpleCheckersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Checkers")

        menu_bar = tk.Menu(self.root)
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Difficulty", command=self.difficulty)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.exit_game)
        menu_bar.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        try:
            self.board_image = Image.open("board.png")
            self.board_photo = ImageTk.PhotoImage(self.board_image)
        except:
            messagebox.showerror("Error", "Cannot load board.png")
            self.root.quit()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.buffer = Image.new("RGB", (500, 500))
        self.buffer_draw = ImageDraw.Draw(self.buffer)

        self.board = Board()
        self.current_player = PlayerType.Human
        self.selected_piece = None

        self.draw_board()

    def draw_board(self):
        self.buffer.paste(self.board_image, (0, 0))
        
        dy = 500 - 125 + 12

        for p in self.board.pieces:
            color = (255, 255, 255) if p.player == PlayerType.Computer else (0, 0, 0)
            if p.player == PlayerType.Human and p.id == self.selected_piece:
                color = (255, 255, 0)
            if p.type==PieceType.Flat:
                self.buffer_draw.rectangle([12 + p.x * 125, dy - p.y * 125, 112 + p.x * 125, dy + 100 - p.y * 125], fill=color)
            else:
                self.buffer_draw.rectangle([12 + p.x * 125, dy - p.y * 125, 112 + p.x * 125, dy + 50 - p.y * 125], fill=color)

        self.tk_buffer = ImageTk.PhotoImage(self.buffer)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_buffer)

    def on_canvas_click(self, event):
        if self.current_player != PlayerType.Human:
            return

        mouse_x = event.x // 125
        mouse_y = 3 - (event.y // 125)

        if self.selected_piece is None:
            for p in self.board.pieces:
                if p.player == PlayerType.Human and p.x == mouse_x and p.y == mouse_y:
                    self.selected_piece = p.id
                    self.draw_board()
                    return
        else:
            selected_piece = self.board.pieces[self.selected_piece]
            move = Move(self.selected_piece, mouse_x, mouse_y)

            if selected_piece.is_valid_move(self.board, move):
                self.selected_piece = None
                new_board = self.board.make_move(move)
                self.board = new_board
                self.draw_board()

                self.current_player = PlayerType.Computer
                self.check_finish()
                
                if self.current_player == PlayerType.Computer:
                    self.computer_move()

    def computer_move(self):
        next_board = Minimax.find_next_board(self.board)
        self.board = next_board
        self.draw_board()

        self.current_player = PlayerType.Human
        self.check_finish()

    def check_finish(self):
        finished, winner = self.board.check_finish()
        if finished:
            if winner == PlayerType.Computer:
                messagebox.showinfo("Game Over", "Calculatorul a castigat!")
            elif winner == PlayerType.Human:
                messagebox.showinfo("Game Over", "Ai castigat!")
            self.current_player = PlayerType.NoPlayer

    def new_game(self):
        self.board = Board()
        self.current_player = PlayerType.Computer
        self.computer_move()

    def difficulty(self):
        raise Exception("Aceasta metoda trebuie implementata")

    def exit_game(self):
        self.root.quit()

    def show_about(self):
        about_text = (
            "Algoritmul minimax\r\n" 
            "Inteligenta artificiala, Laboratorul 7\r\n" 
            "(c)2024 Florin Leon\r\n" 
            "http://florinleon.byethost24.com/lab_ia.html"
        )
        messagebox.showinfo("Despre jocul Dame simple", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCheckersApp(root)
    root.mainloop()
