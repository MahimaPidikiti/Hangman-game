import tkinter as tk
from tkinter import messagebox
import random

# List of words
word_list = ['python', 'hangman', 'challenge', 'programming', 'developer', 'keyboard', 'internet']

# Global variables
guessed_letters = []
lives = 6
chosen_word = ''
display_word = []

# Create main window
root = tk.Tk()
root.title("Hangman Game")
root.geometry("520x500")
root.resizable(False, False)
root.configure(bg="#1e1e1e")  # Dark background

# Label for the word display
word_label = tk.Label(root, text="", font=("Consolas", 26), fg="white", bg="#1e1e1e")
word_label.pack(pady=20)

# Canvas for hangman drawing
canvas = tk.Canvas(root, width=200, height=200, bg="#1e1e1e", highlightthickness=0)
canvas.pack()

# Button frame
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

# Restart button
restart_btn = tk.Button(root, text="🔄 Restart", font=("Arial", 12, "bold"), bg="#333", fg="white", command=lambda: start_game())
restart_btn.pack(pady=5)

# Hangman drawing logic
def draw_hangman(lives_left):
    canvas.delete("all")
    if lives_left < 6: canvas.create_line(20, 180, 180, 180, fill='white')     # base
    if lives_left < 5: canvas.create_line(50, 180, 50, 20, fill='white')       # pole
    if lives_left < 4: canvas.create_line(50, 20, 130, 20, fill='white')       # top bar
    if lives_left < 3: canvas.create_line(130, 20, 130, 40, fill='white')      # rope
    if lives_left < 2: canvas.create_oval(115, 40, 145, 70, outline='white')   # head
    if lives_left < 1:
        canvas.create_line(130, 70, 130, 120, fill='white')                    # body
        canvas.create_line(130, 80, 110, 100, fill='white')                    # left arm
        canvas.create_line(130, 80, 150, 100, fill='white')                    # right arm
        canvas.create_line(130, 120, 110, 150, fill='white')                   # left leg
        canvas.create_line(130, 120, 150, 150, fill='white')                   # right leg

# Guessing logic
def guess_letter(letter, btn):
    global lives
    if letter in guessed_letters:
        return
    guessed_letters.append(letter)
    btn.config(state='disabled', bg="gray")

    if letter in chosen_word:
        for i, l in enumerate(chosen_word):
            if l == letter:
                display_word[i] = letter
        word_label.config(text=' '.join(display_word))
    else:
        lives -= 1
        draw_hangman(lives)

    check_game_status()

# Win/Lose check
def check_game_status():
    if '_' not in display_word:
        messagebox.showinfo("🎉 You Win!", f"The word was: {chosen_word}")
        disable_all_buttons()
    elif lives == 0:
        word_label.config(text=chosen_word)
        draw_hangman(lives)
        messagebox.showinfo("💀 You Lost", f"The word was: {chosen_word}")
        disable_all_buttons()

# Disable all buttons
def disable_all_buttons():
    for btn in buttons:
        btn.config(state='disabled')

# Game start / restart
def start_game():
    global chosen_word, display_word, guessed_letters, lives, buttons

    chosen_word = random.choice(word_list).lower()
    display_word = ['_' for _ in chosen_word]
    guessed_letters = []
    lives = 6

    word_label.config(text=' '.join(display_word))
    draw_hangman(lives)

    # Clear and recreate letter buttons
    for widget in button_frame.winfo_children():
        widget.destroy()

    buttons = []
    for i, letter in enumerate('abcdefghijklmnopqrstuvwxyz'):
        btn = tk.Button(button_frame, text=letter.upper(), width=4, font=("Arial", 10, "bold"),
                        bg="#555", fg="white", activebackground="#777",
                        command=lambda l=letter, b=None: guess_letter(l, b))
        buttons.append(btn)

    # Assign reference after creation
    for i, btn in enumerate(buttons):
        btn.config(command=lambda l='abcdefghijklmnopqrstuvwxyz'[i], b=btn: guess_letter(l, b))
        btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)

# Start game for first time
start_game()

# Main loop
root.mainloop()
