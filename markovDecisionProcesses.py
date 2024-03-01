import pygame
import time

def redrawOptimalPath(grid, policy, start, goal, gridDraw, AnimatePath):
    """
    function to redraw the optimal path based on the policy 
    """
    current = start
    pathLength = 0
    while policy[current] is not None:
        print(current.getPos())
        action = policy[current]
        next_cell = transition_model(grid, current, action)
        current.setPath(AnimatePath)
        current = next_cell
        pathLength += 1
    gridDraw()
    # recolour start
    start.setStart(True)
    return pathLength + 1

def transition_model(grid, cell, action):
    """
    function for the transition model to determine moves based on the actions
    """
    # get the current cell position
    col, row = cell.getPos()
    # move based on the action
    if action == "up":
        row -= 1
    elif action == "down":
        row += 1
    elif action == "left":
        col -= 1
    elif action == "right":
        col += 1
    # if the new cell being moved to is valid then return it
    if 0 <= row < grid.rows and 0 <= col < grid.columns:
        return grid.grid[col][row]
    else:
        # otherwise stay put
        return cell

def valueIteration(gridDraw, grid, start, goal, AnimatePath):
    """
    function to implement the MDP value iteration
    """
    # initialise reward values
    startTime = time.time()
    reward_goal = 100000
    reward_obstacle = -100
    reward_free = 0.1
    # set all values to 0 initially and have no policy for any cell
    values = {cell: 0 for row in grid.grid for cell in row}
    policy = {cell: None for row in grid.grid for cell in row}

    # set the goal value to the reward_goal
    values[goal] = reward_goal

    def reward_function(cell, next_cell):
        # if the cell is the goal return reward for reaching goal
        if cell == goal:
            return reward_goal
            # if the cell is a wall, change cell position to previous cell and return the reward for an obstacle
        elif next_cell.isWall():
            return reward_obstacle
            # otherwise return it is an open cell
        else:
            return reward_free

    # convergence value and discount factor
    convergence_threshold = 0.01
    gamma = 0.99
    counter = 0
    while True:
        delta = 0
        counter = counter + 1
        # for each cell 
        for row in grid.grid:
            for cell in row:
                # if not a wall or the goal
                if cell != goal and not cell.isWall():
                    v = values[cell]
                    max_value = float("-inf")
                    best_action = None
                    # for each possible action from a cell
                    for action in ["up", "down", "left", "right"]:
                        
                        next_cell = transition_model(grid, cell, action)
                        # calculate reward for that action
                        r = reward_function(cell, next_cell)
                        # get the value to be summed as per bellman equation -- assume all transition probs are equal here
                        # alternative: set transition prob for wall to 0 and everything else to 1/ (number of open cell neighbours) 
                        # this can be multiplied by value
                        value = r + gamma * values[next_cell]
                        # update best action to the max 
                        if value > max_value:
                            max_value = value
                            best_action = action
                    # update the values and policy for the cell 
                    temp_cell = cell
                    values[temp_cell] = max_value
                    policy[temp_cell] = best_action
                    # calculate new delta to see if convergence has been reached
                    delta = max(delta, abs(v - max_value))
                    
                    # print(f"Cell {cell.getPos()}: Up={values[transition_model(grid, cell, 'up')]:.5f}, "
                    #       f"Down={values[transition_model(grid, cell, 'down')]:.5f}, "
                    #       f"Left={values[transition_model(grid, cell, 'left')]:.5f}, "
                    #       f"Right={values[transition_model(grid, cell, 'right')]:.5f}")

        if delta < convergence_threshold:
            break
    elapsed_time = time.time() - startTime
    print("Elapsed Time:", elapsed_time, "seconds")
    # printing the optimal policy
    print("counter", counter)
    # print("Optimal Policy:")
    # for row in grid.grid:
    #     for cell in row:
    #         if not cell.isWall():
    #             print(f"Cell {cell.getPos()}: {policy[cell]}")

    # visualise the optimal path on the maze
    pathLength = redrawOptimalPath(grid, policy, start, goal, gridDraw, AnimatePath)

    return policy, pathLength, counter, elapsed_time

def policyIteration(gridDraw, grid, start, goal, AnimatePath):
    # initialize reward values
    reward_goal = 100000
    reward_obstacle = -100
    reward_free = 0.1
    startTime = time.time()
    # set all inital policies to empty
    policy = {cell: None for row in grid.grid for cell in row}

    def reward_function(cell, next_cell):
        if cell == goal:
            return reward_goal
        elif next_cell.isWall():
            return reward_obstacle
        else:
            return reward_free

    # convergence value and discount factor
    convergence_threshold = 0.01
    gamma = 0.99
    values = {cell: 0 for row in grid.grid for cell in row}
    values[goal] = reward_goal
    counter = 0
    while True:
        counter = counter + 1
        # policy evaluation
        policy_delta = 0
        while True:
            delta = 0
            for row in grid.grid:
                for cell in row:
                    if cell != goal and not cell.isWall():
                        v = values[cell]
                        action = policy[cell]
                        next_cell = transition_model(grid, cell, action)
                        r = reward_function(cell, next_cell)
                        values[cell] = r + gamma * values[next_cell]
                        delta = max(delta, abs(v - values[cell]))

            # print("Values:")
            # for row in grid.grid:
            #     for cell in row:
            #         if not cell.isWall():
            #             print(f"Cell {cell.getPos()}: {values[cell]}")
            # print(f"Delta: {delta}")

            if delta < convergence_threshold:
                break

        # policy improvement
        policy_stable = True
        policy_delta = 0
        for row in grid.grid:
            #print('row', row)
            for cell in row:
                if cell != goal and not cell.isWall():
                    old_action = policy[cell]
                    max_value = float("-inf")
                    best_action = None
                    for action in ["up", "down", "left", "right"]:
                        next_cell = transition_model(grid, cell, action)
                        r = reward_function(cell, next_cell)
                        value = r + gamma * values[next_cell]
                        # print("action, cell, value", action, cell.getPos(), value)
                        if value > max_value:
                            max_value = value
                            best_action = action

                    # update the values and policy for the cell 
                    temp_cell = cell
                    values[temp_cell] = max_value
                    policy[temp_cell] = best_action
                    # calculate new delta to see if convergence has been reached
                    #delta = max(delta, abs(v - max_value))
                    
                    # print(f"Cell {cell.getPos()}: Up={values[transition_model(grid, cell, 'up')]:.5f}, "
                    #       f"Down={values[transition_model(grid, cell, 'down')]:.5f}, "
                    #       f"Left={values[transition_model(grid, cell, 'left')]:.5f}, "
                    #       f"Right={values[transition_model(grid, cell, 'right')]:.5f}")
                          
                    if old_action != best_action:
                        policy_stable = False

                        # print(f"Policy change at {cell.getPos()}: {old_action} -> {best_action}")

                        # Update policy_delta based on policy change
                        policy_delta = max(policy_delta, abs(max_value - values[temp_cell]))    
                    # print('policy delta', policy_delta)           
        # print(f"Policy delta: {policy_delta}")
        
        if policy_stable:
            print('broke')
            break
    elapsed_time = time.time() - startTime
    print("Elapsed Time:", elapsed_time, "seconds")
    print('Iterations', counter)
    # printing the optimal policy
    # print("Optimal Policy:")
    # for row in grid.grid:
    #     for cell in row:
    #         if not cell.isWall():
    #             print(f"Cell {cell.getPos()}: {policy[cell]}")

    # visualise the optimal path on the maze
    pathLength = redrawOptimalPath(grid, policy, start, goal, gridDraw, AnimatePath)

    return policy, pathLength, counter, elapsed_time