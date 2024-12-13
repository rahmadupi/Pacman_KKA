import sys
import os
import pygame

def get_base_path():
    if getattr(sys, 'frozen', False):  # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()

sys.path.append(os.path.join(base_path, '../classes'))
sys.path.append(os.path.join(base_path, '../classes/Game'))
from Level import Maze_Generator

pygame.init()

# Tile dimensions
TILE_SIZE = 20
TILES_X = 21  # Number of tiles horizontally
TILES_Y = 21  # Number of tiles vertically

# Screen dimensions based on tiles
SCREEN_WIDTH = TILE_SIZE * TILES_X
SCREEN_HEIGHT = TILE_SIZE * TILES_Y

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Draw Test")

# Load tile images
def load_image(file_name):
    return pygame.image.load(os.path.join(base_path, file_name)).convert_alpha()

wall_image = load_image('wall-nub.gif')
# path_image = load_image('path.png')

class SmartMoveScreen:
    def __init__(self, screen, tile_size, maze_layout):
        self.screen = screen
        self.tile_size = tile_size
        self.maze_layout = maze_layout
        self.maze_width = len(maze_layout[0]) * tile_size
        self.maze_height = len(maze_layout) * tile_size
        self.player_x = 1  # Initial player position (tile coordinates)
        self.player_y = 1
        self.food_pellets = self.initialize_food_pellets()

    def initialize_food_pellets(self):
        food_pellets = []
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == ' ':
                    food_pellets.append((x, y))
        return food_pellets

    def draw_maze(self):
        for y, row in enumerate(self.maze_layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.screen.blit(wall_image, (x * self.tile_size + self.offset_x, y * self.tile_size + self.offset_y))
                # else:
                #     self.screen.blit(path_image, (x * self.tile_size + self.offset_x, y * self.tile_size + self.offset_y))

    def draw_food_pellets(self):
        food_color = (255, 255, 0)  # Yellow color for food pellets
        for pellet in self.food_pellets:
            pellet_rect = pygame.Rect(
                pellet[0] * self.tile_size + self.offset_x + self.tile_size // 4,
                pellet[1] * self.tile_size + self.offset_y + self.tile_size // 4,
                self.tile_size // 2,
                self.tile_size // 2
            )
            pygame.draw.rect(self.screen, food_color, pellet_rect)

    def draw_player(self):
        player_color = (255, 0, 0)  # Red color for the player
        player_rect = pygame.Rect(
            self.player_x * self.tile_size + self.offset_x,
            self.player_y * self.tile_size + self.offset_y,
            self.tile_size,
            self.tile_size
        )
        pygame.draw.rect(self.screen, player_color, player_rect)

    def move_player(self, dx, dy):
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if self.maze_layout[new_y][new_x] != '#':  # Check if the new position is not a wall
            self.player_x = new_x
            self.player_y = new_y
            self.check_food_collision()

    def check_food_collision(self):
        if (self.player_x, self.player_y) in self.food_pellets:
            self.food_pellets.remove((self.player_x, self.player_y))

    def update_screen(self):
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        self.update_offsets()
        self.draw_maze()
        self.draw_food_pellets()
        self.draw_player()
        pygame.display.flip()

    def update_offsets(self):
        # Calculate the offsets to center the player
        center_offset_x = SCREEN_WIDTH // 2 - self.player_x * self.tile_size
        center_offset_y = SCREEN_HEIGHT // 2 - self.player_y * self.tile_size

        # Ensure the maze stays within one tile from the edge of the window
        max_offset_x = TILE_SIZE
        min_offset_x = SCREEN_WIDTH - self.maze_width - TILE_SIZE
        max_offset_y = TILE_SIZE
        min_offset_y = SCREEN_HEIGHT - self.maze_height - TILE_SIZE

        self.offset_x = max(min(center_offset_x, max_offset_x), min_offset_x)
        self.offset_y = max(min(center_offset_y, max_offset_y), min_offset_y)

if __name__ == '__main__':
    Maze = Maze_Generator()
    Maze.generate_maze()
    maze_layout = Maze.get_maze()

    smart_move_screen = SmartMoveScreen(screen, TILE_SIZE, maze_layout)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    smart_move_screen.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    smart_move_screen.move_player(1, 0)
                elif event.key == pygame.K_UP:
                    smart_move_screen.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    smart_move_screen.move_player(0, 1)

        smart_move_screen.update_screen()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()