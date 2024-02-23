from random import choice
from queue import LifoQueue
import pygame

def isNeighbour(grid, current, distance): 
    """
    appends neighbouring cells to the neighbours list
    """
    # clear the neighbours list
    current.clearNeighbours()
    row, column = current.getPos()
    # above
    if row - distance > 0 and grid.grid[row - distance][column].isWall():
        current.neighbours.append(grid.grid[row - distance][column])

    # below
    if row + distance < grid.rows and grid.grid[row + distance][column].isWall():
        current.neighbours.append(grid.grid[row + distance][column])

    # left
    if column - distance > 0 and grid.grid[row][column - distance].isWall():
        current.neighbours.append(grid.grid[row][column - distance])

    # right
    if column + distance < grid.rows and grid.grid[row][column + distance].isWall():
        current.neighbours.append(grid.grid[row][column + distance])
    

def iterativeBacktracking(gridDraw, grid, visualise):
    """ 
    choose the initial cell, mark it as visited and push it to the stack
    while the stack is not empty
    pop a cell from the stack and make it a current cell
    if the current cell has any neighbours which have not been visited
    push the current cell to the stack
    choose one of the unvisited neighbours
    remove the wall between the current cell and the chosen cell
    mark the chosen cell as visited and push it to the stack 
    """

    Q = LifoQueue()

    [cell.resetWall() for row in grid.grid for cell in row]
    gridDraw()
    i = choice(range(2, grid.rows - 2))
    j = choice(range(2, grid.rows - 2))
    current = grid.grid[i][j]
    current.setOpen(visualise)
    Q.put(current)

    while not Q.empty():
        current = Q.get()
        isNeighbour(grid, current, 2)
        if current.neighbours:
            neighbour = choice(current.neighbours)
            current.neighbours.remove(neighbour)
            Q.put(current)
            neighbour.setOpen(visualise)
            
            # get current row, column and neighbouring rows and columns
            currentRow, currentColumn = current.getPos()
            neighbouringRow, neighbouringColumn = neighbour.getPos()
            # get the distance to the neighbours
            rowDistance = currentRow - neighbouringRow
            columnDistance = currentColumn - neighbouringColumn
            # above
            if rowDistance == -2: 
                grid.grid[neighbouringRow - 1][neighbouringColumn].setOpen(visualise)
            # below
            elif rowDistance == + 2:
                grid.grid[neighbouringRow + 1][neighbouringColumn].setOpen(visualise)
            #left
            elif columnDistance == -2:
                grid.grid[neighbouringRow][neighbouringColumn - 1].setOpen(visualise)
            #right
            elif columnDistance == 2: 
                grid.grid[neighbouringRow][neighbouringColumn + 1].setOpen(visualise)
            Q.put(neighbour)
    return

