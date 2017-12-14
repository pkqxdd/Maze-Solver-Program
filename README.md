# How to run the program

1. clone this repository
2. `cd` into it
3. run `python3.6 .` or `python3.6 __main__.py`

# Introduction

This program is made for the [final project](https://pkqxdd.github.io/Maze-Solver/) of my [robotics class](https://pkqxdd.github.io/Advanced-Robotics-Journal/). It is not yet finished. The program does not use any third-party library. 

The program uses A* algorithm to find the shortest route between any two connected nodes. Everything can function correctly without GUI, except for the part about generating a maze.

The maze is in term of paths. That is, if you generate a maze in the program, you are supposed to follow the lines, not the empty spaces in between.

# Known issues

1. When generating a maze, if the density of the path is low, sometimes the nodes are not constructed even the paths appear to be crossing each other.
2. When generating a maze, if you press the button "Generate" more than once, the program may freeze. In that case, please kill and rerun the program.