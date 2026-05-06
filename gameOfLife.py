from tkinter import *
from tkinter import ttk
import threading

"""This project is hosted on 
https://github.com/manueldun/GameOfLife"""


# Functions
def draw_cells(world, canvas):
    canvas.create_line(1, 1, 1, GRID_SIZE_X * CELL_SIZE)
    canvas.create_line(1, 1, GRID_SIZE_Y * CELL_SIZE, 1)
    for col in range(GRID_SIZE_Y):
        for row in range(GRID_SIZE_X):
            if world[col][row]:
                canvas.create_rectangle(
                    col * GRID_SIZE_X + 1,
                    row * GRID_SIZE_Y + 1,
                    (col + 1) * GRID_SIZE_X + 1,
                    (row + 1) * GRID_SIZE_Y + 1,
                    fill="yellow",
                    outline="black",
                )
            else:
                canvas.create_rectangle(
                    col * GRID_SIZE_X + 1,
                    row * GRID_SIZE_Y + 1,
                    (col + 1) * GRID_SIZE_X + 1,
                    (row + 1) * GRID_SIZE_Y + 1,
                    fill="grey",
                    outline="black",
                )


def spawn_cell(event):
    col = event.x // GRID_SIZE_X
    row = event.y // GRID_SIZE_Y
    world[col][row] = True
    draw_cells(world, canvas)


def kill_cell(event):
    col = event.x // GRID_SIZE_X
    row = event.y // GRID_SIZE_Y
    world[col][row] = False
    draw_cells(world, canvas)


"""This is the main iteration of Conway's Game of Life"""


def iterate(world, canvas):
    newIteration = []
    for row in range(GRID_SIZE_X):
        row = []
        for col in range(GRID_SIZE_Y):
            row.append(False)
        newIteration.append(row)
    # Main demonstration of iteration
    for row in range(GRID_SIZE_X):

        for col in range(GRID_SIZE_Y):
            neighbors = 0
            if row + 1 < GRID_SIZE_Y and world[row + 1][col]:
                neighbors = neighbors + 1
            if (
                row + 1 < GRID_SIZE_Y
                and col + 1 < GRID_SIZE_X
                and world[row + 1][col + 1]
            ):
                neighbors = neighbors + 1
            if col + 1 < GRID_SIZE_X and world[row][col + 1]:
                neighbors = neighbors + 1
            if col + 1 < GRID_SIZE_X and row - 1 >= 0 and world[row - 1][col + 1]:
                neighbors = neighbors + 1
            if row - 1 >= 0 and world[row - 1][col]:
                neighbors = neighbors + 1
            if row - 1 >= 0 and col - 1 >= 0 and world[row - 1][col - 1]:
                neighbors = neighbors + 1
            if col - 1 >= 0 and world[row][col - 1]:
                neighbors = neighbors + 1
            if col - 1 >= 0 and row + 1 < GRID_SIZE_X and world[row + 1][col - 1]:
                neighbors = neighbors + 1

            if not world[row][col] and neighbors == 3:
                newIteration[row][col] = True
            if world[row][col] and neighbors > 3 or neighbors == 1:
                newIteration[row][col] = False
            if world[row][col] and neighbors == 2 or neighbors == 3:
                newIteration[row][col] = True
    return newIteration


if __name__ == "__main__":
    CELL_SIZE = 15
    GRID_SIZE_X = 20
    GRID_SIZE_Y = 20
    NUMBER_OF_CELLS = 30
    # setting world
    world = []
    for col in range(GRID_SIZE_Y):
        row_world = []
        for row in range(GRID_SIZE_X):
            row_world.append(False)
        world.append(row_world)
    # Setting UI
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    canvas = Canvas(
        frm, width=GRID_SIZE_X * CELL_SIZE + 1, height=GRID_SIZE_Y * CELL_SIZE + 1
    )
    canvas.grid(column=0, row=0)

    button_frame = ttk.Frame(frm, padding=10)
    label = ttk.Label(
        text="Controls: left click to spawn cells, right click to kill cells."
    )
    iterate_button = ttk.Button(button_frame, text="Iterate")
    run_button = ttk.Button(button_frame, text="Run")
    stop_button = ttk.Button(button_frame, text="Stop")
    stop_button.configure(state="disabled")

    def iterate_callback():
        global world
        world = iterate(world, canvas)
        draw_cells(world, canvas)

    is_iterating = False

    def run():
        global is_iterating
        if is_iterating:
            iterate_callback()
            root.after(500, run)

    def run_callback():
        global is_iterating
        global run_button
        global stop_button
        global iterate_button
        run_button.configure(state="disabled")
        stop_button.configure(state="enabled")
        iterate_button.configure(state="disabled")
        is_iterating = True
        run()

    def stop_callback():
        global is_iterating
        global run_button
        global stop_button
        run_button.configure(state="enabled")
        stop_button.configure(state="disabled")
        iterate_button.configure(state="enabled")
        is_iterating = False

    def close_callback(event):
        global is_iterating
        is_iterating = False

    button_frame.grid(column=0, row=1)
    label.grid(column=0, row=2)
    iterate_button.grid(column=0, row=0)
    run_button.grid(column=1, row=0)
    stop_button.grid(column=2, row=0)

    run_button.configure(command=run_callback)
    iterate_button.configure(command=iterate_callback)
    stop_button.configure(command=stop_callback)
    root.bind("<Destroy>", close_callback)

    # events
    canvas.bind("<Button-1>", spawn_cell)
    canvas.bind("<Button-3>", kill_cell)
    canvas.bind("<B1-Motion>", spawn_cell)
    canvas.bind("<B3-Motion>", kill_cell)

    # drawing world
    draw_cells(world, canvas)
    # run
    root.mainloop()
