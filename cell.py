import pygame

class Cell:
    """Defines the cell which would make up the grid"""
    def __init__(self, row, col, width, totalRows, window):
        self.row = row 
        self.col = col
        self.x = row * width
        self.y = col * width
        self.state = 0
        self.color = (255, 255, 255)
        self.neighbours = []
        self.width = width
        self.totalRows = totalRows
        self.window = window
    
    def getPos(self):
        return self.row, self.col
    
    def isOpen(self):
        return self.state == 0

    def isWall(self):
        return self.state == 1

    def resetOpen(self):
        self.state = 0
        self.color = (255, 255, 255)
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.width))

    def resetWall(self):
        self.state = 1
        self.color = (0, 0, 0)
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.width))

    def setOpen(self, vis=True):
        self.state = 0
        self.color = (255, 255, 255)
        self.draw(vis)

    def setWall(self, vis=True):
        self.state = 1
        self.color = (0, 0, 0)
        self.draw(vis)

    def setStart(self, vis=True):
        self.state = 2
        self.color = (255, 165 ,0)
        self.draw(vis)

    def setGoal(self, vis=True):
        self.state = 3
        self.color = (64, 224, 208)
        self.draw(vis)
    
    def setClosed(self, vis=True):
        self.state = 4
        self.color = (148, 184, 242)
        self.draw(vis)

    def setEdge(self, vis=True):
        self.state = 5
        self.color = (219, 149, 162)
        self.draw(vis)
    
    def setPath(self, pathVis=True):
        self.state = 6
        self.color = (83, 128, 100)
        self.draw(pathVis)

    # function to draw a rectangle
    def draw(self, vis):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.width))
        if vis:
            pygame.display.update((self.x, self.y, self.width, self.width))
    
    def updateNeighbours(self, grid):
        """
        function to update the neighbours of the current slot
        check if a neighbour is not a wall and if not, append it to neighbours list in correct order
        """
        self.neighbours.clear()
        self.neighbours = []
        # above
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():
            self.neighbours.append(grid[self.row - 1][self.col])
        # below
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall():
            self.neighbours.append(grid[self.row + 1][self.col])
        # left 
        if self.col > 0 and not grid[self.row][self.col - 1].isWall():
            self.neighbours.append(grid[self.row][self.col - 1])
        # right
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall():
            self.neighbours.append(grid[self.row][self.col + 1])

    # clear the neighbouts list
    def clearNeighbours(self):
        self.neighbours.clear()

  