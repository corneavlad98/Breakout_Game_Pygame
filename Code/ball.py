import pygame
from random import randint
BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height,x_vel,y_vel):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        #self.velocity =[-1,1]
        self.velocity = [x_vel,y_vel]
        #self.velocity = [-5,4]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    def bounce(self):
        self.velocity[0] = self.velocity[0]
        self.velocity[1] = -self.velocity[1]
