import pygame
from cell import Cell

class Grid:
    """
    grid properties
    """
    def __init__(self, rows, columns, screenWidth, window):
        self.rows = rows
        self.columns = columns 
        self.cellWidth = screenWidth // rows
        self.screenWidth = screenWidth
        self.window = window
        self.grid = []

    def createGrid(self):
        """
        function to create the grid
        """
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.columns):
                cell = Cell(i, j, self.cellWidth, self.rows, self.window)
                cell.resetOpen()
                self.grid[i].append(cell)

    def draw(self):
        #pygame.draw.line(self.window, (150, 150, 150), (self.screenWidth, 0),(self.screenWidth, self.screenWidth))
        pygame.display.update()

    def getCellIndex(self, mousePosition):
        """
        function to return the mouse position on the screen
        """
        x, y = mousePosition
        row = x // self.cellWidth
        col = y // self.cellWidth

        return row, col
    def connect_cells(self, cell1, cell2):
        """
        function for connecting two cells together by marking both as open 
        """
        row1, col1 = cell1.getPos()
        row2, col2 = cell2.getPos()

        if row1 == row2:
            for col in range(min(col1, col2) + 1, max(col1, col2)):
                self.grid[row1][col].setOpen(True)
        elif col1 == col2:
            for row in range(min(row1, row2) + 1, max(row1, row2)):
                self.grid[row][col1].setOpen(True)
