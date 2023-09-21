# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 9/21/23
# Description: Simple backtracking algorithm to solve a sudoku puzzle.

def solve_sudoku(grid):
    """
    Function that takes in a puzzle and solves it using the helper methods below.
    """

    empty_cell = find_empty_cell(grid)

    if not empty_cell:
        return True

    row, col = empty_cell

    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num

            if solve_sudoku(grid):
                return True

            # backtrack
            grid[row][col] = 0

    # backtrack further
    return False


def find_empty_cell(grid):
    """
    Finds a cell to insert a new value into, returns that cell as a coordinate pair.
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None


def is_valid_move(grid, row, col, num):
    """
    Returns a check for a valid move. If the space is not being used, True is returned.
    """
    return (
            not used_in_row(grid, row, num) and
            not used_in_col(grid, col, num) and
            not used_in_subgrid(grid, row - row % 3, col - col % 3, num)
    )


def used_in_row(grid, row, num):
    return num in grid[row]


def used_in_col(grid, col, num):
    return num in [grid[i][col] for i in range(9)]


def used_in_subgrid(grid, row, col, num):
    for i in range(3):
        for j in range(3):
            if grid[i + row][j + col] == num:
                return True
    return False


# Example usage
if __name__ == "__main__":

    # 0s are empty cells
    example_grid = [
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

    solve_sudoku(example_grid)

    # solved grid
    for row in example_grid:
        print(row)
