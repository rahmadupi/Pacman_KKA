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
import Level_Manager
import Object
import Error
import Progress

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
    GAME_RESTART = auto()
    GAME_OVER = auto()
    WIN = auto()
    END = auto()
    
def load_image(file_name):
    return pygame.image.load(os.path.join(base_path,'..','resources','sprite', file_name)).convert_alpha()

def scale_logo(image, new_width):
        width, height = image.get_size()
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))
    
class Start_Menu:
    def __init__(self, screen, Account, Scoreboard, Achievement):
        self.screen = screen
        self.state = Game_State.START
        
        self.Account_Node = Account
        self.Scoreboard_Node = Scoreboard
        self.Achievement_Node = Achievement
        
        self.font_path = os.path.join(base_path,'..','resources','font','Minecraft.ttf')

        self.logo_image = scale_logo(load_image('logo.gif'), 400)
        self.font = pygame.font.Font(self.font_path, 28)
        self.font1 = pygame.font.Font(self.font_path, 26)
        self.font2 = pygame.font.Font(self.font_path, 22)
        self.font3 = pygame.font.Font(self.font_path, 19)
        self.font3 = pygame.font.Font(self.font_path, 14)
        
        self.user_selection=0
        # self.difficulty_options = list(Level.Difficulty.__members__.keys())
        self.user_options = None
        # print(self.difficulty_options)
        
        #background
        self.ghost_background = []
        self.grid_background=[[" " for x in range(TILES_X)] for y in range(TILES_Y)]
        self.graph_background = Level_Manager.Graph().connect_maze(self.grid_background)
            
        for i in range(random.randint(10,25)):
            self.ghost_background.append(Entity.Dumb_Ghost(self.screen))
            self.ghost_background[i].set_maze(self.grid_background, self.graph_background)
            self.ghost_background[i].set_graph(Level_Manager.Graph())
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
    
    def user_menu(self):
        # self.screen.fill((0, 0, 0))  # Clear the screen with black
        # self.background()
        
        # title_text = 'Choose Save Data:'
        # title_outline_color = (255, 0, 0)
        # title_color = (255, 255, 255)
        # title_surface = self.font.render(title_text, True, title_outline_color)
        # title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 210))
        
        # offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        # for dx, dy in offsets:
        #     outline_surface = self.font.render(title_text, True, title_outline_color)
        #     outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, 210 + dy))
        #     self.screen.blit(outline_surface, outline_rect)
        
        # title_surface = self.font.render(title_text, True, title_color)
        # self.screen.blit(title_surface, title_rect)
        
        # for i, option in enumerate(self.difficulty_options):
        #     option_text = Level.Difficulty(option).name
        #     if i == self.difficulty_selection:
        #         outline_color = (0, 0, 255) 
        #         text_color = (255, 0, 0) 
        #     else:
        #         outline_color = (255, 255, 255)
        #         text_color = (255, 255, 0)  
            
        #     for dx, dy in offsets:
        #         outline_surface = self.font2.render(option_text, True, outline_color)
        #         outline_rect = outline_surface.get_rect(center=(self.screen.get_width() // 2 + dx, self.screen.get_height() // 2.1 + i * 35 + dy))
        #         self.screen.blit(outline_surface, outline_rect)
            
        #     option_surface = self.font2.render(option_text, True, text_color)
        #     option_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.1 + i * 35))
        #     self.screen.blit(option_surface, option_rect)
        
        # pygame.display.flip()
        pass
        
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        
    def get_difficulty(self):
        return self.difficulty_options[self.difficulty_selection]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == Game_State.START:
                self.state = Game_State.MENU
                time.sleep(0.25)
                
            elif self.state == Game_State.MENU:
                # time.sleep(0.25)
                if event.key == pygame.K_UP:
                    self.user_selection = (self.user_selection - 1) % len(self.user_options)
                elif event.key == pygame.K_DOWN:
                    self.user_selection = (self.user_selection + 1) % len(self.user_options)
                elif event.key == pygame.K_ESCAPE:
                    self.state = Game_State.START
                    
                elif event.key == pygame.K_RETURN:
                    self.state = Game_State.GAME_START
                    self.difficulty = self.user_options[self.user_selection]

class Game:
    def __init__(self, screen, user=None, tile_size=TILE_SIZE):
        self.screen = screen
        self.state = Game_State.START
        self.user=user
        self.score=0
        self.life=3
        self.level = 0
        
        self.running = True
        
        self.tile_size = tile_size
        self.maze_layout = None
        self.maze_graph = None
        self.maze_path = None
        self.maze_width = None
        self.maze_height = None
        self.difficulty = None
        
        self.Player=None
        self.Ghost=[]
        self.Food_Pellets=[]
        self.Fruit=[]
        
        self.font_path = os.path.join(base_path,'..','resources','font','Minecraft.ttf')
        self.font = pygame.font.Font(self.font_path, 22)
        
        self.start_image = load_image('start.gif')
        self.ready_image = load_image('ready.gif')
        self.game_over_image = load_image('gameover.gif')
        self.life_image = load_image('life.gif')
        
        self.wall_nub = load_image('wall-nub.gif')
        self.wall_corner_ll = load_image('wall-corner-ll.gif')
        self.wall_corner_lr = load_image('wall-corner-lr.gif')
        self.wall_corner_ul = load_image('wall-corner-ul.gif')
        self.wall_corner_ur = load_image('wall-corner-ur.gif')
        self.wall_end_b = load_image('wall-end-b.gif')
        self.wall_end_l = load_image('wall-end-l.gif')
        self.wall_end_r = load_image('wall-end-r.gif')
        self.wall_end_t = load_image('wall-end-t.gif')
        self.wall_straight_horiz = load_image('wall-straight-horiz.gif')
        self.wall_straight_vert = load_image('wall-straight-vert.gif')
        self.wall_t_left = load_image('wall-t-left.gif')
        self.wall_t_right = load_image('wall-t-right.gif')
        self.wall_t_up = load_image('wall-t-top.gif')
        self.wall_t_bottom = load_image('wall-t-bottom.gif')
        self.wall_x = load_image('wall-x.gif')
        
        
    def initialize_game(self, level_data=None, Player=None, difficulty=None):
        self.maze_width=level_data['size'][0]*self.tile_size
        self.maze_height=level_data['size'][1]*self.tile_size
        self.maze_layout=level_data['maze']
        self.maze_graph=level_data['graph']
        self.maze_path=level_data['path']
        
        self.level=level_data['level']
        self.difficulty=level_data['difficulty'].__members__.keys()
        
        
        #...................................................
        self.Player = Player
        self.Player.set_maze(self.maze_layout, self.maze_graph)
        self.Player.set_pos()
        if difficulty == Level_Manager.Difficulty.EASY:
            for i in range(4):
                self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level_Manager.Difficulty.MEDIUM:
            for i in range(5):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen),Entity.Hunter1_Ghost(self.screen),Entity.Hunter2_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                # self.Ghost.append(Entity.Dumb_Ghost(self.screen))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level_Manager.Difficulty.HARD:
            for i in range(6):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen),Entity.Hunter1_Ghost(self.screen),Entity.Hunter2_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        elif difficulty == Level_Manager.Difficulty.SUPER_HARD:
            for i in range(8):
                self.Ghost.append(random.choice([Entity.Dumb_Ghost(self.screen), Entity.Wanderer_Ghost(self.screen)]))
                self.Ghost[i].set_maze(self.maze_layout, self.maze_graph)
                self.Ghost[i].set_graph(Level_Manager.Graph())
                self.Ghost[i].set_pos()
        
        for vertex in self.maze_path:
            x,y=vertex.split(',')
            self.Food_Pellets.append(Object.Pellet_Food(self.screen, int(y), int(x)))
            
    def set_user(self, user):
        self.user = user
        
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        
    def draw_hud(self):
        # Draw life images in the bottom left corner
        life_x = 10
        life_y = self.screen.get_height() - self.life_image.get_height() - 10
        for i in range(self.life):
            self.screen.blit(self.life_image, (life_x, life_y))
            life_x += self.life_image.get_width() + 5  # Add some spacing between life images

        # Draw score next to the life images with a red outline
        score_text = f'Score: {self.score}'
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        score_outline_surface = self.font.render(score_text, True, (255, 0, 0))
        score_rect = score_surface.get_rect(bottomleft=(life_x + 5, self.screen.get_height() -5))
        score_outline_rect = score_outline_surface.get_rect(bottomleft=(life_x + 5, self.screen.get_height() - 5))

        # Draw the outline by rendering the text multiple times with slight offsets
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in offsets:
            self.screen.blit(score_outline_surface, score_outline_rect.move(dx, dy))
        self.screen.blit(score_surface, score_rect)
        
    def draw_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.screen.blit(self.wall_nub, (x * self.tile_size, y * self.tile_size))

                
    def game_begin(self):
        # self.screen.fill((0, 0, 0))
        self.update_screen()
        ready_rect = self.ready_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(self.ready_image, ready_rect)
        pygame.display.flip()
        time.sleep(2)
    
    def game_restart(self):
        self.Player.set_pos()
        for setan in self.Ghost:
            setan.set_pos()
        self.game_begin()
        
    def game_over(self):
        return [self.user, self.score, self.level]
            
    def reset_game(self):
        # self.Player=None
        self.Ghost=[]
        self.Food_Pellets=[]
        self.score=0
        self.life=3
        # self.maze_layout = None
        # self.maze_graph = None
        # self.maze_path = None
        # self.maze_width = None
        # self.maze_height = None   
        
        self.screen.blit(self.game_over_image, (self.screen.get_width() // 2 - self.game_over_image.get_width() // 2, self.screen.get_height() // 2 - self.game_over_image.get_height() // 2))
        pygame.display.flip()
        # time.sleep(2)

    def update_offsets(self):
        # Calculate the offsets to center the maze
        maze_width = len(self.maze_layout[0]) * TILE_SIZE
        maze_height = len(self.maze_layout) * TILE_SIZE

        # Calculate the offsets to center the maze on the screen
        self.offset_x = 0#(SCREEN_WIDTH - maze_width) // 2
        self.offset_y = 0#(SCREEN_HEIGHT - maze_height) // 2

    
    def update_screen(self, keys=None):
        keys=pygame.key.get_pressed()
        # if self.state == Game_State.START:
        #     BLACK = (0, 0, 0)

        #     current_time=time.time()
        #     random.seed(current_time)
        #     self.update_offsets()
        #     self.screen.fill(BLACK)
        #     self.draw_maze()
        #     self.draw_hud()
        #     for setan in self.Ghost:
        #         # print("ss")
        #         if isinstance(setan,Entity.Dumb_Ghost):
        #             setan.control(current_time)
        #         else:
        #             setan.control(current_time, self.Player)
                
        #         if setan.check_collision(self.Player):
        #             self.life -= 1
        #             if self.life == 0:
        #                 self.state = Game_State.GAME_OVER
        #                 self.game_over()
        #                 return
        #             else:
        #                 self.game_restart()
                
        #     for food in self.Food_Pellets:
        #         food.draw()
        #         if food.check_collision(self.Player):
        #             self.score += food.get_score()
        #             self.Food_Pellets.remove(food)
                    
        #     if not self.Food_Pellets:
        #         self.state = Game_State.WIN
        #         self.game_over()
        #         return
                    
        #     self.Player.move(keys, self.offset_x, self.offset_y)
        #     self.Player.draw(self.offset_x, self.offset_y)
        #     pygame.display.flip()
        # elif self.state == Game_State.GAME_OVER:
        #     self.game_over()
        #     print("Game Over")
        #     if keys[pygame.K_RETURN]:
        #         self.state = Game_State.END
        
    def run(self):
        # self.running = True
        print(self.state)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or self.state == Game_State.END:
                    print("End")
                    self.state = Game_State.START
                    self.running = False
                    return
                
            self.update_screen()
            # if self.state == Game_State.END:
            #     self.running = False
                
            # pygame.display.update()
            pygame.time.Clock().tick(30)

class Game_Controller(Level_Manager.Level , Game, Start_Menu, Progress.Account, Progress.Scoreboard, Progress.Achievement):
    def __init__(self, screen):
        Level_Manager.Level.__init__(self)
        Game.__init__(self, screen, 'user')
        Progress.Account.__init__(self)
        Progress.Scoreboard.__init__(self)
        Start_Menu.__init__(self, screen, Progress.Account, Progress.Scoreboard, Progress.Achievement)
        
        self.screen = screen
        self.state=Game_State.START
        
        # self.start_menu = None
        # self.level = None
        # self.game = None
        
        self.running = True
    
    def setup(self):
        # self.set_start_menu(Start_Menu(screen, Progress.Account, Progress.Scoreboard, Progress.Achievement))
        # self.set_game(Game(screen, 'user'))
        # self.set_level(Level_Manager.Level())
        pass
    
    def end(self):
        pass
        
    def run(self):
        # running = True
        while self.running:
            current_time=time.time()
            random.seed(current_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            result=None
            
            self.start_menu.handle_event(event)
            if self.start_menu.get_state() == Game_State.START:
                self.start_menu.start_menu()
                
            elif self.start_menu.get_state() == Game_State.MENU:
                self.start_menu.user_menu()
                
            elif self.start_menu.get_state() == Game_State.GAME_START:
                # print('Game Start')
                self.level.generate_level()
                self.game.initialize_game(self.level.get_level_data(), Entity.Player(screen), self.start_menu.get_difficulty())
                self.game.game_begin()
                self.start_menu.set_state(Game_State.START)
                self.game.run()
                self.level.reset_level()
                
            # elif self.start_menu.get_state() == Game_State.GAME:
            #     # print(self.start_menu.get_difficulty())
            #     self.start_menu.set_state(Game_State.START)
            #     self.game.run()
            #     self.level.reset_level()
                
            # self.game.handle_event(event)
            pygame.time.Clock().tick(30)

if __name__== '__main__':
    
    
    # Game = Game(screen, 'user')
    # level_node = Level_Manager.Level()
    game_controller = Game_Controller(screen)
    # game_controller.set_start_menu(Start_Menu(screen))
    # game_controller.set_game(Game)
    # game_controller.set_level(level_node)
    game_controller.run()