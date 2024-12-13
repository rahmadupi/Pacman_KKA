import pygame
import sys
import os



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
pygame.display.set_caption("Pygame Sprite Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SHADOW_COLOR = (50, 50, 50)  # Dark gray for shadow

def get_image_surface(file_path):
    image = pygame.image.load(file_path).convert()
    # image_rect = image.get_rect()
    # image_surface = pygame.Surface((image_rect.width, image_rect.height))
    # image_surface.blit(image, image_rect)
    return image

class Player():
    def __init__(self):
        super().__init__()
        self.anim=None
        self.xpos=50
        self.ypos=50
        
        self.velx=0
        self.vely=0
        
        self.speed=5
        
        self.frame=1
        
        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        
        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = get_image_surface(
                os.path.join(os.getcwd(), "pacman/resources", "sprite", "pacman-l " + str(i) + ".gif"))
            self.anim_pacmanR[i] = get_image_surface(
                os.path.join(os.getcwd(), "pacman/resources", "sprite", "pacman-r " + str(i) + ".gif"))
            self.anim_pacmanU[i] = get_image_surface(
                os.path.join(os.getcwd(), "pacman/resources", "sprite", "pacman-u " + str(i) + ".gif"))
            self.anim_pacmanD[i] = get_image_surface(
                os.path.join(os.getcwd(), "pacman/resources", "sprite", "pacman-d " + str(i) + ".gif"))
            self.anim_pacmanS[i] = get_image_surface(os.path.join(os.getcwd(), "pacman/resources", "sprite", "pacman.gif"))
            

    def move(self, keys):
        self.xpos += self.velx
        self.ypos += self.vely
        if self.xpos < 0 :
            self.velx = 0
            self.xpos = 0
        if self.xpos > SCREEN_WIDTH - TILE_SIZE:
            self.velx = 0
            self.xpos = SCREEN_WIDTH - TILE_SIZE
        if self.ypos < 0:
            self.vely = 0
            self.ypos = 0
        if self.ypos > SCREEN_HEIGHT - TILE_SIZE:
            self.vely = 0
            self.ypos = SCREEN_HEIGHT - TILE_SIZE
            
        
        
        if keys[pygame.K_LEFT]:
            self.velx = -self.speed
            self.vely = 0
        if keys[pygame.K_RIGHT]:
            self.velx = self.speed
            self.vely = 0
        if keys[pygame.K_UP]:
            self.vely = -self.speed
            self.velx = 0
        if keys[pygame.K_DOWN]:
            self.vely = self.speed
            self.velx = 0
            
    def draw(self):
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
        
        screen.blit(self.anim[self.frame], (self.xpos, self.ypos))
        self.frame += 1
        if self.frame >= 9:
            self.frame = 1
        

# Create a sprite group and add the player sprite
# all_sprites = pygame.sprite.Group()
player = Player()
# all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)
    
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.draw()
    
    # pygame.display.flip()
    pygame.display.update()

    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()