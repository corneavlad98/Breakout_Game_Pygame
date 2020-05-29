# Import the pygame library and initialise the game engine
import pygame
# Let's import the Paddle Class & Ball Class
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

# Define some colors
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Main menu
# This screen will be seen by the player when entering the game
# It includes a PLAY button, QUIT button and a fancy name animation above them
def game_intro():
    frames_count = 0
    intro = True
    y = 245
    color = RED
    while intro:
        frames_count += 1
        if frames_count == 40:
            if color == RED:
                color = ORANGE
            elif color == ORANGE:
                color = GREEN
            else:
                color = RED
            frames_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #Initialize joystick as first joystick (only one connected)                               
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        exit_button = joystick.get_button(9) #OPTIONS button on PS4 controller
        #if user pressed OPTIONS button, terminate the program
        if exit_button == 1:
            pygame.quit()
            quit()
        
        screen.fill(DARKBLUE)

        font = pygame.font.SysFont("Georgia", 120, True)
        buttonFont = pygame.font.SysFont("Georgia", 70, True)

        text = font.render("Arkanoid", True, color)
        playText = buttonFont.render("Play", True, BLACK)
        quitText = buttonFont.render("Quit", True, BLACK)

        screen.blit(text, (100, 60))

        selectRect = pygame.Rect(245, y, 310, 90)
        pygame.draw.rect(screen, WHITE, selectRect)

        playButton = pygame.draw.rect(screen, GREEN, (250, 250, 300, 80))
        screen.blit(playText, (320, 245))
        quitButton = pygame.draw.rect(screen, YELLOW, (250, 340, 300, 80))
        screen.blit(quitText, (320, 335))


        hat=joystick.get_hat(0)                 #DPad buttons on PS4 controller
        select_button = joystick.get_button(1)  #X button on PS4 controller
            
        if hat[1] == 1:   #if we press Up-DPad, we go up with select rectangle            
            y = 245    
        if hat[1] == -1:  #if we press Down-Dpad, we go down with select rectangle
            y = 335          
        #if X button is pressed   
        if select_button == 1:
            if y == 245:
                intro = False   #if select rectangle is first, exit 'intro' and start the game
            elif y == 335:      #if select rectangle is second, terminate the program
                 pygame.quit()              
                 quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y = 245
        if keys[pygame.K_DOWN]:
            y = 335
        if keys[pygame.K_RETURN]:
            if y == 245:
                intro = False
            elif y == 335:
                quit()

        pygame.display.update()
        clock.tick(60)

#The actual game
while True:
    game_intro()
    score = 0
    lives = 3

    #Initialize joystick as first joystick (only one connected)                               
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    # Create the Paddle
    paddle = Paddle(LIGHTBLUE, 150, 10,size[0])
    paddle.rect.x = 350
    paddle.rect.y = 560

    # Create the Ball
    ball = Ball(WHITE, 20, 20,-5,4)
    ball.rect.x = 345
    ball.rect.y = 195

    # Create the Bricks
    all_bricks = pygame.sprite.Group()
    for i in range(7):
        brick = Brick(RED, 80, 30, 3)
        brick.rect.x = 60 + i * 100
        brick.rect.y = 60
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    for i in range(7):
        brick = Brick(ORANGE, 80, 30, 2)
        brick.rect.x = 60 + i * 100
        brick.rect.y = 100
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    for i in range(7):
        brick = Brick(YELLOW, 80, 30, 1)
        brick.rect.x = 60 + i * 100
        brick.rect.y = 140
        all_sprites_list.add(brick)
        all_bricks.add(brick)

    # Add the paddle & ball to the list of sprites
    all_sprites_list.add(paddle)
    all_sprites_list.add(ball)

    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True

    # -------- Main Program Loop -----------
    while carryOn:       
        # For using a joystick connected via USB; initialize the joystick and exit program when a certain button is pressed
        # We used a PS4 controller for this game, but any controller with an analog stick should work if configured correctly
        
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        exit_button = joystick.get_button(8)
        if exit_button == 1:            
            carryOn = False
    
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT: 
                carryOn = False             # If user clicked close, close the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: 
                    carryOn = False         # If user pressed the X button, close the game
                if event.key == pygame.K_SPACE: 
                    while True:
                        event = pygame.event.wait() #If user pressed the SPACE button, pause the game
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                break  # Exit infinite loop, unpause the game when pressing SPACE
                            if event.key == pygame.K_x:
                                carryOn = False  # Exit game
                                break
            
        # Same thing as above, but for joystick buttons
        
            elif event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(9):                 
                    while True:                        
                        event = pygame.event.wait()
                        if event.type == pygame.JOYBUTTONDOWN:
                            if joystick.get_button(9):                            
                                break
                            if joystick.get_button(8):                             
                                carryOn = False
                                break
        
        """
        # We use an analog stick on the controller, so we need information about it's X axis
        # The values read from the stick are between -1.000 and 1.000 (left and right)
        
        axis = joystick.get_axis(0)
        axis_rounded = round(axis, 2) #we used only 2 decimals from the value
        
        # Moving the paddle with the left analog stick
        if axis_rounded < -0.1:            
            paddle.moveLeft(-15 * axis_rounded) # we used a formula to set how many pixels the paddle moves per axis value(rule of three)
        if axis_rounded > 0.1:            
            paddle.moveRight(15 * axis_rounded)
        """
        
        # Moving the paddle when the use uses the arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(10)
        if keys[pygame.K_RIGHT]:
            paddle.moveRight(10)


        # Moving the paddle when we press the DPad Keys; alternative to using the stick
        hat=joystick.get_hat(0)
        if hat[0] == -1:            
            paddle.moveLeft(10)
        if hat[0] == 1:            
            paddle.moveRight(10)    

        # --- Game logic should go here
        all_sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= 780:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > 580:
            ball.velocity[1] = -ball.velocity[1]
            lives -= 1
            if lives == 0:
                # Display GAME OVER Message for 3 seconds
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER", 1, WHITE)
                screen.blit(text, (250, 300))
                pygame.display.flip()
                pygame.time.wait(3000)

                # Stop the Game
                carryOn = False
        if ball.rect.y < 40:
            ball.velocity[1] = -ball.velocity[1]

        # Detect collisions between the ball and the paddle
        if pygame.sprite.collide_mask(ball, paddle):
            ball.rect.x -= ball.velocity[0]
            ball.rect.y -= ball.velocity[1]
            ball.bounce()

        # Check if there is a brick collision
        brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
        for brick in brick_collision_list:
            ball.bounce()
            score += brick.hurt()
            if len(all_bricks) == 0:
                # Display LEVEL COMPLETE Message for 3 seconds
                font = pygame.font.Font(None, 74)
                text = font.render("LEVEL COMPLETE", 1, WHITE)
                screen.blit(text, (200, 300))
                pygame.display.flip()
                pygame.time.wait(3000)

                # Stop the game
                carryOn = False

        # --- Drawing code should go here
        # First, clear the screen to dark blue.
        screen.fill(DARKBLUE)
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        # Display the score and the number of lives at the top of the screen
        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20, 10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650, 10))

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
