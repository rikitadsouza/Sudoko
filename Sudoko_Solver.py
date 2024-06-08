import tkinter as tk
from tkinter import messagebox

class SudokuSolverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")

        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=450, height=450, bg="white")
        self.canvas.pack()

        self.draw_board()

        self.solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        self.solve_button.pack()

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear)
        self.clear_button.pack()

        self.instructions_label = tk.Label(self.master, text="Enter the number in the cell to solve:")
        self.instructions_label.pack()

        self.row_entry = tk.Entry(self.master, width=3)
        self.row_entry.pack()

        self.column_entry = tk.Entry(self.master, width=3)
        self.column_entry.pack()

        self.number_entry = tk.Entry(self.master, width=3)
        self.number_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.pack()

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                x0 = j * 50
                y0 = i * 50
                x1 = x0 + 50
                y1 = y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                if self.board[i][j] != 0:
                    self.canvas.create_text(x0 + 25, y0 + 25, text=str(self.board[i][j]))

    def solve(self):
        solved_board = [row[:] for row in self.board]  # Copy the original board
        if self.solve_sudoku(solved_board):
            self.update_board(solved_board)
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists for this puzzle.")

    def solve_sudoku(self, board):
        find = self.find_empty_location(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve_sudoku(board):
                    return True

                board[row][col] = 0

        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        # Check row
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def clear(self):
        self.update_board(self.board)

    def submit(self):
        try:
            row = int(self.row_entry.get()) - 1
            col = int(self.column_entry.get()) - 1
            num = int(self.number_entry.get())

            if 0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9:
                if self.board[row][col] == 0:
                    if self.is_valid(self.board, num, (row, col)):
                        self.board[row][col] = num
                        self.update_board(self.board)
                    else:
                        messagebox.showerror("Sudoku Solver", "Invalid move! Please try again.")
                else:
                    messagebox.showerror("Sudoku Solver", "Cell is already filled.")
            else:
                messagebox.showerror("Sudoku Solver", "Please enter valid row (1-9), column (1-9), and number (1-9).")
        except ValueError:
            messagebox.showerror("Sudoku Solver", "Please enter valid integers.")

    def update_board(self, board):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    x0 = j * 50 + 25
                    y0 = i * 50 + 25
                    self.canvas.create_text(x0, y0, text=str(board[i][j]), tags="numbers")

def main():
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
