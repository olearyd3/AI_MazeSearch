from grid import Grid
from searchAlgos import AStar, BFS, DFS
from mazeGenerator import backtracker, backtrackerWithLoops
import pygame
import pygame_gui
from markovDecisionProcesses import valueIteration, policyIteration

pygame.init()

# set up the GUI window
width = 1000
window = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption("AI Assignment 1")
background = pygame.Surface((1500, 1000))
background.fill(pygame.Color(255, 255, 255))
manager = pygame_gui.UIManager((1500, 1000))

# set up buttons in the GUI
bfs_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1025, 350), (200, 50)), text='BFS', manager=manager)
dfs_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1275, 350), (200, 50)), text='DFS', manager=manager)
a_star_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1150, 425), (200, 50)), text='A*', manager=manager)
generate_iterative_loops_maze_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1025, 275), (200, 50)), text='Generate Maze w/Loops', manager=manager)
generate_maze_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1275, 275), (200, 50)), text='Generate Maze', manager=manager)
value_iteration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1025, 500), (200, 50)), text='MDP Value Iteration', manager=manager)
policy_iteration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1275, 500), (200, 50)), text='MDP Policy Iteration', manager=manager)
clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1150, 575), (200, 50)), text='Clear Solution', manager=manager)

# label_rect = pygame.Rect((50, 50), (1500, 50))
# label = pygame_gui.elements.UILabel(relative_rect=label_rect, text='Artificial Intelligence - Assignment 1!', manager=manager)
numVisitedCells = 0
shortestPathLength = 0
elapsedTime = 0

maze_size_options = ["10x10", "20x20", "50x50", "100x100", "200x200"]
maze_size_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=maze_size_options,
    starting_option=maze_size_options[1],  # Default option
    relative_rect=pygame.Rect((1150, 50), (200, 50)),
    manager=manager
)

visited_cells_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((1050, 700), (300, 50)),
    text=f'Number of cells visited: {numVisitedCells}',
    manager=manager
)

path_length_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((1050, 725), (300, 50)),
    text=f'Length of Path: {shortestPathLength}',
    manager=manager
)

time_taken_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((1050, 750), (300, 50)),
    text=f'Elapsed time (secs): {elapsedTime}',
    manager=manager
)

dropdown_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((1000, 50), (200, 50)),
    text='Maze size: ',
    manager=manager
)

num_rows_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((1025, 200), (350, 50)),
    text='Custom number of rows and columns to use:',
    manager=manager
)

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1375, 205), (50, 35)), manager=manager)

# define the number of rows in the grid
rows = 20
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

title_font = pygame.font.Font(None, 36)  # You can customize the font and size here
title_text = title_font.render('Maze Generator', True, (150, 150, 150))

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
        # Check for user input in the text entry for rows
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == text_input:
                    entered_text = event.text
                    try:
                        rows = int(entered_text)
                    except ValueError:
                        print("Entered text is not an integer.")
                    else:
                        rows = int(entered_text)
                        columns = rows
                        start = None
                        goal = None
                        [cell.resetOpen() for row in gridObj.grid for cell in row if (cell.state == 4 or cell.state == 5
                                    or cell.state == 6)]
                        gridObj = Grid(rows, columns, width, window)
                        gridObj.createGrid()
                        print(f"Entered text is an integer: {rows}")
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            selected_option = event.text
            # Set rows based on the selected maze size
            if selected_option == "10x10":
                rows = 10
            elif selected_option == "20x20":
                rows = 20
            elif selected_option == "50x50":
                rows = 50
            elif selected_option == "100x100":
                rows = 100
            elif selected_option == "200x200":
                rows = 200
            columns = rows

            start = None
            goal = None

            [cell.resetOpen() for row in gridObj.grid for cell in row if (cell.state == 4 or cell.state == 5
                        or cell.state == 6)]

            gridObj = Grid(rows, columns, width, window)
            gridObj.createGrid()
         # if the button is pressed: 
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # BFS
            if event.ui_element == bfs_button:
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    numVisitedCells, shortestPathLength, elapsedTime = BFS(lambda: gridObj.draw(), start, goal, visualiseAlgorithm, AnimatePath)
                    text_area_rect = pygame.Rect(1050, 700, 300, 150)
                    pygame.draw.rect(window, (0, 0, 0), text_area_rect)
                    visited_cells_label.set_text(f'Number of visited cells: {numVisitedCells}')
                    path_length_label.set_text(f'Length of Path: {shortestPathLength}')
                    time_taken_label.set_text(f'Elapsed time: {elapsedTime} secs')
                else:
                    print("Please set both start and goal cells within the grid boundaries.")
            # DFS
            if event.ui_element == dfs_button:
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    numVisitedCells, shortestPathLength, elapsedTime = DFS(lambda: gridObj.draw(), start, goal, visualiseAlgorithm, AnimatePath)
                    text_area_rect = pygame.Rect(1050, 700, 300, 150)
                    pygame.draw.rect(window, (0, 0, 0), text_area_rect)
                    visited_cells_label.set_text(f'Number of visited cells: {numVisitedCells}')
                    path_length_label.set_text(f'Length of Path: {shortestPathLength}')
                    time_taken_label.set_text(f'Elapsed time: {elapsedTime} secs')
                else:
                    print("Please set both start and goal cells within the grid boundaries.")
            # A*
            elif event.ui_element == a_star_button:
                print("A* button pressed")
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    numVisitedCells, shortestPathLength, elapsedTime = AStar(lambda: gridObj.draw(), gridObj.grid, start, goal, visualiseAlgorithm, AnimatePath)
                    text_area_rect = pygame.Rect(1050, 700, 300, 150)
                    pygame.draw.rect(window, (0, 0, 0), text_area_rect)
                    visited_cells_label.set_text(f'Number of visited cells: {numVisitedCells}')
                    path_length_label.set_text(f'Length of Path: {shortestPathLength}')
                    time_taken_label.set_text(f'Elapsed time: {elapsedTime} secs')
                else:
                    print("Please set both start and goal cells within the grid boundaries.")
            # generate maze
            elif event.ui_element == generate_maze_button:
                start = None
                goal = None

                [cell.resetOpen() for row in gridObj.grid for cell in row if (cell.state == 4 or cell.state == 5
                            or cell.state == 6)]

                gridObj = Grid(rows, columns, width, window)
                gridObj.createGrid()
                backtracker(lambda: gridObj.draw(), gridObj, True)
                print("Generate maze button pressed")
            elif event.ui_element == generate_iterative_loops_maze_button:
                start = None
                goal = None

                [cell.resetOpen() for row in gridObj.grid for cell in row if (cell.state == 4 or cell.state == 5
                            or cell.state == 6)]

                gridObj = Grid(rows, columns, width, window)
                gridObj.createGrid()
                backtrackerWithLoops(lambda: gridObj.draw(), gridObj, True)
                print("Generate maze with loops button pressed")
            # value iteration
            elif event.ui_element == value_iteration_button:
                print("MDP value iteration button pressed")
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    policy, pathLength, numIterations, elapsedTime = valueIteration(lambda: gridObj.draw(), gridObj, start, goal, AnimatePath)
                    text_area_rect = pygame.Rect(1050, 700, 300, 150)
                    pygame.draw.rect(window, (0, 0, 0), text_area_rect)
                    visited_cells_label.set_text(f'Number of iterations: {numIterations}')
                    path_length_label.set_text(f'Length of Path: {pathLength}')
                    time_taken_label.set_text(f'Elapsed time: {elapsedTime} secs')
            # policy iteration
            elif event.ui_element == policy_iteration_button:
                print("MDP policy iteration button pressed")
                if start is not None and goal is not None and 0 <= start_row < rows and 0 <= start_col < rows and 0 <= goal_row < rows and 0 <= goal_col < rows:
                    [cell.updateNeighbours(gridObj.grid) for row in gridObj.grid for cell in row]
                    policy, pathLength, numIterations, elapsedTime = policyIteration(lambda: gridObj.draw(), gridObj, start, goal, AnimatePath)
                    text_area_rect = pygame.Rect(1050, 700, 300, 150)
                    pygame.draw.rect(window, (0, 0, 0), text_area_rect)
                    visited_cells_label.set_text(f'Number of iterations: {numIterations}')
                    path_length_label.set_text(f'Length of Path: {pathLength}')
                    time_taken_label.set_text(f'Elapsed time: {elapsedTime} secs')
            elif event.ui_element == clear_button:
                numVisitedCells = 0
                shortestPathLength = 0
                elapsedTime = 0
                print("Clear button pressed")
                [cell.resetOpen() for row in gridObj.grid for cell in row if (cell.state == 4 or cell.state == 5
                            or cell.state == 6)]
        window.blit(title_text, (1150, 10))
        manager.process_events(event)

    manager.update(time)
    manager.draw_ui(window)
    pygame.display.update()