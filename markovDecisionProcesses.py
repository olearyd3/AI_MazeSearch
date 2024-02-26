import pygame

def redrawOptimalPath(grid, policy, start, goal, gridDraw, AnimatePath):
    """
    function to redraw the optimal path based on the policy 
    """
    current = start
    while policy[current] is not None:
        print(current.getPos())
        action = policy[current]
        next_cell = transition_model(grid, current, action)
        current.setPath(AnimatePath)
        current = next_cell
    gridDraw()
    # recolour start
    start.setStart(True)

# define the transition model and reward function
def transition_model(grid, cell, action):
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

def valueIteration(gridDraw, grid, start, goal, visualiseAlgorithm, AnimatePath):
    """
    function to implement the MDP value iteration
    """
    # initialise reward values
    reward_goal = 100
    reward_obstacle = -5
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

    # convergence value and gamma
    convergence_threshold = 0.01
    gamma = 0.99

    while True:
        delta = 0
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
                    
                    print(f"Cell {cell.getPos()}: Up={values[transition_model(grid, cell, 'up')]:.5f}, "
                          f"Down={values[transition_model(grid, cell, 'down')]:.5f}, "
                          f"Left={values[transition_model(grid, cell, 'left')]:.5f}, "
                          f"Right={values[transition_model(grid, cell, 'right')]:.5f}")

        if delta < convergence_threshold:
            break
    
    # printing the optimal policy
    print("Optimal Policy:")
    for row in grid.grid:
        for cell in row:
            if not cell.isWall():
                print(f"Cell {cell.getPos()}: {policy[cell]}")

    # visualise the optimal path on the maze
    redrawOptimalPath(grid, policy, start, goal, gridDraw, AnimatePath)

    return policy
