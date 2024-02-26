from grid import Grid
from searchAlgos import AStar, BFS, DFS
from mazeGenerator import iterativeBacktracking, iterativeBacktrackingWithLoops
import pygame
import pygame_gui
from markovDecisionProcesses import valueIteration

pygame.init()

# set up the GUI window
width = 700
window = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("AI Assignment 1")
background = pygame.Surface((1200, 700))
background.fill(pygame.Color(255, 255, 255))
manager = pygame_gui.UIManager((1200, 700))

# set up buttons in the GUI
bfs_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 150), (200, 50)), text='BFS', manager=manager)
dfs_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 250), (200, 50)), text='DFS', manager=manager)
a_star_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 350), (200, 50)), text='A*', manager=manager)
generate_iterative_loops_maze_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 100), (200, 50)), text='Generate Maze with Looping', manager=manager)
generate_maze_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 50), (200, 50)), text='Generate Maze', manager=manager)
value_iteration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 450), (200, 50)), text='MDP Value Iteration', manager=manager)
policy_iteration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 550), (200, 50)), text='MDP Policy Iteration', manager=manager)
clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((950, 650), (200, 50)), text='Clear', manager=manager)

# define the number of rows in the grid
rows = 10
columns = rows

clock = pygame.time.Clock()

# create a grid object to handle the grid state 
gridObj = Grid(rows, columns, width, window)
gridObj.createGrid()

# initialise variables to be used
start = None
goal = None   
run = True
visualiseAlgorithm = True
AnimatePath = True

clock = pygame.time.Clock()
isRunning = True

# set the background to white
#window.blit(background, (0, 0))

reward_free = -1
reward_obstacle = -100
reward_goal = 100
gamma = 0.99  # Discount factor
theta = 0.1  # Convergence threshold

# while the app is active
while isRunning:
    time = clock.tick(60)
    # if user quits then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        # when clicking
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            # convert mouse position to grid coordinates
            row, col = gridObj.getCellIndex(mouse_pos)
            # check if the clicked cell is within the grid boundaries
            if row is not None and col is not None and 0 <= row < rows and 0 <= col < rows:
                # check if start cell is not yet set
                if start is None:
                    start_row, start_col = row, col
                    start = gridObj.grid[start_row][start_col]
                    start.setStart()
                    print("Start cell set to:", start.getPos())
                # check if start cell is already set but goal cell is not yet set
                elif goal is None:
                    goal_row, goal_col = row, col
                    goal = gridObj.grid[goal_row][goal_col]
                    goal.setGoal()
                    print("Goal cell set to:", goal.getPos())
         # if the button is pressed: 
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # BFS
            if event.ui_element == bfs_button:
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    BFS(lambda: gridObj.draw(), start, goal, visualiseAlgorithm, AnimatePath)
                else:
                    print("Please set both start and goal cells within the grid boundaries.")
            # DFS
            if event.ui_element == dfs_button:
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    DFS(lambda: gridObj.draw(), start, goal, visualiseAlgorithm, AnimatePath)
                else:
                    print("Please set both start and goal cells within the grid boundaries.")
            # A*
            elif event.ui_element == a_star_button:
                print("A* button pressed")
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    AStar(lambda: gridObj.draw(), gridObj.grid, start, goal, visualiseAlgorithm, AnimatePath)
                else:
                    print("Please set both start and goal cells within the grid boundaries.")
            # generate maze
            elif event.ui_element == generate_maze_button:
                iterativeBacktracking(lambda: gridObj.draw(), gridObj, True)
                print("Generate maze button pressed")
            elif event.ui_element == generate_iterative_loops_maze_button:
                iterativeBacktrackingWithLoops(lambda: gridObj.draw(), gridObj, True)
                print("Generate maze button pressed")
            # value iteration
            elif event.ui_element == value_iteration_button:
                print("MDP value iteration button pressed")
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    policy = valueIteration(lambda: gridObj.draw(), gridObj, start, goal, visualiseAlgorithm, AnimatePath)
                #print("Optimal Policy:", policy)
            # policy iteration
            elif event.ui_element == policy_iteration_button:
                print("MDP policy iteration button pressed")
            elif event.ui_element == clear_button:
                print("Clear button pressed")
                [cell.resetOpen() for row in gridObj.grid for cell in row if (cell.state == 4 or cell.state == 5
                            or cell.state == 6)]

        manager.process_events(event)

    manager.update(time)
    manager.draw_ui(window)
    pygame.display.update()