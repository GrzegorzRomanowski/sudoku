# SUDOKU

import random
import tkinter as tk
from raw_data import *

# Fonts and font sizes
f = "Comic Sans MS"
s = "14"

#
# Init empty list for buttons 9 x 9
button_list = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
# Init empty list for buttons 9 x 9 - duplicated version of 'button_list' with filled values during the game
current_puzzle2 = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
# Init empty list of buttons used to typing numbers from 1 to 9
writing_button_list = [[0]*3, [0]*3, [0]*3]
# Init of global variables containing current number to type
number_to_type = ""

# Main App Window from Tkinter
main_window = tk.Tk()
main_window.title("SUDOKU")
main_window.iconbitmap("icon.ico")
main_window.geometry("450x670")

main_frame = tk.Frame(main_window)
main_frame.pack(pady=10)

# Init a Tkinter buttons 9 x 9 and paint then like a yellow/blue chessboard. Buttons have no command in this stage.
for row in range(9):
    for column in range(9):
        if (((row // 3) + 1) * ((column // 3) + 1)) % 2 == 0:
            colour = "Yellow"
        else:
            colour = "Light Blue"
        if (((row // 3) + 1) * ((column // 3) + 1)) == 4:
            colour = "Light BLue"
        button = tk.Button(main_frame, text="", font=(f, s, 'bold'), width=3, command=None, bg=colour)
        button.grid(row=row, column=column, padx=1, pady=1)
        button_list[row][column] = button


def pull():
    puzzle = random.choice(raw_sudoku)
    return tuple(puzzle)

def load_puzzel_frame():
    global current_puzzle2, current_puzzle
    for gggg in range(9):
        for ggggg in range(9):
            current_puzzle2[gggg][ggggg] = current_puzzle[gggg][ggggg]
    for q in button_list:
        for w in q:
            w.config(state=tk.NORMAL)
    for m in range(9):
        for n in range(9):
            num1 = current_puzzle[m][n]
            if num1 == 0:
                num = ""
            else:
                num = num1
                button_list[m][n].config(state=tk.DISABLED, fg="Black")
            button_list[m][n].config(text=num)

def new_game():
    global current_puzzle
    current_puzzle = pull()
    load_puzzel_frame()

writing_frame = tk.Frame(main_window)
writing_frame.pack(side=tk.LEFT, padx=10)
button_new_game = tk.Button(main_window, text="New game", font=(f, s,), width=22, command=new_game)
button_new_game.pack(anchor=tk.E, padx=10, pady=27)
button_reset = tk.Button(main_window, text="Restart current game", font=(f, s,), width=22, command=load_puzzel_frame)
button_reset.pack(anchor=tk.E, padx=10, pady=25)

for k in range(3):
    for l in range(3):
        writing_button = tk.Button(writing_frame, text=(k*3+l+1), font=(f, s), width=3, command=None, bg="Silver", fg="Black")
        writing_button.grid(row=k, column=l, padx=1, pady=1)
        writing_button_list[k][l] = writing_button

def clean():
    global number_to_type
    number_to_type = 0
    for c in writing_button_list:
        for d in c:
            d.config(bg="Silver", fg="Black")
    zero_button.config(bg="Black", fg="White")
zero_button = tk.Button(writing_frame, text="Clean", font=(f, s), command=clean, bg="Silver", fg="Black")
zero_button.grid(row=3, column=0, columnspan=3, padx=1, pady=1, sticky=tk.NSEW)

def pick(k,l):
    def pick2():
        global number_to_type
        number_to_type = (k * 3 + l + 1)
        for c in writing_button_list:
            for d in c:
                d.config(bg="Silver", fg="Black")
        zero_button.config(bg="Silver", fg="Black")
        writing_button_list[k][l].config(bg="Black", fg="White")
    return pick2

a = 0
while a < 3:
    for h in writing_button_list[a]:
        b = writing_button_list[a].index(h)
        writing_button_list[a][b].config(command=pick(a, b))
    a += 1

def warning():
    warning_window = tk.Toplevel()
    warning_window.title("Warning")
    warning_window.iconbitmap('C:/Dane/Python/Wlasne/Sudoku/icon.ico')
    warning_text = "You cannot enter the selected number\nin this field!"
    war = tk.Label(warning_window, text=warning_text, font=(f, s), padx=10, pady=10)
    war.pack()
    def war_destroy():
        warning_window.destroy()
    war_button = tk.Button(warning_window, text="OK", width=10, font=(f, s), command=war_destroy)
    war_button.pack(padx=10, pady=10)
    warning_window.mainloop()

def finished():
    finished_window = tk.Toplevel()
    finished_window.title("Congratulations !")
    finished_window.iconbitmap('C:/Dane/Python/Wlasne/Sudoku/icon.ico')
    finished_text = "YOU WIN!"
    fin = tk.Label(finished_window, text=finished_text, font=(f, s), padx=10, pady=10)
    fin.pack()
    def fin_destroy():
        finished_window.destroy()
        new_game()
    fin_button = tk.Button(finished_window, text="New game?", width=10, font=(f, s), command=fin_destroy)
    fin_button.pack(padx=10, pady=10)
    finished_window.mainloop()

def check():
    for z in range(1, 10):
        # horizontal check
        for zz in current_puzzle2:
            horizontal = zz.count(z)
            if horizontal > 1:
                return 0
        # vertical check
        g = 0
        while g < 9:
            vertical_list = []
            for zzz in current_puzzle2:
                vertical_list.append(zzz[g])
            vertical = vertical_list.count(z)
            if vertical > 1:
                return 0
            g += 1
        # square check
        for t in range(3):
            for tt in range(3):
                square_list = []
                u = 0
                while u < 9:
                    v = 0
                    while v < 9:
                        if (u // 3) == t and (v // 3) == tt:
                            square_list.append(current_puzzle2[u][v])
                        v += 1
                    u += 1
                square = square_list.count(z)
                if square > 1:
                    return 0
    return 1

def win():
    win_list = []
    for ww in current_puzzle2:
        for www in ww:
            win_list.append(www)
    game_ended = win_list.count(0)
    if game_ended == 0:
        return 1
    else:
        return 0

def put(kk,ll):
    def put2():
        global number_to_type
        current_puzzle2[kk][ll] = number_to_type
        cannot = check()
        if cannot == 1:
            if number_to_type == 0:
                button_list[kk][ll].config(text="")
            else:
                button_list[kk][ll].config(text=number_to_type)
        elif cannot == 0:
            current_puzzle2[kk][ll] = 0
            warning()
        winner = win()
        if winner == 1:
            finished()
    return put2

aa = 0
while aa < 9:
    for hh in button_list[aa]:
        bb = button_list[aa].index(hh)
        button_list[aa][bb].config(command=put(aa, bb))
    aa += 1

new_game()

main_window.mainloop()
