from tkinter import *
from tkinter import ttk


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
    # Main demonstration of iteration
    for row in range(GRID_SIZE_X):
        row = []
        for col in range(GRID_SIZE_Y):
            row.append(False)
        newIteration.append(row)
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

    def iterate_command():
        global world
        world = iterate(world, canvas)
        draw_cells(world, canvas)

    iterate_button = ttk.Button(frm, text="Iterate", command=iterate_command)
    iterate_button.grid(column=0, row=1)

    # events
    canvas.bind("<Button-1>", spawn_cell)
    canvas.bind("<Button-3>", kill_cell)
    canvas.bind("<B1-Motion>", spawn_cell)
    canvas.bind("<B3-Motion>", kill_cell)

    # drawing world
    draw_cells(world, canvas)
    # run
    root.mainloop()
