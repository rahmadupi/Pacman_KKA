"""
Object.py

This file contains the classes for the objects in the game.
"""

from Game_Controller import *
TILE_SIZE = 20

# =============================================================================
# Abstract
class object_wall:
    pass

class object_food:
    pass
# =============================================================================

# =============================================================================
# Child
class Pellet_Food(object_food):
    def __init__(self,screen, x, y):
        self.score = 100
        self.screen = screen 
        self.x = x * TILE_SIZE + TILE_SIZE//2
        self.y = y * TILE_SIZE + TILE_SIZE//2
        self.radius = 2
        # print(x, y)
        
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        food_color = (255, 255, 0)  # Yellow color for food pellets
        pygame.draw.circle(self.screen, food_color, (self.x, self.y), self.radius)
    
    def get_score(self):
        return self.score
    
    # def check_collision(self,player):
    #     distance = ((self.x - player.xpos) ** 2 + (self.y - player.ypos) ** 2) ** 0.5
    #     return distance < (self.radius + 12)
    def check_collision(self, player):
        return self.x//TILE_SIZE == player.xpos//TILE_SIZE and self.y//TILE_SIZE == player.ypos//TILE_SIZE

class Strawberry_Food(object_food):
    # extra score 1500
    
    pass

class Blueberry_Food(object_food):
    # power up ghost killer
    # extra score 500
    pass

class Banana_Food(object_food):
    # power up ghost hunter (banish ghost(randomly)) # ghost house if there is one
    # extra score 500
    pass

class Apple_Food(object_food):
    # power up invicibility
    # extra score 500
    pass

class Orange_Food(object_food):
    # power up speed 25%
    # extra score 500
    pass

class Poison_Food(object_food):
    # nerf speed 25%
    # score -1000
    pass
# =============================================================================