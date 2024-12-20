import random
import tkinter as tk
from tkinter import messagebox

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Generate a random number
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # GUI elements
        self.label = tk.Label(root, text="Guess the number (between 1 and 100):", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Submit", font=("Arial", 12), command=self.check_guess)
        self.button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if guess < 1 or guess > 100:
                self.result_label.config(text="Please enter a number between 1 and 100.")
            elif guess < self.secret_number:
                self.result_label.config(text="Too low! Try again.")
            elif guess > self.secret_number:
                self.result_label.config(text="Too high! Try again.")
            else:
                messagebox.showinfo("Congratulations!", f"You guessed the number {self.secret_number} correctly in {self.attempts} attempts!")
                self.reset_game()
        except ValueError:
            self.result_label.config(text="Invalid input! Please enter a valid number.")

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
