import random

class MazeGenerator:
    def __init__(self, width=24, height=24):
        self.width = width
        self.height = height
        self.grid = [['#' for _ in range(width)] for _ in range(height)]
        self.visited = set()

    def generate_maze(self):
        """Generate the maze using Prim's algorithm."""
        # Start with an initial random cell
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = ' '
        self.visited.add((start_x, start_y))

        # Initialize the frontier with adjacent cells
        frontier = self.get_frontier_cells(start_x, start_y)

        while frontier:
            # Randomly pick a frontier cell
            current_x, current_y = random.choice(frontier)
            frontier.remove((current_x, current_y))

            # Check if the cell can be added to the maze
            adjacent_visited = self.get_adjacent_visited(current_x, current_y)
            if adjacent_visited:
                # Carve a path to the adjacent visited cell
                px, py = random.choice(adjacent_visited)
                self.grid[current_y][current_x] = ' '
                self.grid[(py + current_y) // 2][(px + current_x) // 2] = ' '
                self.visited.add((current_x, current_y))

                # Add new frontier cells
                frontier.extend(self.get_frontier_cells(current_x, current_y))

        # Carve out a few holes in the outer walls
        self.carve_outer_walls()

    def get_frontier_cells(self, x, y):
        """Get frontier cells that are adjacent to the visited cells, including outer edges."""
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        frontier_cells = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check for wrapping around the boundaries
            if nx < 0:
                nx = self.width - 2  # Wrap around to the far right
            elif nx >= self.width:
                nx = 1  # Wrap around to the far left
            if ny < 0:
                ny = self.height - 2  # Wrap around to the bottom
            elif ny >= self.height:
                ny = 1  # Wrap around to the top

            if (0 <= nx < self.width and 0 <= ny < self.height and
                (nx, ny) not in self.visited and (nx, ny) not in frontier_cells):
                # The frontier cell must be a wall in the grid
                if self.grid[ny][nx] == '#':
                    frontier_cells.append((nx, ny))

        return frontier_cells

    def get_adjacent_visited(self, x, y):
        """Get adjacent visited cells to the current cell."""
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        adjacent_cells = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and
                (nx, ny) in self.visited):
                adjacent_cells.append((nx, ny))

        return adjacent_cells

    def carve_outer_walls(self):
        """Carve a few holes in the outer walls to create entry/exit points."""
        # Carve entry/exit points on the top row
        for x in range(2, self.width - 2, 4):
            self.grid[0][x] = ' '
        
        # Carve entry/exit points on the left column
        for y in range(2, self.height - 2, 4):
            self.grid[y][0] = ' '
        
        # Carve entry/exit points on the right column
        for y in range(2, self.height - 2, 4):
            self.grid[y][self.width - 1] = ' '
        
        # Carve entry/exit points on the bottom row
        for x in range(2, self.width - 2, 4):
            self.grid[self.height - 1][x] = ' '

    def display(self):
        """Display the maze."""
        for row in self.grid:
            print(''.join(row))

# Test the maze generator
if __name__ == "__main__":
    maze = MazeGenerator(width=10, height=10)
    maze.generate_maze()
    maze.display()
