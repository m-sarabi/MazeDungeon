import random


# Generate an ascii maze with the given width and height
# The algorithms use is:
# Randomized depth-first search, Iterative implementation (with stack)
# Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_implementation_(with_stack)
def generate_maze(height: int, width: int) -> list[str]:
    """Generate an ascii maze with the given width and height.\n
    The actual width and height of the maze is (height * 2 + 1, width * 3 + 1)
    :param height: Number rows of cells
    :param width: Number of columns of cells
    :return: A list of strings that each item of the list is a row of the maze to be printed
    """
    size = [height, width]  # Defining the size of the maze

    # Initialize the maze with walls and clearing the cells
    maze = ["|--" * size[1] + "|"] * (size[0] * 2 + 1)
    for i in range(size[0]):
        maze[i * 2 + 1] = maze[i * 2 + 1].replace("--", "  ")

    # Initialize a matrix to keep track of the unvisited cells
    maze_matrix = [[0 for _ in range(size[1])] for _ in range(size[0])]

    # Function to remove the wall between two adjacent wall
    def clear_wall(c1, c2):
        # Determining the location of the wall based on the position of the cells
        if c1[1] == c2[1] and c2[0] < c1[0]:
            d = "up"
        elif c1[1] == c2[1] and c2[0] > c1[0]:
            d = "down"
        elif c1[0] == c2[0] and c2[1] < c1[1]:
            d = "left"
        elif c1[0] == c2[0] and c2[1] > c1[1]:
            d = "right"
        else:
            raise ValueError(f"c2 is wrong: {c1}, {c2}")

        # Convert the matrix coords of the first cell to maze coords
        r = c1[0] * 2 + 1
        c = c1[1] * 3 + 1

        # Remove the wall in the determined location
        match d:
            case "up":
                maze[r - 1] = maze[r - 1][:c] + "  " + maze[r - 1][c + 2:]
            case "down":
                maze[r + 1] = maze[r + 1][:c] + "  " + maze[r + 1][c + 2:]
            case "left":
                maze[r] = maze[r][:c - 1] + " " + maze[r][c:]
            case "right":
                maze[r] = maze[r][:c + 2] + " " + maze[r][c + 3:]

    # Set the first cell to be the bottom left one
    # Mark it as visited and add it to the tracking stack
    current_cell = [size[0] - 1, 0]
    maze_matrix[current_cell[0]][current_cell[1]] = 1
    stack = [current_cell]

    # While there are cells in the stack to track
    while stack:
        # Set the last cell in stack as current stack and pop it from te stack
        current_cell = stack.pop()

        # Look for unvisited cells in all 4 directions of the current cell
        unvisited = []
        for i in [current_cell[0] - 1, current_cell[0] + 1]:  # Cells above and below
            if (0 <= i < size[0]) and maze_matrix[i][current_cell[1]] == 0:
                unvisited.append([i, current_cell[1]])
        for i in [current_cell[1] - 1, current_cell[1] + 1]:  # Cells left and right
            if (0 <= i < size[1]) and maze_matrix[current_cell[0]][i] == 0:
                unvisited.append([current_cell[0], i])

        # If there is any unvisited cell around the current cell
        if unvisited:
            # Add the current cell to stack
            stack.append(current_cell)
            # Randomly pick one of the unvisited cells
            current_cell = random.choice(unvisited)
            # Clear the wall between these two cells
            clear_wall(stack[-1], current_cell)
            # Mark the new cell as visited and append it to the stack
            maze_matrix[current_cell[0]][current_cell[1]] = 1
            stack.append(current_cell)

    return maze


# Print the maze
if __name__ == "__main__":
    size = [int(_) for _ in input("Enter the size: ").split()]
    my_maze = generate_maze(size[0], size[1])
    for _ in my_maze:
        print(_)
