# CS7IS2 Artificial Intelligence - Assignment 1 

This assignment implementing a number of search and MDP algorithms to solve a maze.

### Assignment Specification: 

1. Implement a maze generator in Python, capable of generating mazes of varying sizes.

2. Implement DFS, BFS and A* for maze solving.

3. Implement MDP value iteration and policy iteration for maze solving.

4. Compare the performances of all 5 algorithms in a range of at least three different maze sizes using at least 2 suitable metrics.
### How to Run:

1. Clone the repository locally with `git clone https://github.com/olearyd3/AI_MazeSearch.git`

2. Install necessary libraries with `pip install -r requirements.txt` 

3. Run the code by typing `python main.py` in your terminal. The GUI will appear.

### Using the GUI to generate different mazes and run the algorithms

In the GUI, there will be a dropdown with different preset maze sizes. Users can select an option from this dropdown and then select either 'Generate Maze w/loops' or 'Generate Maze' to generate a maze with or without more than one possible path from a start cell to a goal respectively. Mazes of custom size can also be generated by entering a number into the text input box below the dropdown menu and hitting the Enter key before selecting one of the two buttons to generate a maze.

Once the maze has generated, click any two cells on the maze. The first will be the start cell (orange) and the second will be the goal (turquoise).

Select one of the five buttons: 'BFS', 'DFS', 'A*', 'MDP Value Iteration' or 'MDP Policy Iteration' to solve the maze using the selected algorithm. The stats of the algorithm will be displayed in the bottom right section of the GUI. 

To run a different algorithm on the same maze with the same start and end goal, simply select 'Clear solution' and then select the new algorithm.
