from queue import PriorityQueue
import pygame

def h(position1, position2):
    """
    heuristic to estimate the cost from current node to the goal -- return distance between the cells
    """
    x1, y1 = position1 
    x2, y2 = position2 
    return abs(y1 - y2) + abs(x1 - x2)

def redrawPath(prev, current, gridDraw, AnimatePath):
    """
    function to redraw the best path to the goal
    """
    while current in prev:
        current = prev[current]
        current.setPath(AnimatePath)
    gridDraw()

def AStar(gridDraw, grid, start, end, visualiseAlgorithm, AnimatePath):
    """
    function to implement the A* heuristic -- differs from an algo since it uses estimates
    """
    # variable to count order nodes are added to openSet in
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    # dictionary to redraw path when goal found
    cameFrom = {}
    # g is the cost so far to reach the goal
    g = {cell: float("inf") for row in grid for cell in row}
    g[start] = 0
    # f is the total estimated cost of the path from start to the current node
    f = {cell: float("inf") for row in grid for cell in row}
    f[start] = h(start.getPos(), end.getPos())


    existingOpenSet = {start}
    # while there are still open paths to check and goal is not reached
    while not openSet.empty():
        # if user quits while algo is running ensure no crashes occur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        existingOpenSet.remove(current)
        # if the goal has been reached
        if current == end:
            gridDraw()
            # recolour the best path
            redrawPath(cameFrom, current, gridDraw, AnimatePath)
            end.setGoal(visualiseAlgorithm)
            start.setStart(visualiseAlgorithm)
            return True
        # calculate the cost from start to the current node for each of the current node's neighbours
        for neighbour in current.neighbours:
            gNew = g[current] + 1
            # if new g score is better than previous best score, update the scores and add neighbour to openSet
            if gNew < g[neighbour]:
                cameFrom[neighbour] = current
                g[neighbour] = gNew
                f[neighbour] = gNew + h(neighbour.getPos(), end.getPos())
                if neighbour not in existingOpenSet:
                    count += 1 
                    openSet.put((f[neighbour], count, neighbour))
                    existingOpenSet.add(neighbour)
                    neighbour.setEdge(visualiseAlgorithm)

        if current != start:
            current.setClosed(visualiseAlgorithm)
    # if goal cannot be reached -- this should not occur
    return False