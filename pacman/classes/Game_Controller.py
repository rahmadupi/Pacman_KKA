import sys
import os
from enum import Enum, auto
import random
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


import Entity
import Level
import Object
import Error
import progress

# to be moved to support OOP principles
# smart screen allignment issue
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
    START = auto()
    MENU= auto()
    GAME_START= auto()
    GAME = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    WIN = auto()
    
def load_image(file_name):
    return pygame.image.load(os.path.join(base_path,'..','resources','sprite', file_name)).convert_alpha()

def scale_logo(image, new_width):
        width, height = image.get_size()
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))
    
class Start_Menu:
    def __init__(self, screen):
        self.screen = screen
        self.state = Game_State.START
        
        self.font_path = os.path.join(base_path,'..','resources','font','Minecraft.ttf')

        self.logo_image = scale_logo(load_image('logo.gif'), 400)
        self.font = pygame.font.Font(self.font_path, 28)
        self.font1 = pygame.font.Font(self.font_path, 26)
        self.font2 = pygame.font.Font(self.font_path, 22)
        self.font3 = pygame.font.Font(self.font_path, 19)
        self.font3 = pygame.font.Font(self.font_path, 14)
        
        self.difficulty_selection=0
        self.difficulty_options = list(Level.Difficulty.__members__.keys())
        # print(self.difficulty_options)
        
        #background
        self.ghost_background = []
        self.grid_background=[[" " for x in range(TILES_X)] for y in range(TILES_Y)]
        self.graph_background = Level.Graph().connect_maze(self.grid_background)
        for i in range(random.randint(10,25)):
            self.ghost_background.append(Entity.Dumb_Ghost(self.screen))
            self.ghost_background[i].set_maze(self.grid_background, self.graph_background)
            self.ghost_background[i].set_graph(Level.Graph())
            self.ghost_background[i].set_pos()
        
    def background(self):
        current_time=time.time()
        for setan in self.ghost_background:
            setan.control(current_time)
        
    def start_menu(self):        
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        self.background()
        
        logo_rect = self.logo_image.get_rect(center=(self.screen.get_width() // 2, 200))
        text = '< Press any key to Play >'
        outline_color = (255, 0, 0)
        text_color = (255, 255, 255)
        
        # Create the outline by rendering the text multiple times with slight offsets
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            outline_surface = self.font2.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 320 + dy))
            self.screen.blit(outline_surface, outline_rect)
        
        # Render the main text
        text_surface = self.font2.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 320))
        self.screen.blit(text_surface, text_rect)
        
        self.screen.blit(self.logo_image, logo_rect)
        pygame.display.flip()
    
    def difficulty_menu(self):
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        self.background()
        
        title_text = 'Choose Difficulty:'
        title_outline_color = (255, 0, 0)
        title_color = (255, 255, 255)
        title_surface = self.font.render(title_text, True, title_outline_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 210))
        
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            outline_surface = self.font.render(title_text, True, title_outline_color)
            outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 210 + dy))
            self.screen.blit(outline_surface, outline_rect)
        
        title_surface = self.font.render(title_text, True, title_color)
        self.screen.blit(title_surface, title_rect)
        
        for i, option in enumerate(self.difficulty_options):
            option_text = option
            if i == self.difficulty_selection:
                outline_color = (0, 0, 255) 
                text_color = (255, 0, 0) 
            else:
                outline_color = (255, 255, 255)
                text_color = (255, 255, 0)  
            
            for dx, dy in offsets:
                outline_surface = self.font2.render(option_text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, self.screen.get_height() // 2.1 + i * 35 + dy))
                self.screen.blit(outline_surface, outline_rect)
            
            option_surface = self.font2.render(option_text, True, text_color)
            option_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.1 + i * 35))
            self.screen.blit(option_surface, option_rect)
        
        pygame.display.flip()
        
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        
    def get_difficulty(self):
        return self.difficulty_options[self.difficulty_selection]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == Game_State.START:
                if event.key == pygame.K_RETURN:
                    self.state = Game_State.MENU
                    time.sleep(0.25)
                    
            elif self.state == Game_State.MENU:
                # time.sleep(0.25)
                if event.key == pygame.K_UP:
                    self.difficulty_selection = (self.difficulty_selection - 1) % 4
                elif event.key == pygame.K_DOWN:
                    self.difficulty_selection = (self.difficulty_selection + 1) % 4
                elif event.key == pygame.K_ESCAPE:
                    self.state = Game_State.START
                    
                elif event.key == pygame.K_RETURN:
                    self.state = Game_State.GAME_START
                    self.difficulty = self.difficulty_options[self.difficulty_selection]

class Game:
    def __init__(self, screen, user=None):
        self.screen = screen
        self.state = Game_State.START
        self.user=user
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
        self.Fruit=[]
        
        # self.player_x = 1  # Initial player position (tile coordinates)
        # self.player_y = 1
        # self.food_pellets = self.initialize_food_pellets()
        
        self.wall_image = load_image('wall-nub.gif')
        self.life_image = load_image('life.gif')
        
    # def set_player(self, player):
    #     self.Player=player  
        
    # def set_ghost(self, ghost_lineup):
    #     pass    
    
    # def set_food_pellets(self, food_pe llets):
    #     # self.Food_Pellets=food_pellets
    #     pass
    # def set_fruit(self, fruit):
    #     # self.Fruit=fruit
    #     pass
        
    def initialize_game(self, level_data=None, Player=None, difficulty=None):
        self.maze_width=level_data['size'][0]*self.tile_size
        self.maze_height=level_data['size'][1]*self.tile_size
        self.maze_layout=level_data['maze']
        self.maze_graph=level_data['graph']
        self.maze_path=level_data['path']
        # print(self.maze_layout)
        
        self.Player = Player
        self.Player.set_maze(self.maze_layout, self.maze_graph)
        self.Player.set_pos()
        if difficulty == Level.Difficulty.EASY:
            for i in range(4):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level.Difficulty.MEDIUM:
            for i in range(5):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen),Entity.Hunter1_Ghost(self.screen),Entity.Hunter2_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                # self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level.Difficulty.HARD:
            for i in range(6):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen),Entity.Hunter1_Ghost(self.screen),Entity.Hunter2_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level.Difficulty.SUPER_HARD:
            for i in range(8):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level.Graph())
                self.Ghost[i].set_pos()
    
    def draw_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.screen.blit(self.wall_image, (x * self.tile_size, y * self.tile_size))

    def update_offsets(self):
        # Calculate the offsets to center the maze
        maze_width = len(self.maze_layout[0]) * TILE_SIZE
        maze_height = len(self.maze_layout) * TILE_SIZE

        # Calculate the offsets to center the maze on the screen
        self.offset_x = 0#(SCREEN_WIDTH - maze_width) // 2
        self.offset_y = 0#(SCREEN_HEIGHT - maze_height) // 2

    
    def update_screen(self):
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        self.update_offsets()
        current_time=time.time()
        
        self.draw_maze()
        for setan in self.Ghost:
            if isinstance(setan,Entity.Dumb_Ghost):
                setan.control(current_time)
            else:
                setan.control(current_time, self.Player)
            
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
    def __init__(self, screen):
        self.screen = screen
        
        self.start_menu = None
        self.level = None
        self.game = None
        
    def set_start_menu(self, start_menu):
        self.start_menu = start_menu
    
    def set_game(self, game):
        self.game = game
        
    def set_level(self, level):
        self.level = level
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            result=None
            if self.start_menu.get_state() == Game_State.START:
                self.start_menu.start_menu()
            elif self.start_menu.get_state() == Game_State.MENU:
                self.start_menu.difficulty_menu()
            elif self.start_menu.get_state() == Game_State.GAME_START:
                # print('Game Start')
                # print(self.start_menu.get_difficulty())
                self.level.generate_level()
                self.game.initialize_game(self.level.get_level_data(), Entity.Player(screen), self.start_menu.get_difficulty())
                result=self.game.run()
            self.start_menu.handle_event(event)
            # self.game.handle_event(event)
            pygame.time.Clock().tick(30)

if __name__== '__main__':
    # Level_node = Level.Level()
    # Level_node.advance_level()
    # Game.initialize_game(Level_node.get_level_data(), Player=Entity.Player(screen))
    # Game.run()
    
    Game = Game(screen, 'user')
    level_node = Level.Level()
    game_controller = Game_Controller(screen)
    game_controller.set_start_menu(Start_Menu(screen))
    game_controller.set_game(Game)
    game_controller.set_level(level_node)
    game_controller.run()