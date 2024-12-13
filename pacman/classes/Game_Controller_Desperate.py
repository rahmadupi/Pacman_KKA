import sys
import os
from enum import Enum, auto
import pygame
import time

def get_base_path():
    if getattr(sys, 'frozen', False): # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()

sys.path.append(os.path.join(base_path,'Game'))
sys.path.append(os.path.join(base_path,'Progress'))
sys.path.append(os.path.join(base_path,'User_Interface'))
sys.path.append(os.path.join(base_path,'Error'))
sys.path.append(os.path.join(base_path,'Database'))

import User_Interface
import Account
import Achievement
import Entity
import Level as Lv
import Object
import Error
import Database
import Scoreboard


TILE_SIZE = 20
TILES_X = 27
TILES_Y = 27
SCREEN_WIDTH = TILE_SIZE * TILES_X
SCREEN_HEIGHT = TILE_SIZE * TILES_Y
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-man")

current_time=time.time()

class Game_State(Enum):
    MAIN_MENU = auto()
    GAME_START= auto()
    GAME = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    WIN = auto()
    pass

class Game:
    def load_image(file_name):
        return pygame.image.load(os.path.join(base_path,'..','resources','sprite', file_name)).convert_alpha()
    
    def __init__(self, screen, user):
        self.screen = screen
        self.user=user
        
        self.font = pygame.font.SysFont('Minecraft', 20)
        self.score=0
        self.life=3
        
        self.tile_size = TILE_SIZE
        self.maze_layout = None
        self.maze_graph = None
        self.maze_path = None
        self.maze_width = None
        self.maze_height = None
        
        self.Player=None
        self.Ghost=[]
        self.Food_Pellets=[]
        self.Fruit=None
        
        self.wall_image = Game.load_image('wall-nub.gif')
        self.ready_image = Game.load_image('ready.gif')
        self.gameover_image = Game.load_image('gameover.gif')
        self.logo_image = Game.load_image('logo.gif')
        self.life_image = Game.load_image('life.gif')
        
    def set_player(self, player):
        self.Player=player
        
    def set_ghost(self, ghost_lineup):
        pass
    
    def set_food_pellets(self, food_pellets):
        # self.Food_Pellets=food_pellets
        pass
    def set_fruit(self, fruit):
        # self.Fruit=fruit
        pass
    
    def draw_text(self, text, position, color=(255, 255, 255), outline_color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        text_surface = self.font.render(text, True, color)
        outline_surface = self.font.render(text, True, outline_color)
        
        # Draw outline
        x, y = position
        self.screen.blit(outline_surface, (x - 1, y - 1))
        self.screen.blit(outline_surface, (x + 1, y - 1))
        self.screen.blit(outline_surface, (x - 1, y + 1))
        self.screen.blit(outline_surface, (x + 1, y + 1))
        
        # Draw main text
        self.screen.blit(text_surface, position)
        
    def initialize_game(self, level_data=None, Player=None):
        self.maze_width=level_data['size'][0]*self.tile_size
        self.maze_height=level_data['size'][1]*self.tile_size
        self.maze_layout=level_data['maze']
        self.maze_graph=level_data['graph']
        self.maze_path=level_data['path']
        # print(self.maze_layout)
        
        self.Player = Player
        self.Player.set_maze(self.maze_layout, self.maze_graph)
        self.Player.set_pos()
        if level_data['difficulty'] == Lv.Difficulty.EASY:
            for i in range(3):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Lv.Graph())
                self.Ghost[i].set_pos()
        elif level_data['difficulty'] == Lv.Difficulty.MEDIUM:
            for i in range(4):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Lv.Graph())
                self.Ghost[i].set_pos()
        elif level_data['difficulty'] == Lv.Difficulty.HARD:
            for i in range(5):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Lv.Graph())
                self.Ghost[i].set_pos()
        elif level_data['difficulty'] == Lv.Difficulty.SUPER_HARD:
            for i in range(8):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Lv.Graph())
                self.Ghost[i].set_pos()
        
        for i,node in enumerate(self.maze_graph.keys()):
            self.Food_Pellets.append(Object.Pellet_Food(self.screen, int(node.split(',')[1]), int(node.split(',')[0])))
        # for y, row in enumerate(self.maze_layout):
        #     for x, tile in enumerate(row):
        #         if tile == ' ': 
        #     # print(node)
        #             self.Food_Pellets.append(Object.Pellet_Food(self.screen,x, y))
        
    def draw_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.screen.blit(self.wall_image, (x * self.tile_size, y * self.tile_size))

    def update_offsets(self):
        # Calculate the offsets to center the maze
        maze_width = (len(self.maze_layout[0]) * TILE_SIZE)
        maze_height = (len(self.maze_layout) * TILE_SIZE)

        # Calculate the offsets to center the maze on the screen
        self.offset_x = 0#(SCREEN_WIDTH - maze_width) // 2
        self.offset_y = 0#(SCREEN_HEIGHT - maze_height) // 2

    
    def update_screen(self):
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        self.update_offsets()
        current_time=time.time()
        self.draw_maze()
        self.draw_text(f'Lives: {self.life}', (5, self.screen.get_height() - 50),(255,255,255))
        self.draw_text(f'Score: {self.score}', (10, self.screen.get_height() - 25),(255,255,255))
        
        for food in self.Food_Pellets:
            if food.check_collision(self.Player):
                self.score+=food.get_score()
                self.Food_Pellets.remove(food)
                continue
            food.draw()
        for setan in self.Ghost:
            setan.control(current_time)
        print(len(self.Food_Pellets))
        # self.Ghost.control(current_time)
        keys=pygame.key.get_pressed()
        self.Player.move(keys, self.offset_x, self.offset_y)
        self.Player.draw(self.offset_x, self.offset_y)
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.update_screen()
            # pygame.display.update()
            pygame.time.Clock().tick(30)

class Game_Controller:
    # score
    pass


if __name__ == '__main__':
    # print('Game Controller')
    Game = Game(screen, 'user')
    Level_Cls = Lv.Level()
    Level_Cls.advance_level()
    Game.initialize_game(Level_Cls.get_current_level_data(), Player=Entity.Player(screen))
    Game.run()