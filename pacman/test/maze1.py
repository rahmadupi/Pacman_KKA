import random

class MazeGenerator:
    def __init__(self, width=24, height=24):
        self.width = width
        self.height = height
        self.grid = [['#' for _ in range(width)] for _ in range(height)] # base maze
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

            # carve
            adjacent_visited = self.get_adjacent_visited(current_x, current_y)
            if adjacent_visited:
                # Carve a path to the adjacent visited cell
                px, py = random.choice(adjacent_visited)
                self.grid[current_y][current_x] = ' '
                self.grid[(py + current_y) // 2][(px + current_x) // 2] = ' '
                self.visited.add((current_x, current_y))

                # Add new frontier cells
                frontier.extend(self.get_frontier_cells(current_x, current_y))

    def get_frontier_cells(self, x, y):
        """Get frontier cells that are adjacent to the visited cells."""
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        frontier_cells = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 < nx < self.width and 0 < ny < self.height and 
                (nx, ny) not in self.visited and (nx, ny) not in frontier_cells):
                
                # The frontier cell must be a wall inside the grid
                if self.grid[ny][nx] == '#':
                    frontier_cells.append((nx, ny))
        
        return frontier_cells

    def get_adjacent_visited(self, x, y):
        """Get adjacent visited cells to the current cell."""
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)] # right, left, down, up
        adjacent_cells = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and
                (nx, ny) in self.visited):
                adjacent_cells.append((nx, ny))
        
        return adjacent_cells

    def display(self):
        """Display the maze."""
        for row in self.grid:
            print(''.join(row))

# Test the maze generator
if __name__ == "__main__":
    maze = MazeGenerator(width=19, height=13)
    maze.generate_maze()
    maze.display()
