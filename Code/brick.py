import pygame
BLACK = (0,0,0)
 
class Brick(pygame.sprite.Sprite):
    #This class represents a brick. It derives from the "Sprite" class in Pygame.
    lives=0

    def __init__(self, color, width, height, lives):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.lives=lives
 
        # Pass in the color of the brick, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the brick (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def hurt(self):
        self.lives -= 1

        if self.lives == 0:
            self.kill()
            return 1

        return 0


