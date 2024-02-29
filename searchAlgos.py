from queue import Queue, LifoQueue, PriorityQueue
import pygame
import time

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

def constructPath(cameFrom, start, end):
    """
    helper function to construct the path from the 'cameFrom' dictionary
    """
    path = []
    current = end
    while current != start:
        path.append(current)
        current = cameFrom[current]
    path.append(start)
    return path[::-1] 

def AStar(gridDraw, grid, start, end, visualiseAlgorithm, AnimatePath, visited_cells_label, path_length_label, time_taken_label):
    """
    function to implement the A* heuristic -- differs from an algo since it uses estimates
    """
    # start a timer
    startTime = time.time()
    visitedCells = set()
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
            elapsed_time = time.time() - startTime
            numVisitedCells = len(visitedCells)
            shortestPathLength = g[end] + 1
            elapsedTime = elapsed_time
            print(f"A* Algorithm - Visited Cells: {len(visitedCells)}, Path Length: {g[end] + 1}, Elapsed Time: {elapsed_time} seconds")
            return numVisitedCells, shortestPathLength, elapsedTime
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
                visitedCells.add(neighbour)

        if current != start:
            current.setClosed(visualiseAlgorithm)
    # if goal cannot be reached -- this should not occur
    return 0, 0, 0

def BFS(gridDraw, start, end, visualiseAlgorithm, AnimatePath, visited_cells_label, path_length_label, time_taken_label):
    """
    function to implement Breadth-First Search algorithm
    """
    # queue for BFS
    startTime = time.time()

    queue = Queue()
    queue.put(start)
    # dictionary to redraw path when goal found
    cameFrom = {}
    # set to keep track of visited nodes
    visited = {start}

    while not queue.empty():
        # if user quits while algo is running ensure no crashes occur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()
        # if the goal has been reached
        if current == end:
            gridDraw()
            # recolor the best path
            redrawPath(cameFrom, current, gridDraw, AnimatePath)
            end.setGoal(visualiseAlgorithm)
            start.setStart(visualiseAlgorithm)
            elapsed_time = time.time() - startTime
            # print stats
            print(f"BFS Algorithm - Visited Cells: {len(visited)}, Shortest Path Length: {len(constructPath(cameFrom, start, end)) if current == end else 0}, Elapsed Time: {elapsed_time} seconds")
            visited_cells_label.set_text(f'Visited Cells: {len(visited)}')
            path_length_label.set_text(f'Path Length: {len(constructPath(cameFrom, start, end)) if current == end else 0}')
            time_taken_label.set_text(f'Elapsed Time: {elapsed_time} seconds')
            return len(visited), len(constructPath(cameFrom, start, end)) if current == end else 0, elapsed_time
        # iterate through the neighbors of the current node
        for neighbour in current.neighbours:
            # if the neighbour has not been visited
            if neighbour not in visited:
                # add neighbour to the queue and the visited list
                queue.put(neighbour)
                visited.add(neighbour)
                # mark the neighbour as the current cell and visualise it
                cameFrom[neighbour] = current
                neighbour.setEdge(visualiseAlgorithm)

        if current != start:
            current.setClosed(visualiseAlgorithm)

    # if the goal cannot be reached -- this should not occur
    return 0, 0, 0

def DFS(gridDraw, start, end, visualiseAlgorithm, AnimatePath, visited_cells_label, path_length_label, time_taken_label):
    """
    function to implement Depth-First Search algorithm
    """
    # stack for DFS
    startTime = time.time()
    print("start:", f"({start.x}, {start.y}), Goal: ({end.x}, {end.y})")
    stack = LifoQueue()
    stack.put(start)
    # dictionary to redraw path when goal found
    cameFrom = {}
    # set to keep track of visited nodes
    visited = {start}

    while not stack.empty():
        # if user quits while algo is running ensure no crashes occur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.get()
        # if the goal has been reached
        if current == end:
            gridDraw()
            # recolor the best path
            redrawPath(cameFrom, current, gridDraw, AnimatePath)
            end.setGoal(visualiseAlgorithm)
            start.setStart(visualiseAlgorithm)
            elapsed_time = time.time() - startTime
            # print stats
            print(f"DFS Algorithm - Visited Cells: {len(visited)}, Shortest Path Length: {len(constructPath(cameFrom, start, end)) if current == end else 0}, Elapsed Time: {elapsed_time} seconds")
            visited_cells_label.set_text(f'Visited Cells: {len(visited)}')
            path_length_label.set_text(f'Path Length: {len(constructPath(cameFrom, start, end)) if current == end else 0}')
            time_taken_label.set_text(f'Elapsed Time: {elapsed_time} seconds')              
            return len(visited), len(constructPath(cameFrom, start, end)) if current == end else 0, elapsed_time
        # iterate through the neighbors of the current node
        for neighbour in current.neighbours:
            # if the neighbour has not been visited
            if neighbour not in visited:
                # add neighbour to the stack and the visited list
                stack.put(neighbour)
                visited.add(neighbour)
                # mark the neighbour as the current cell and visualize it
                cameFrom[neighbour] = current
                neighbour.setEdge(visualiseAlgorithm)

        if current != start:
            current.setClosed(visualiseAlgorithm)

    # if the goal cannot be reached -- this should not occur
    return 0, 0, 0