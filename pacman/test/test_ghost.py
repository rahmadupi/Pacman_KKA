import pygame
import random
import sys
import time
import os
import heapq

def get_base_path():
    if getattr(sys, 'frozen', False): # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()
sys.path.append(os.path.join(base_path, '../classes'))
sys.path.append(os.path.join(base_path, '../classes/Game'))
from Level import Graph
# from Game_Controller import *



# Initialize Pygame
pygame.init()

# Tile dimensions
TILE_SIZE = 20
TILES_X = 30  # Number of tiles horizontally
TILES_Y = 30  # Number of tiles vertically

# Screen dimensions based on tiles
SCREEN_WIDTH = TILE_SIZE * TILES_X
SCREEN_HEIGHT = TILE_SIZE * TILES_Y

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test Ghost")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SHADOW_COLOR = (50, 50, 50)  # Dark gray for shadow

def get_image_surface(file_path):
    image = pygame.image.load(file_path).convert()
    return image

ghostcolor = {
    0: (255, 0, 0, 255),
    1: (255, 128, 255, 255),
    2: (128, 255, 255, 255),
    3: (255, 128, 0, 255),
    4: (50, 50, 255, 255),
    5: (255, 255, 255, 255)}

grid=[[" " for x in range(TILES_X)] for y in range(TILES_Y)]

class ghost:
    def __init__(self, id):
        self.cur_x = 0#TILES_X // 2
        self.cur_y = 0#TILES_Y // 2
        self.velx = 0
        self.vely = 0
        self.speed = 5
        self.path = []
        self.goal='0,0'
        self.reached_goal = True
        
        self.last_path_update_time = time.time()
        
        self.state="IDLE"
        
        self.maze = None
        self.maze_graph = None
        self.id = id
        self.direction = "RIGHT"
        self.movedelay = 0
        
        self.animFrame = 1
        self.animDelay = 0
        self.anim = {}
        
        self.Graph = None
        
        for i in range(1, 7, 1):
            self.anim[i] = get_image_surface(
                os.path.join(base_path, "../resources", "sprite", "ghost " + str(i) + ".gif"))

            # change the ghost color in this frame
            for y in range(0, 24, 1):
                for x in range(0, 24, 1):

                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), ghostcolor[self.id])

        self.animFrame = 1
        self.animDelay = 0
        
    def set_graph(self, graph):
        self.Graph = graph
        
    def set_maze(self, maze):
        self.maze = maze
        self.maze_graph = self.Graph.connect_maze(maze)
    
    def feel_the_player(self, current_vertex, goal_vertex):
        c_x,c_y=self.Graph.decode_vertex_name(current_vertex)
        g_x,g_y=self.Graph.decode_vertex_name(goal_vertex)
        return (c_x-g_x)+(c_y-g_y)
    
    def generate_path(self, goal_node):
        
        def heuristic(current_vertex, goal_vertex):
            c_x,c_y=self.Graph.decode_vertex_name(current_vertex)
            g_x,g_y=self.Graph.decode_vertex_name(goal_vertex)
            return (c_x-g_x)+(c_y-g_y)
        
        found=False
        start_node = self.Graph.encode_vertex_name(int(self.cur_x/TILE_SIZE), int(self.cur_y/TILE_SIZE))
        visited_vertex = set()
        vertex_pqueue = [(heuristic(start_node,goal_node), start_node)]
        current_vertex_cost = {start_node: 0}
        parent_map = {start_node: None}

        while vertex_pqueue and not found:
            _, current_vertex = heapq.heappop(vertex_pqueue)
            if current_vertex not in visited_vertex:
                visited_vertex.add(current_vertex)

                if current_vertex == goal_node:
                    found = True
                    break

                for vertex, weight in self.maze_graph[current_vertex][2]:
                    tentative_neighbor_vertex_cost = current_vertex_cost[current_vertex] + weight
                    if vertex not in current_vertex_cost or tentative_neighbor_vertex_cost < current_vertex_cost[vertex]:
                        current_vertex_cost[vertex] = tentative_neighbor_vertex_cost
                        estimated_goal_cost = tentative_neighbor_vertex_cost + heuristic(vertex,goal_node)
                        heapq.heappush(vertex_pqueue, (estimated_goal_cost, vertex))
                        parent_map[vertex] = current_vertex
        if found:
            path = []
            step = goal_node
            while step is not None:
                path.append(step)
                step = parent_map[step]
            path.reverse()
            self.path=path
            self.goal=self.Graph.encode_vertex_name(self.cur_x//TILE_SIZE, self.cur_y//TILE_SIZE)
            # print(self.path)
            return self.path
    
    def draw(self):
        screen.blit(self.anim[self.animFrame], (self.cur_x, self.cur_y))
        self.animDelay += 1
        if self.animDelay >= 3:
            self.animFrame += 1
            if self.animFrame > 6:
                self.animFrame = 1
            self.animDelay = 0
            
    def move(self):
        self.cur_x += self.velx
        self.cur_y += self.vely
        if self.Graph.decode_vertex_name(self.goal)[0] < int(self.cur_x/TILE_SIZE):
            self.velx = -self.speed
            self.vely = 0
        if self.Graph.decode_vertex_name(self.goal)[0] > int(self.cur_x/TILE_SIZE):
            self.velx = self.speed
            self.vely = 0
        if self.Graph.decode_vertex_name(self.goal)[1] < int(self.cur_y/TILE_SIZE):
            self.vely = -self.speed
            self.velx = 0
        if self.Graph.decode_vertex_name(self.goal)[1] > int(self.cur_y/TILE_SIZE):
            self.vely = self.speed
            self.velx = 0
            
        # print(int(self.cur_x/TILE_SIZE), int(self.cur_y/TILE_SIZE))
        if (self.path and (self.Graph.encode_vertex_name(int(self.cur_x/TILE_SIZE), int(self.cur_y/TILE_SIZE)) == self.goal)):
            if len(self.path)>4:
                self.path.pop(0)
                self.path.pop(0)
                # self.path.pop(0)
                # self.path.pop(0)
            self.goal = self.path.pop(0)
            
        elif not self.path:
            self.velx = 0
            self.vely = 0
            self.reached_goal = True
    def control(self, current_time=0,player=None):
        if current_time - self.last_path_update_time > 1:
            self.last_path_update_time = current_time
            self.generate_path(self.Graph.encode_vertex_name(random.randint(0,29),random.randint(0,29)))
        self.draw()
        self.move()
            

Ghost=[]
for i in range (4):
    Ghost.append(ghost(i))
    Ghost[i].set_graph(Graph())
    Ghost[i].set_maze(grid)
    # Ghost[i].generate_path(Ghost[i].Graph.encode_vertex_name(0,0))

running = True
def is_running():
    global running
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
while running:
    is_running()
    
    # keys = pygame.key.get_pressed()
    # player.move(keys)
    # player.draw()
    current_time = time.time()
    for setan in Ghost:
        setan.control(current_time=current_time)
    # pygame.display.flip()
    pygame.display.update()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()