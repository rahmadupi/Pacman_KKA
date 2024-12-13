import sys
import os
from enum import Enum, auto
import pygame

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
import Level
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
        self.tile_size = TILE_SIZE
        self.maze_layout = None
        self.maze_graph = None
        self.maze_path = None
        self.maze_width = None
        self.maze_height = None
        
        self.Player=None
        self.Ghost=None
        self.Food_Pellets=None
        self.Fruit=None
        
        # self.player_x = 1  # Initial player position (tile coordinates)
        # self.player_y = 1
        # self.food_pellets = self.initialize_food_pellets()
        
        self.wall_image = Game.load_image('wall-nub.gif')
        self.ready_image = Game.load_image('ready.gif')
        self.gameover_image = Game.load_image('gameover.gif')
        self.logo_image = Game.load_image('logo.gif')
        self.life_image = Game.load_image('life.gif')
        
    def set_player(self, player):
        self.Player=player
        
    def set_ghost(self, ghost_lineup):
        # self.Ghost=ghost
        pass
    def set_food_pellets(self, food_pellets):
        # self.Food_Pellets=food_pellets
        pass
    def set_fruit(self, fruit):
        # self.Fruit=fruit
        pass
        
    def initialize_game(self, Level=None, Player=None):
        self.maze_width=Level['size'][0]*self.tile_size
        self.maze_height=Level['size'][1]*self.tile_size
        self.maze_layout=Level['maze']
        self.maze_graph=Level['graph']
        self.maze_path=Level['path']
        # print(self.maze_layout)
        
        self.Player = Player
        self.Player.set_maze(self.maze_layout, self.maze_graph)
        self.Player.set_pos()
        
        # print(self.Player.xpos, self.Player.ypos)
        # print(self.Player.xpos, self.Player.ypos)
        # self.ghosts = [Entity.Ghost(i) for i in range(4)]
        # self.level = Level.Level()
        # self.scoreboard = Scoreboard.Scoreboard()
        # self.achievement = Achievement.Achievement()
        # self.database = Database.Database()
        # self.account = Account.Account()
        # self.error = Error.Error()
        # self.game_state = Game_State.MAIN_MENU
        # self.user_interface = User_Interface.User_Interface()
        # self.object = Object.Object()
        # self.smart_move_screen = SmartMoveScreen(screen, tile_size, maze_layout)
        # self.level = Level.Level()
        # self.graph = Level.Graph()
        pass

    # def initialize_food_pellets(self):
    #     food_pellets = []
    #     for y, row in enumerate(self.maze_layout):
    #         for x, tile in enumerate(row):
    #             if tile == ' ':
    #                 food_pellets.append((x, y))
    #     return food_pellets

    def draw_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.screen.blit(self.wall_image, (x * self.tile_size, y * self.tile_size))

    # def draw_food_pellets(self):
        # food_color = (255, 255, 0)  # Yellow color for food pellets
        # for pellet in self.food_pellets:
        #     pellet_rect = pygame.Rect(
        #         pellet[0] * self.tile_size + self.offset_x + self.tile_size // 4,
        #         pellet[1] * self.tile_size + self.offset_y + self.tile_size // 4,
        #         self.tile_size // 2,
        #         self.tile_size // 2
        #     )
        #     pygame.draw.rect(self.screen, food_color, pellet_rect)

    # def draw_player(self):
    #     player_color = (255, 0, 0)  # Red color for the player
    #     player_rect = pygame.Rect(
    #         self.player_x * self.tile_size + self.offset_x,
    #         self.player_y * self.tile_size + self.offset_y,
    #         self.tile_size,
    #         self.tile_size
    #     )
    #     pygame.draw.rect(self.screen, player_color, player_rect)

    # def move_player(self, dx, dy):
    #     new_x = self.player_x + dx
    #     new_y = self.player_y + dy
    #     if self.maze_layout[new_y][new_x] != '#':  # Check if the new position is not a wall
    #         self.player_x = new_x
    #         self.player_y = new_y
            # self.check_food_collision()

    # def check_food_collision(self):
    #     if (self.player_x, self.player_y) in self.food_pellets:
    #         self.food_pellets.remove((self.player_x, self.player_y))

    def update_offsets(self):
        self.offset_x = 0
        self.offset_y = 0
        # center_offset_x = SCREEN_WIDTH // 2 - self.Player.xpos * self.tile_size
        # center_offset_y = SCREEN_HEIGHT // 2 - self.Player.ypos * self.tile_size
        # print(self.Player.xpos,self.Player.ypos)
        # max_offset_x = TILE_SIZE
        # min_offset_x = SCREEN_WIDTH - self.maze_width - TILE_SIZE
        # max_offset_y = TILE_SIZE
        # min_offset_y = SCREEN_HEIGHT - self.maze_height - TILE_SIZE

        # self.offset_x = max(min(center_offset_x, max_offset_x), min_offset_x)
        # self.offset_y = max(min(center_offset_y, max_offset_y), min_offset_y)

    
    def update_screen(self):
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        self.update_offsets()
        # self.draw_food_pellets()
        # self.draw_player()
        keys=pygame.key.get_pressed()
        self.Player.move(keys)
        self.Player.draw(self.offset_x,self.offset_y)
        self.draw_maze()
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
    Level = Level.Level()
    Level.advance_level()
    Game.initialize_game(Level.get_current_level_data(), Player=Entity.Player(screen))
    Game.run()