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

3. Run the code by typing `python main.py` in your terminal.

When the GUI pops up, select an option to generate a maze with loops or a maze without loops. When the maze has generated, select a cell to be the starting point by clicking on it. Select a second cell to be the goal by clicking on it. The cells shoudl highlight when clicked on. Once both the start and goal are selected, select the button corresponding to the algorithm you wish to visualise and the algorithm will start running and solve the maze. The 'Clear' button can be selected to remove the solved maze visualisation and a different algorithm can then be selected.