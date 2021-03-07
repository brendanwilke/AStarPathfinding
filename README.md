# AStarPathfinding

**Description**

This program contains a 50x50 grid of nodes. Using the GUI, the user can select a start node, an end node, and barriers that are placed on to the grid. Once the user is ready, the algorithm will start and display the shortest possible path from the start node to the end node that does not go through any barriers. 

**Necessary Installations**
* Python 3
* Pygame

**Usage**

1. Use left-click to select the starting node, end node, and barriers in that order. Left-click can be held down and dragged to create multiple barriers at once.
2. Use right-click to remove a currently occupied node. Based on the priority listed above, that may potentially be the next node to be placed. For example, if I place the start node, end node, and barriers, but decide I want to move the start node, I right-click on it, it is moved to the top priority in the code so it will be the next placement on my left-click (higher priority than another barrier), then place it with left-click.
3. Use space to run the algorithm once you have it set up how you would like it. The red squares are nodes that have already been considered, the green nodes are nodes that are currently being considered, and the purple nodes that appear once the algorithm is finished indicate the shortest path found by the algorithm.
4. The c button clears all the nodes on the grid. The next 2 placements will be the start and end nodes based on the priority set at the beginning.
