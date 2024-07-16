import tkinter as tk
from tkinter import messagebox

def check_winner():
    global winner
    for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] and buttons[combo[0]]["text"] != "":
            for index in combo:
                buttons[index].config(bg="green")
            winner = True
            messagebox.showinfo("Tic-Tac-Toe", f"Player {buttons[combo[0]]['text']} wins!")
            return

def button_click(index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
        check_winner()
        if not winner:
            toggle_player()
        elif winner:
            label.config(text=f"Player {buttons[index]['text']} wins!")

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Current player: {current_player}")

def reset_game():
    global winner, current_player
    winner = False
    current_player = "X"
    label.config(text=f"Current player: {current_player}")
    for button in buttons:
        button.config(text="", bg="SystemButtonFace")

root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = [tk.Button(root, text="", font=("normal", 25), width=6, height=2, command=lambda i=i: button_click(i)) for i in range(9)]

for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

current_player = "X"
winner = False

label = tk.Label(root, text=f"Current player: {current_player}", font=("normal", 16))
label.grid(row=3, column=0, columnspan=3)

reset_button = tk.Button(root, text="Reset", font=("normal", 16), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
