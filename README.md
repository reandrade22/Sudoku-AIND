# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation consists in reducing the search space for possible solutions. When tow boxes in the Sudoku puzzle consists of the same two numbers, it means that for the peers that these two boxes share, both numbers are not a possible solution. Thus, they can be eliminated from said peers, reducing the search space for them. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propagation consists in reducing the search space for possible solutions. When the diagonal is included, boxes located on either diagonal have an added contraint, reducing the search space.

### Install

This project requires **Python 3**.

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

