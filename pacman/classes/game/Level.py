from enum import Enum, auto
import random
# from Game_Controller import *

# to be factored
class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    SUPER_HARD = auto()
    pass

class Objectify:
    def __init__(self):
        pass
    
    def populate_maze(self, maze, object_list):
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == ' ':
                    maze[y][x] = object_list.pop(0)
        return maze

class Graph:
    def __init__(self):
        pass
    
    def encode_vertex_name(self, x,y):
      return str(x)+','+str(y)

    def decode_vertex_name(self, str):
      return [int(i) for i in str.split(',')]
  
    def add_vertex(self, symbol, vertex, heuristic_value=0, adjacentcy_list={}):
        if vertex not in adjacentcy_list:
            adjacentcy_list[vertex] = [symbol, heuristic_value,[]]
        return adjacentcy_list

    def add_edge(self, symbol_src, node_src, symbol_dest, node_dest, weight=0,adjacentcy_list={}):
        if node_src not in adjacentcy_list:
            adjacentcy_list=self.add_vertex(symbol_src, node_src)
        if node_dest not in adjacentcy_list:
            adjacentcy_list=self.add_vertex(symbol_dest, node_dest)

        if node_src in adjacentcy_list and node_dest in adjacentcy_list:
            adjacentcy_list[node_src][2].append((node_dest, weight))
            adjacentcy_list[node_dest][2].append((node_src, weight))
        return adjacentcy_list
    
    def connect_maze(self, grid_map): #traverse the grid with bfs to connect each node as adjacent vertex to form an edge, not necessary but it looks cool
        # Traditional traverse
        # for i in range(len(self.__grid_map)):
        #   for j in range(len(self.__grid_map[i])):
        #     pass
        walkable_path={}
        # self.__wall_list={}
        grid_width = len(grid_map[0])
        grid_height=len(grid_map)

        # begin_x, begin_y=random.randint(0,grid_height-1),random.randint(0,grid_width-1)
        begin_x, begin_y=0,0
        if grid_map[begin_x][begin_y]=="#":
            while(grid_map[begin_x][begin_y]=="#"):
                begin_x, begin_y=random.randint(0,grid_height-1),random.randint(0,grid_width-1)
        x,y=begin_x,begin_y
        vertex_queue=[self.encode_vertex_name(x,y)]
        visited_vertex=set()
        while(vertex_queue):
            current_vertex=vertex_queue.pop(0)
            visited_vertex.add(current_vertex)

            cur_x,cur_y=self.decode_vertex_name(current_vertex)
            # check adjacent vertex by coordinates
            if (cur_x-1<grid_height and cur_x-1>=0) and (grid_map[cur_x-1][cur_y] != "#"):
                neighbor=self.encode_vertex_name(cur_x-1,cur_y)
                if(neighbor not in visited_vertex or (neighbor,1) not in walkable_path[current_vertex][2]):
                    vertex_queue.append(neighbor)
                    visited_vertex.add(neighbor)
                    walkable_path=self.add_edge(grid_map[cur_x][cur_y],current_vertex,grid_map[cur_x-1][cur_y],neighbor,1, walkable_path)

            if (cur_x+1<grid_height and cur_x+1>=0) and (grid_map[cur_x+1][cur_y] != "#"):
                neighbor=self.encode_vertex_name(cur_x+1,cur_y)
                if(neighbor not in visited_vertex or (neighbor,1) not in walkable_path[current_vertex][2]):
                    vertex_queue.append(neighbor)
                    visited_vertex.add(neighbor)
                    walkable_path=self.add_edge(grid_map[cur_x][cur_y],current_vertex,grid_map[cur_x-1][cur_y],neighbor,1,walkable_path)

            if (cur_y-1<grid_width and cur_y-1>=0) and (grid_map[cur_x][cur_y-1] != "#"):
                neighbor=self.encode_vertex_name(cur_x,cur_y-1)
                if(neighbor not in visited_vertex or (neighbor,1) not in walkable_path[current_vertex][2]):
                    vertex_queue.append(neighbor)
                    visited_vertex.add(neighbor)
                    walkable_path=self.add_edge(grid_map[cur_x][cur_y],current_vertex,grid_map[cur_x-1][cur_y],neighbor,1,walkable_path)

            if (cur_y+1<grid_width and cur_y+1>=0) and (grid_map[cur_x][cur_y+1] != "#"):
                neighbor=self.encode_vertex_name(cur_x,cur_y+1)
                if(neighbor not in visited_vertex or (neighbor,1) not in walkable_path[current_vertex][2]):
                    vertex_queue.append(neighbor)
                    visited_vertex.add(neighbor)
                    walkable_path=self.add_edge(grid_map[cur_x][cur_y],current_vertex,grid_map[cur_x-1][cur_y],neighbor,1,walkable_path)
                    
        return walkable_path

class Maze_Generator:
    def __init__(self):
        self.width = 21
        self.height = 21
        self.grid = [['#' for _ in range(self.width)] for _ in range(self.height)] # base maze
        self.visited = set()

    def generate_maze(self):
        """Generate the maze using Prim's algorithm."""
        self.grid = [['#' for _ in range(self.width)] for _ in range(self.height)]
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
        return self.grid

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
            
    def get_maze(self):
        return self.grid

class Level:
    def __init__(self, level_number=0, level_x_size=27, level_y_size=27):
        self.level_number = level_number
        self.level_graph = None
        self.level_path_list = None
        self.level_maze = None
        self.level_info = None
        
        self.level_x_size = level_x_size
        self.level_y_size = level_y_size
        self.ghost_lineup = []
        self.difficulty = random.choice(list(Difficulty))
        
        # self.EASY_DIFF=["DUMB", "DUMB", "WANDERER", "HUNTER1"] # Ghost arrangement
        # self.MEDIUM_DIFF=["DUMB", "WANDERER", "HUNTER1", "HUNTER1"]
        # self.HARD_DIFF=["DUMB", "WANDERER", "HUNTER1", "HUNTER1", "HUNTER2"]
        # self.SUPERHARD_DIFF=["WANDERER", "HUNTER1","HUNTER1", "HUNTER2","HUNTER2"]    
    
    #difficulty settings to be factored
    def generate_level(self, level=1):
        self.level_number = level
        self.difficulty = random.choice(list(Difficulty))
        # if self.difficulty == Difficulty.EASY:
        #     self.ghost_lineup = [random.choice(self.EASY) for _ in range(4)]
        # elif self.difficulty == Difficulty.MEDIUM:
        #     self.ghost_lineup = [random.choice(self.MEDIUM) for _ in range(5)]
        # elif self.difficulty == Difficulty.HARD:
        #     self.ghost_lineup = [random.choice(self.HARD) for _ in range(6)]
        # elif self.difficulty == Difficulty.SUPER_HARD:
        #     self.ghost_lineup = [random.choice(self.SUPERHARD) for _ in range(8)]
        self.generate_maze(maze_width=self.level_x_size, maze_height=self.level_y_size)
        # self.set_level(self.level_number)
        print("Difficulty: ", self.difficulty)
        
    def advance_level(self):
        self.level_number += 1
        self.generate_level(self.level_number)
    
    def get_level_data(self):
        return {
            'level':self.level_number,
            'difficulty':self.difficulty,
            'size':(self.level_x_size,self.level_y_size),
            'ghosts':self.ghost_lineup,
            'maze':self.level_maze,
            'graph':self.level_graph,
            'path':self.level_path_list
            }
        
    def load_level(self):
        # self.set_level(level_number)
        pass
    
    def generate_maze(self,maze_width=25,maze_height=25, grapher=Graph(), maze=Maze_Generator()):
        maze.width = self.level_x_size = maze_width
        maze.height = self.level_y_size = maze_height
        
        self.level_maze = maze.generate_maze()
        self.level_graph = grapher.connect_maze(self.level_maze)
        self.level_path_list = [str(i) for i in self.level_graph.keys()]
    
if __name__ == "__main__":
    # maze = Maze_Generator()
    # maze.generate_maze()
    # maze.display()
    # level=Level()
    # # level.advance_level()
    # level.generate_maze(maze_width=15,maze_height=15)
    # print(level.get_current_level_data())
    pass
