import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Game settings
GRID_SIZE = 6
NUM_MINES = 3
SAFE_CELL_REWARD = 10  # Points awarded for a safe cell
STARTING_BALANCE = 500  # Starting wallet balance


class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper with Wallet and Scoring")
        self.buttons = []
        self.mines = []
        self.wallet_balance = STARTING_BALANCE  # Player's wallet balance
        self.bet_history = []  # List to track betting history
        self.amount = 0  # User's current bet amount
        self.points = 0  # Points earned in the current game
        self.initialize_game()

    def initialize_game(self):
        """Initialize the game grid and wallet system."""
        if self.wallet_balance <= 0:
            messagebox.showinfo("Game Over", "Your wallet is empty. Thanks for playing!")
            self.root.destroy()
            return

        self.amount = simpledialog.askinteger(
            "Place Your Bet",
            f"Enter your bet amount (Wallet: ${self.wallet_balance}):",
            minvalue=10,
            maxvalue=self.wallet_balance
        )
        if self.amount is None:  # User cancels
            self.root.destroy()
            return

        self.wallet_balance -= self.amount
        self.bet_history.append(self.amount)
        self.points = 0

        self.create_side_panel()
        self.create_grid()
        self.place_mines()
        self.update_status()

    def create_side_panel(self):
        """Create the side panel for wallet balance, scoring, and betting history."""
        side_panel = tk.Frame(self.root, bg="#2c2f33", relief="raised", borderwidth=3)
        side_panel.grid(row=0, column=GRID_SIZE, rowspan=GRID_SIZE + 2, padx=5, pady=5, sticky="ns")

        wallet_label = tk.Label(side_panel, text="Wallet Balance:", font=("Arial", 12, "bold"), bg="#2c2f33",
                                fg="white")
        wallet_label.pack(pady=5)

        self.wallet_display = tk.Label(side_panel, text=f"${self.wallet_balance}", font=("Arial", 14), bg="#23272a",
                                       fg="lime", width=15, relief="ridge")
        self.wallet_display.pack(pady=5)

        status_label = tk.Label(side_panel, text="Winning Amount:", font=("Arial", 12, "bold"), bg="#2c2f33",
                                fg="white")
        status_label.pack(pady=5)

        self.status_display = tk.Label(side_panel, text=f"${self.points}", font=("Arial", 14), bg="#23272a",
                                       fg="yellow", width=15, relief="ridge")
        self.status_display.pack(pady=5)

        history_label = tk.Label(side_panel, text="Bet History:", font=("Arial", 12, "bold"), bg="#2c2f33", fg="white")
        history_label.pack(pady=5)

        self.history_listbox = tk.Listbox(side_panel, font=("Arial", 10), bg="#23272a", fg="white", width=15, height=10)
        for bet in self.bet_history:
            self.history_listbox.insert(tk.END, f"${bet}")
        self.history_listbox.pack(pady=5)

        cashout_button = tk.Button(side_panel, text="Cash Out", command=self.cash_out, font=("Arial", 10, "bold"),
                                   bg="orange", fg="black", width=15)
        cashout_button.pack(pady=10)

    def create_grid(self):
        """Create a grid of buttons with dark gray background and smaller border."""
        self.buttons = []
        for r in range(GRID_SIZE):
            row_buttons = []
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.root,
                    text="?",
                    width=10,
                    height=4,
                    bg="darkgray",
                    font=("Arial", 12, "bold"),
                    relief="solid",
                    borderwidth=2,
                    command=lambda r=r, c=c: self.reveal(r, c)
                )
                btn.grid(row=r + 2, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def place_mines(self):
        """Randomly place mines on the grid."""
        mine_locations = random.sample(range(GRID_SIZE * GRID_SIZE), NUM_MINES)
        self.mines = [(loc // GRID_SIZE, loc % GRID_SIZE) for loc in mine_locations]

    def reveal(self, row, col):
        """Reveal the cell content (mine or safe)."""
        if (row, col) in self.mines:
            # Hit a mine: Game over
            self.buttons[row][col].config(text="*", bg="red")
            messagebox.showinfo("Game Over", f"You hit a mine! You lost your bet of ${self.amount}.")
            self.reset_game()
        else:
            # Safe cell: Add points
            self.points += SAFE_CELL_REWARD
            self.wallet_balance += SAFE_CELL_REWARD  # Add to wallet immediately
            self.buttons[row][col].config(
                text=self.get_adjacent_mines(row, col),
                bg="green",
                state="disabled"
            )
            self.update_status()

    def get_adjacent_mines(self, row, col):
        """Count adjacent mines for a given cell."""
        adjacent_mines = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    if (r, c) in self.mines:
                        adjacent_mines += 1
        return str(adjacent_mines) if adjacent_mines > 0 else " "

    def update_status(self):
        """Update the wallet balance, winning amount, and bet history."""
        self.wallet_display.config(text=f"${self.wallet_balance}")
        self.status_display.config(text=f"${self.points}")
        self.history_listbox.delete(0, tk.END)
        for bet in self.bet_history:
            self.history_listbox.insert(tk.END, f"${bet}")

    def cash_out(self):
        """Allow the user to cash out their winnings."""
        if messagebox.askyesno("Cash Out", f"Do you want to cash out your current total of ${self.wallet_balance}?"):
            messagebox.showinfo("Cash Out", f"You cashed out ${self.wallet_balance}. Thanks for playing!")
            self.root.destroy()
        else:
            messagebox.showinfo("Keep Playing", "Continue playing to increase your points!")

    def reset_game(self):
        """Reset the game after a loss."""
        self.points = 0
        self.amount = 0
        self.initialize_game()


def main():
    root = tk.Tk()
    root.configure(bg="#2c2f33")
    game = Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()
