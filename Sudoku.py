import os
import sys
import random
import tkinter as tk
from raw_data import *


# region *** Init variables REGION ***

# Fonts and font sizes
f = "Comic Sans MS"
s = "14"


# Init empty list for buttons 9 x 9
button_list = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
# Init empty list for buttons 9 x 9 - duplicated version of 'button_list' with filled values during the game
current_puzzle2 = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
# Init empty list of buttons used to typing numbers from 1 to 9
writing_button_list = [[0]*3, [0]*3, [0]*3]
# Init of global variables containing current number to type
number_to_type = ""

# endregion


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


logo_path = resource_path("icon.ico")


# region *** REGION of functions for buttons command ***
def pull() -> tuple:
    """
    Pull the set of numbers with a not begun sudoku game from 'raw_data' file.
    Function randomly selects 1 puzzle out of 27 available
    :return: tuple with fresh set of numbers
    """
    puzzle = random.choice(raw_sudoku)
    return tuple(puzzle)


def load_puzzel_frame():
    """
    Fill buttons 9 x 9 in 'button_list' with values from 'current puzzle'
    and create a copy of working version of the 'current puzzle'
    :return:
    """
    global current_puzzle2, current_puzzle
    # Creating a working version of the 'current puzzle'
    for row in range(9):
        for column in range(9):
            current_puzzle2[row][column] = current_puzzle[row][column]
    # Set 'normal' stage to all buttons
    for row in button_list:
        for button in row:
            button.config(state=tk.NORMAL)
    # Enter the values into buttons and set 'disabled' stage to buttons which shouldn't be modified during game
    for row in range(9):
        for column in range(9):
            number_from_raw_data = current_puzzle[row][column]
            if number_from_raw_data == 0:
                initial_value = ""
            else:
                initial_value = number_from_raw_data
                button_list[row][column].config(state=tk.DISABLED, fg="Black")
            button_list[row][column].config(text=initial_value)


def new_game():
    """
    Pull new data from 'raw_data' file and reload frame with buttons
    :return:
    """
    global current_puzzle
    current_puzzle = pull()
    load_puzzel_frame()


def clean():
    """
    Function under the 'Clean' button. It reset value of 'number_to_type' to zero and recolor the 'writing buttons'.
    :return:
    """
    global number_to_type
    number_to_type = 0
    for row in writing_button_list:
        for writing_button in row:
            writing_button.config(bg="Silver", fg="Black")
    zero_button.config(bg="Black", fg="White")


def pick(vertical_coordinate: int, horizontal_coordinate: int):
    """
    This function returns the execution of the 'pick2' function on the specified 'writing button' based on coordinates.
    The 'Pick2' function assigns a command to one button in the 'writing button panel'.
    Those two functions (one inside another) give the possibility to assign the function to all buttons in one loop.
    :param vertical_coordinate: row index on writing buttons panel
    :param horizontal_coordinate: column index on writing buttons panel
    :return:
    """
    def pick2():
        global number_to_type
        number_to_type = (vertical_coordinate * 3 + horizontal_coordinate + 1)
        for row_with_buttons in writing_button_list:
            for writing_button in row_with_buttons:
                writing_button.config(bg="Silver", fg="Black")
        zero_button.config(bg="Silver", fg="Black")
        writing_button_list[vertical_coordinate][horizontal_coordinate].config(bg="Black", fg="White")
    return pick2


def warning():
    """
    Function which throw a warning message box.
    :return:
    """
    warning_window = tk.Toplevel()
    warning_window.title("Warning")
    warning_window.iconbitmap(logo_path)
    warning_text = "You cannot enter the selected number\nin this field!"
    war = tk.Label(warning_window, text=warning_text, font=(f, s), padx=10, pady=10)
    war.pack()

    def war_destroy():
        warning_window.destroy()

    war_button = tk.Button(warning_window, text="OK", width=10, font=(f, s), command=war_destroy)
    war_button.pack(padx=10, pady=10)
    warning_window.mainloop()


def finished():
    """
    Function which throw a message box with congratulations. Puzzle solved.
    :return:
    """
    finished_window = tk.Toplevel()
    finished_window.title("Congratulations !")
    finished_window.iconbitmap(logo_path)
    finished_text = "YOU WIN!"
    fin = tk.Label(finished_window, text=finished_text, font=(f, s), padx=10, pady=10)
    fin.pack()

    def fin_destroy():
        finished_window.destroy()
        new_game()

    fin_button = tk.Button(finished_window, text="New game?", width=10, font=(f, s), command=fin_destroy)
    fin_button.pack(padx=10, pady=10)
    finished_window.mainloop()


def check() -> int:
    """
    Function checks possibility to enter a new number into puzzle according to the rules of solving Sudoku.
    :return: 1 if rules were not broken or 0 if one of them was
    """
    for digit in range(1, 10):
        # horizontal check
        for h_row in current_puzzle2:
            horizontal_count = h_row.count(digit)
            if horizontal_count > 1:
                return 0
        # vertical check
        v_column_index = 0
        while v_column_index < 9:
            vertical_list = []
            for v_row in current_puzzle2:
                vertical_list.append(v_row[v_column_index])
            vertical_count = vertical_list.count(digit)
            if vertical_count > 1:
                return 0
            v_column_index += 1
        # square check
        for square_v_index in range(3):
            for square_h_index in range(3):
                square_list = []  # Init list of numbers filled in each square
                s_row = 0
                while s_row < 9:
                    s_col = 0
                    while s_col < 9:
                        if (s_row // 3) == square_v_index and (s_col // 3) == square_h_index:
                            # Here we fill a 'square_list' with already filled digits
                            square_list.append(current_puzzle2[s_row][s_col])
                        s_col += 1
                    s_row += 1
                square_count = square_list.count(digit)
                if square_count > 1:
                    return 0
    return 1


def win() -> int:
    """
    Checks if it's game over (win)
    :return: 1 if all buttons are filled with 1-9 digit or 0 if any button contains zero
    """
    win_list_of_all_filled_values = []
    for win_row in current_puzzle2:
        for win_button in win_row:
            win_list_of_all_filled_values.append(win_button)
    zeroes_count = win_list_of_all_filled_values.count(0)
    if zeroes_count == 0:
        return 1
    else:
        return 0


def put(vertical_coordinate: int, horizontal_coordinate: int):
    """
    This function returns the execution of the 'put2' function on the specified 'puzzle button' based on coordinates.
    The 'Put2' function assigns a command to one button in the 'puzzle button panel'.
    Those two functions (one inside another) give the possibility to assign the function to all buttons in one loop.
    :param vertical_coordinate: row index on puzzle buttons panel
    :param horizontal_coordinate: column index on puzzle buttons panel
    :return:
    """
    def put2():
        global number_to_type
        # Replace value in current_puzzle2
        already_written_value = current_puzzle2[vertical_coordinate][horizontal_coordinate]
        current_puzzle2[vertical_coordinate][horizontal_coordinate] = number_to_type
        # Checks whether entering this value has not broken the rules of the SUDOKU game
        cannot = check()
        if cannot == 1:  # if it's OK
            if number_to_type == 0:  # if user planned to clear the value
                button_list[vertical_coordinate][horizontal_coordinate].config(text="")
            else:
                button_list[vertical_coordinate][horizontal_coordinate].config(text=number_to_type)
        elif cannot == 0:  # if it breaks rules back value to zero and throw warning
            current_puzzle2[vertical_coordinate][horizontal_coordinate] = already_written_value
            warning()
        # After every value entering check if its game over
        winner = win()
        if winner == 1:
            finished()
    return put2


# endregion


# region *** REGION for GUI with Tkinter ***

if __name__ == "__main__":
    # Main App Window
    main_window = tk.Tk()
    main_window.title("SUDOKU")
    main_window.iconbitmap(logo_path)
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
    # Loop for assign function to puzzle buttons ('aa' anb 'bb' are the vertical_coordinate and horizontal_coordinate)
    aa = 0
    while aa < 9:
        for button in button_list[aa]:
            bb = button_list[aa].index(button)
            button_list[aa][bb].config(command=put(aa, bb))
        aa += 1

    # Create buttons for typing and cleaning values
    writing_frame = tk.Frame(main_window)
    writing_frame.pack(side=tk.LEFT, padx=10)
    # Init Tkinter buttons 3 x 3 to pick a number to type. Buttons have no command in this stage.
    for row in range(3):
        for col in range(3):
            writing_button = tk.Button(writing_frame, text=(row*3+col+1), font=(f, s), width=3, command=None,
                                       bg="Silver", fg="Black")
            writing_button.grid(row=row, column=col, padx=1, pady=1)
            writing_button_list[row][col] = writing_button
    # Loop for assign function to writing buttons ('a' anb 'b' are the vertical_coordinate and horizontal_coordinate)
    a = 0
    while a < 3:
        for button in writing_button_list[a]:
            b = writing_button_list[a].index(button)
            writing_button_list[a][b].config(command=pick(vertical_coordinate=a,
                                                          horizontal_coordinate=b))
        a += 1
    # Init 'Zero button'
    zero_button = tk.Button(writing_frame, text="Clean", font=(f, s), command=clean, bg="Silver", fg="Black")
    zero_button.grid(row=3, column=0, columnspan=3, padx=1, pady=1, sticky=tk.NSEW)

    # Create buttons for 'New game' and 'Restart' buttons
    button_new_game = tk.Button(main_window, text="New game", font=(f, s,), width=22, command=new_game)
    button_new_game.pack(anchor=tk.E, padx=10, pady=27)

    button_reset = tk.Button(main_window, text="Restart current game", font=(f, s,), width=22,
                             command=load_puzzel_frame)
    button_reset.pack(anchor=tk.E, padx=10, pady=25)

    new_game()

    main_window.mainloop()

# endregion
