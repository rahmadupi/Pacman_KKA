"""
Entity.py

This file contains the classes for the entity in the game.
"""
from enum import auto, Enum
import random
import heapq
import time
from Game_Controller import *
TILE_SIZE = 20

def get_base_path():
    if getattr(sys, 'frozen', False): # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()

def load_image(file_path):
    image = pygame.image.load(file_path).convert()
    return image

class Player_State(Enum):
    IDLE = auto()
    NORMAL = auto()
    POWER_KILLER = auto()
    POWER_BANISH = auto()
    POWER_INVINCIBLE = auto()
    POWER_FAST = auto()
    POWER_SLOW = auto()
    AUTO=auto()
    DEAD = auto()
    NEAR_GHOST = auto()
    
class Player:
    def __init__(self, screen):
        self.anim=None
        self.screen = screen
        self.xpos=0
        self.ypos=0
        
        self.velx=0
        self.vely=0
        self.pending_turn = None
        
        self.speed=5
        
        
        self.state_timer = time.time()
        
        self.maze = None
        self.maze_graph = None
        
        self.frame=1
        self.frame_delay=0
        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        
        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "pacman-l " + str(i) + ".gif"))
            self.anim_pacmanR[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "pacman-r " + str(i) + ".gif"))
            self.anim_pacmanU[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "pacman-u " + str(i) + ".gif"))
            self.anim_pacmanD[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "pacman-d " + str(i) + ".gif"))
            self.anim_pacmanS[i] = load_image(os.path.join(os.getcwd(), "pacman/resources", "sprite", "pacman.gif"))
    def set_maze(self, maze, maze_graph):
        self.maze = maze
        self.maze_graph = maze_graph
    
    def get_pos(self):
        return (self.xpos, self.ypos)
    
    def set_pos(self):
        # print("asdsa",self.maze_graph.keys())
        pos=random.choice([str(i) for i in self.maze_graph.keys()])
        self.xpos,self.ypos=[int(i)*TILE_SIZE for i in pos.split(',')]
        # print(pos)
        
    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def get_direction(self):
        if self.velx > 0:
            return "RIGHT"
        elif self.velx < 0:
            return "LEFT"
        elif self.vely > 0:
            return "DOWN"
        elif self.vely < 0:
            return "UP"
        else:
            return
    
    def set_speed(self, speed):
        self.speed = speed
        
    def reset_attr(self):
        self.speed = 5
        self.state = Player_State.NORMAL
        
    def dead(self):
        for i in range(1, 9, 1):
            self.anim_pacmanS[i] = load_image(
                os.path.join(base_path, "pacman/resources", "sprite", "pacman " + str(i) + ".gif"))
            for y in range(0, 24, 1):
                for x in range(0, 24, 1):
                    if self.anim_pacmanS[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim_pacmanS[i].set_at((x, y), (255, 255, 255, 255))
        self.state = Player_State.DEAD
        
    def move(self, keys, offset_x=0, offset_y=0):
        # Handle keyboard input for movement
        if keys[pygame.K_LEFT]:
            self.set_pending_turn(-self.speed, 0)
        elif keys[pygame.K_RIGHT]:
            self.set_pending_turn(self.speed, 0)
        elif keys[pygame.K_UP]:
            self.set_pending_turn(0, -self.speed)
        elif keys[pygame.K_DOWN]:
            self.set_pending_turn(0, self.speed)

        # Constrain movement to allow turns only when aligned with tiles
        if self.xpos % TILE_SIZE == 0 and self.ypos % TILE_SIZE == 0:
            # Allow turning if the pending turn is valid
            if self.pending_turn:
                new_velx, new_vely = self.pending_turn
                new_xpos = self.xpos + new_velx
                new_ypos = self.ypos + new_vely
                if self.is_valid_move(new_xpos, new_ypos):
                    self.velx, self.vely = self.pending_turn
                    self.pending_turn = None

        new_xpos = self.xpos + self.velx
        new_ypos = self.ypos + self.vely

        # Check for collisions with walls before updating position
        if self.is_valid_move(new_xpos, self.ypos):
            self.xpos = new_xpos
        else:
            self.xpos = (self.xpos // TILE_SIZE) * TILE_SIZE
            if self.velx < 0:
                self.xpos += TILE_SIZE
            self.velx = 0

        if self.is_valid_move(self.xpos, new_ypos):
            self.ypos = new_ypos
        else:
            self.ypos = (self.ypos // TILE_SIZE) * TILE_SIZE
            if self.vely < 0:
                self.ypos += TILE_SIZE
            self.vely = 0

    def set_pending_turn(self, velx, vely):
        # Set the pending turn direction
        self.pending_turn = (velx, vely)

    def is_valid_move(self, x, y, offset_x=0, offset_y=0):
        tile_x = (x + TILE_SIZE // 2) // TILE_SIZE 
        tile_y = (y + TILE_SIZE // 2) // TILE_SIZE

        # Check if the tile is within the maze boundaries and not a wall
        if 0 <= tile_x < len(self.maze[0]) and 0 <= tile_y < len(self.maze):
            return self.maze[tile_y][tile_x] != '#'
        return False
            
    def draw(self, offset_x=0, offset_y=0):
        if self.velx > 0:
            self.anim = self.anim_pacmanR
        elif self.velx < 0:
            self.anim = self.anim_pacmanL
        elif self.vely > 0:
            self.anim = self.anim_pacmanD
        elif self.vely < 0:
            self.anim = self.anim_pacmanU
        else:
            self.anim = self.anim_pacmanS
        
        self.screen.blit(self.anim[self.frame], (self.xpos+offset_x, self.ypos+offset_y))
        # self.frame += 1
        self.frame_delay += 1
        if self.frame_delay >= 1:
            self.frame += 1
            if self.frame >= 9:
                self.frame = 1
            self.frame_delay = 0
    
    def control(self, keys=None, current_time=0):
        if current_time - self.state_timer > 10:
            self.reset_attr()
        self.move(keys)
        self.draw()
        pass
                
# =============================================================================

# =============================================================================
# Ghost
class Ghost_State(Enum):
    IDLE=auto()
    STRONG = auto()
    WEAK = auto()
    DEAD = auto()
    CHASE = auto()
    AMBUSH = auto()
    GUARD = auto()
    HUNT = auto()
    WANDER=auto()
    ESCAPE = auto()
    HOSTILE = auto()
    COOLDOWN = auto()
      
class Ghost:
    def __init__(self, screen):
        self.screen=screen
        self.cur_x = 0#TILES_X // 2
        self.cur_y = 0#TILES_Y // 2
        self.velx = 0
        self.vely = 0
        self.speed = 5
        
        self.path = []
        self.goal='0,0'
        self.reached_goal = True
        
        self.state="IDLE"
        self.last_path_update_time = time.time()
        self.last_state_time = time.time()
        
        self.maze = None
        self.maze_graph = None
        
        self.animFrame = 1
        self.animDelay = 0
        self.anim = {}
        
        self.Graph = None

        self.animFrame = 1
        self.animDelay = 0
        
        self.score = 400
        
    def set_graph(self, graph):
        self.Graph = graph
        
    def set_maze(self, maze, maze_graph):
        self.maze = maze
        self.maze_graph = maze_graph
    
    def get_pos(self):
        return (self.cur_x, self.cur_y)
    
    def set_pos(self):
        pos=random.choice([str(i) for i in self.maze_graph.keys()])
        self.cur_x,self.cur_y=[int(i)*TILE_SIZE for i in pos.split(',')]
        
    def set_state(self, state):
        self.state = state
    
    def get_state(self):
        return self.state
    
    def get_score(self):
        return self.score
    
    def dead(self):
        for i in range(1, 7, 1):
            self.anim[i] = load_image(
            os.path.join(base_path, "../../resources", "sprite", "ghost " + str(i) + ".gif"))
            for y in range(0, 24, 1):
                for x in range(0, 24, 1):
                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), (255, 255, 255, 255))
            self.anim[i] = pygame.transform.scale(self.anim[i], (0, 0))
        self.state = Ghost_State.DEAD
    
    def check_collision(self, player):
        ghost_rect = pygame.Rect(self.cur_x, self.cur_y, TILE_SIZE, TILE_SIZE)
        player_rect = pygame.Rect(player.xpos, player.ypos, TILE_SIZE, TILE_SIZE)
        return ghost_rect.colliderect(player_rect)
        
    
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
                try:
                    for vertex, weight in self.maze_graph[current_vertex][2]:
                        tentative_neighbor_vertex_cost = current_vertex_cost[current_vertex] + weight
                        if vertex not in current_vertex_cost or tentative_neighbor_vertex_cost < current_vertex_cost[vertex]:
                            current_vertex_cost[vertex] = tentative_neighbor_vertex_cost
                            estimated_goal_cost = tentative_neighbor_vertex_cost + heuristic(vertex,goal_node)
                            heapq.heappush(vertex_pqueue, (estimated_goal_cost, vertex))
                            parent_map[vertex] = current_vertex
                except KeyError as e:
                    print('KeyError:', e, "May because of the wall")
                    continue
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
    
    def draw(self, offset_x=0, offset_y=0):
        self.screen.blit(self.anim[self.animFrame], (self.cur_x+offset_x, self.cur_y+offset_y))
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
                # self.path.pop(0)
                # self.path.pop(0)
                # self.path.pop(0)
                # self.path.pop(0)
                pass
            self.goal = self.path.pop(0)
            
        elif not self.path:
            self.velx = 0
            self.vely = 0
            self.reached_goal = True
            
    def control(self, current_time=0,player=None):
        # if current_time - self.last_path_update_time > 1:
        #     self.last_path_update_time = current_time
        #     self.generate_path(self.Graph.encode_vertex_name(random.randint(0,29),random.randint(0,29)))
        # self.draw()
        # self.move()
        pass
        

class Dumb_Ghost(Ghost):
    # random wandering
    def __init__(self, screen):
        super().__init__(screen)
        self.type="DUMB"
        self.color=(random.randint(100, 255), random.randint(100, 255), 0, random.randint(100, 255))
        
        for i in range(1, 7, 1):
            self.anim[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "ghost " + str(i) + ".gif"))

            for y in range(0, 24, 1):
                for x in range(0, 24, 1):
                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), self.color)
                        
    def control(self, current_time=0):
        if current_time - self.last_path_update_time > random.randint(1,9):
            self.last_path_update_time = current_time
            self.generate_path(random.choice([str(i) for i in self.maze_graph.keys()]))#self.Graph.encode_vertex_name(random.randint(0,29),random.randint(0,29))
            
        # print(self.path)
        self.move()
        self.draw()

class Wanderer_Ghost(Ghost):
    # random wandering will chase if player seen(by in the same row or column)
    # 5 second chase or timeout
    def __init__(self, screen):
        super().__init__(screen)
        self.type="WANDERER"
        self.color=(0, 255, 0, 255)
        
        for i in range(1, 7, 1):
            self.anim[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "ghost " + str(i) + ".gif"))

            for y in range(0, 24, 1):
                for x in range(0, 24, 1):
                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), self.color)
    def sense_the_player(self, player_pos):
        c_x,c_y=self.cur_x//TILE_SIZE,self.cur_y//TILE_SIZE
        g_x,g_y=player_pos[0]//TILE_SIZE, player_pos[1]//TILE_SIZE#self.Graph.decode_vertex_name(player_pos)
        return (c_x-g_x)+(c_y-g_y)
                        
    def control(self, current_time=0,player=None):
        if self.sense_the_player(player.get_pos()) > 7:    
            self.state = Ghost_State.WANDER
        else:
            self.state= Ghost_State.HUNT
        
        if self.state == Ghost_State.HUNT:
            if current_time - self.last_state_time < random.randint(7, 10):
                if current_time - self.last_path_update_time > 2:
                    self.last_path_update_time = current_time
                    player_pos = player.get_pos()
                    self.generate_path(self.Graph.encode_vertex_name(player_pos[0] // TILE_SIZE, player_pos[1] // TILE_SIZE))
            else:
                self.state = Ghost_State.COOLDOWN
                self.last_state_time = current_time
        elif self.state == Ghost_State.COOLDOWN:
            if current_time - self.last_state_time < 3:
                if current_time - self.last_path_update_time > 2:
                    self.last_path_update_time = current_time
                    self.generate_path(self.Graph.encode_vertex_name(random.randint(0, 29), random.randint(0, 29)))
            else:
                self.state = Ghost_State.WANDER
                self.last_state_time = current_time
        
        if self.state == Ghost_State.WANDER:
            if current_time - self.last_path_update_time > random.randint(1,5):
                self.last_path_update_time = current_time
                self.generate_path(self.Graph.encode_vertex_name(random.randint(0,29),random.randint(0,29)))
        self.draw()
        self.move()

class Hunter2_Ghost(Ghost):
    # bfs for game ballance (depend)
    # hunt and ambush the player by going to the player's predicted position
    # 10second chase 4second cooldown
    # go
    def __init__(self, screen):
        super().__init__(screen)
        self.type="HUNTER2"
        self.color=(0, 0, 255, 255)
        
        for i in range(1, 7, 1):
            self.anim[i] = load_image(
                os.path.join(base_path, "../../resources", "sprite", "ghost " + str(i) + ".gif"))

            for y in range(0, 24, 1):
                for x in range(0, 24, 1):
                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), self.color)
    
    def sense_the_player(self, player_pos):
        c_x,c_y=self.cur_x//TILE_SIZE,self.cur_y//TILE_SIZE
        g_x,g_y=player_pos[0]//TILE_SIZE, player_pos[1]//TILE_SIZE#self.Graph.decode_vertex_name(player_pos)
        return (c_x-g_x)+(c_y-g_y)
    
    def ambush(self, player_direction, player_x, player_y):
        for i in range(5):
            try:
                if player_direction == "LEFT":
                    for i in range(5):
                        if self.maze_graph[player_x-1][player_y] != "#":
                            player_x -= 1
                        elif self.maze_graph[player_x][player_y-1] != "#":
                            player_y -= 1
                        elif self.maze_graph[player_x][player_y+1] != "#":
                            player_y += 1
                        elif self.maze_graph[player_x+1][player_y] != "#":
                            player_x += 1
                elif player_direction == "RIGHT":
                    for i in range(5):
                        if self.maze_graph[player_x+1][player_y] != "#":
                            player_x += 1
                        elif self.maze_graph[player_x][player_y-1] != "#":
                            player_y -= 1
                        elif self.maze_graph[player_x][player_y+1] != "#":
                            player_y += 1
                        elif self.maze_graph[player_x-1][player_y] != "#":
                            player_x -= 1
                elif player_direction == "UP":
                    for i in range(5):
                        if self.maze_graph[player_x][player_y-1] != "#":
                            player_y -= 1
                        elif self.maze_graph[player_x+1][player_y] != "#":
                            player_x += 1
                        elif self.maze_graph[player_x-1][player_y] != "#":
                            player_x -= 1
                        elif self.maze_graph[player_x][player_y+1] != "#":
                            player_y += 1
                elif player_direction == "DOWN":
                    for i in range(5):
                        if self.maze_graph[player_x][player_y+1] != "#":
                            player_y += 1
                        elif self.maze_graph[player_x+1][player_y] != "#":
                            player_x += 1
                        elif self.maze_graph[player_x-1][player_y] != "#":
                            player_x -= 1
                        elif self.maze_graph[player_x][player_y-1] != "#":
                            player_y -= 1
            except KeyError as e:
                print('KeyError:', e)
                return [player_x,player_y]
        return [player_x,player_y]
                        
    def control(self, current_time=0,player=None):
        if self.sense_the_player(player.get_pos()) > 7:    
            self.state = Ghost_State.AMBUSH
        else:
            self.state= Ghost_State.HUNT
            
        if self.state == Ghost_State.HUNT:
            if current_time - self.last_state_time < random.randint(7, 10):
                if current_time - self.last_path_update_time > 1:
                    self.last_path_update_time = current_time
                    player_pos = player.get_pos()
                    self.generate_path(self.Graph.encode_vertex_name(player_pos[0] // TILE_SIZE, player_pos[1] // TILE_SIZE))
            else:
                self.state = Ghost_State.COOLDOWN
                self.last_state_time = current_time
        elif self.state == Ghost_State.COOLDOWN:
            if current_time - self.last_state_time < 3:
                if current_time - self.last_path_update_time > 1:
                    self.last_path_update_time = current_time
                    self.generate_path(self.Graph.encode_vertex_name(random.randint(0, 29), random.randint(0, 29)))
            else:
                self.state = Ghost_State.HUNT
                self.last_state_time = current_time
            
            
        if self.state == Ghost_State.AMBUSH:
            if current_time - self.last_path_update_time > random.randint(1,3):
                self.last_path_update_time = current_time
                player_direction = player.get_direction()
                player_x, player_y = player.get_pos()
                dir=self.ambush(player_direction, player_x, player_y)
                self.generate_path(self.Graph.encode_vertex_name(dir[0], dir[1]))
       
        self.draw()
        self.move()
        
class Hunter1_Ghost(Ghost):
    # bfs for game ballance (depend)
    # hunt the player
    # 7second chase or 2second cooldown
    def __init__(self, screen):
        super().__init__(screen)
        self.type="HUNTER1"
        self.state = Ghost_State.HUNT
        self.color=(50, 50, 50)
        
        for i in range(1, 7, 1):
            self.anim[i] = load_image(os.path.join(base_path, "../../resources", "sprite", "ghost " + str(i) + ".gif"))

            for y in range(0, 24, 1):
                for x in range(0, 24, 1):
                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        self.anim[i].set_at((x, y), self.color)
    
    def control(self, current_time=0,player=None, offset_x=0, offset_y=0):
        if self.state == Ghost_State.HUNT:
            if current_time - self.last_state_time < random.randint(7, 10):
                if current_time - self.last_path_update_time > 1:
                    self.last_path_update_time = current_time
                    player_pos = player.get_pos()
                    self.generate_path(self.Graph.encode_vertex_name(player_pos[0] // TILE_SIZE, player_pos[1] // TILE_SIZE))
            else:
                self.state = Ghost_State.COOLDOWN
                self.last_state_time = current_time
        elif self.state == Ghost_State.COOLDOWN:
            if current_time - self.last_state_time < 2:
                if current_time - self.last_path_update_time > 2:
                    self.last_path_update_time = current_time
                    self.generate_path(self.Graph.encode_vertex_name(random.randint(0, 29), random.randint(0, 29)))
            else:
                self.state = Ghost_State.HUNT
                self.last_state_time = current_time
            
        self.draw(offset_x, offset_y)
        self.move()

# =============================================================================