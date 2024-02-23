import pygame
from cell import Cell

class Grid:
    def __init__(self,rows, screenWidth, window):
        self.rows = rows
        self.cellWidth = screenWidth // rows
        self.screenWidth = screenWidth
        self.window = window
        self.grid = []

    def createGrid(self):
        """Create the grid of size rows"""
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                cell = Cell(i, j, self.cellWidth, self.rows, self.window)
                cell.resetOpen()
                self.grid[i].append(cell)

    def draw(self):

        pygame.draw.line(self.window, (150, 150, 150), (self.screenWidth, 0),(self.screenWidth, self.screenWidth))
        pygame.display.update()

    def getCellIndex(self, mousePosition):
        """
        function to return the mouse position on the screen
        """
        x, y = mousePosition
        row = x // self.cellWidth
        col = y // self.cellWidth

        return row, col
