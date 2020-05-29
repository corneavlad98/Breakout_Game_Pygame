import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
import math
import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import digitalio
import board

#size of the SPI OLED Display
size = (128, 64)

#Create the SPI interface
spi = board.SPI()
reset_pin = digitalio.DigitalInOut(board.D4) #GPIO 4
cs_pin = digitalio.DigitalInOut(board.D5)    #not used
dc_pin = digitalio.DigitalInOut(board.D6)    #GPIO6

#Initialize the display with coresponding parameters
oled = adafruit_ssd1306.SSD1306_SPI(size[0], size[1], spi, dc_pin, reset_pin, cs_pin)

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main menu
# This screen will be seen by the player when entering the game
# It includes a PLAY and QUIT button
def game_intro():
    intro = True
    
    #clear display
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    
    #initial top-left y-coordonate of the select rectangle   
    y0=22
    
    #initial bottom-right y-coordonate of the select rectangle
    y1=32

    #Fonts used for title and buttons
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    buttonfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    
    while intro:
        #if user pressed the closed button (top-right corner), terminate the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                oled.fill(0)
                oled.show()
                quit()
                
        #Initialize joystick as first joystick (only one connected)                               
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        
        exit_button = joystick.get_button(9) #OPTIONS button on PS4 controller
        #if user pressed OPTIONS button, terminate the program
        if exit_button == 1:
            pygame.quit()
            oled.fill(0)
            oled.show()
            quit()

        #draw the title on the screen
        draw.text((30,0),"Arkanoid",font=font,fill=255)

        hat=joystick.get_hat(0)                 #DPad buttons on PS4 controller
        select_button = joystick.get_button(0)  #X button on PS4 controller
            
        if hat[1] == 1:   #if we press Up-DPad, we go up with select rectangle
            #fill down-select rectangle black, then fill up-select rectangle white
            draw.rectangle((36,42,92,52),outline=0,fill=0)    
            draw.rectangle((36,22,92,32),outline=0,fill=255)
            #change y-coordonates of the select rectangle (position of the white rectangle)
            y0 = 22
            y1 = 32
        if hat[1] == -1:  #if we press Down-Dpad, we go down with select rectangle
            #fill up-select rectangle black, then fill down-select rectangle 
            draw.rectangle((36,22,92,32),outline=0,fill=0)
            draw.rectangle((36,42,92,52),outline=0,fill=255)     
            #change y-coordonates of the select rectangle (position of the white rectangle)
            y0 = 42
            y1 = 52
        #if X button is pressed   
        if select_button == 1:
            if y0 == 22:
                intro = False   #if select rectangle is first, exit 'intro' and start the game
            elif y0 == 42:      #if select rectangle is second, terminate the program
                 pygame.quit()
                 oled.fill(0)
                 oled.show()
                 quit()

        draw.rectangle((38,24,90,30),outline=0,fill=0)     #black first button rectangle
        draw.text((55,23),"Play",font=buttonfont,fill=255) #draw text on the black rectangle
        
        draw.rectangle((38,44,90,50),outline=0,fill=0)     #black second button rectangle
        draw.text((55,42),"Quit",font=buttonfont,fill=255) #draw text on the black rectangle

        #Display the 'image' on the OLED                
        oled.image(image)

        oled.show()

#The actual game
while True:
    game_intro()
    score = 0
    lives = 3
    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()
    # Create the Paddle
    paddle = Paddle(WHITE, 35, 2,size[0])   #color, width, height, screen_width
    #starting position on the screen
    paddle.rect.x = 47
    paddle.rect.y = 60
    # Create the Ball
    ball = Ball(WHITE, 4, 4,-2,2)           #color, width, height, velocity.x,velocity.y
    ball.rect.x = 55
    ball.rect.y = 30
    # Create the Bricks
    all_bricks = pygame.sprite.Group()      #sprite group for all the bricks
    #row 1 of bricks
    for i in range(7):
        brick = Brick(WHITE, 12, 3)
        brick.rect.x = 10 + i * 15
        brick.rect.y = 9
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    #row 2 of bricks
    for i in range(7):
        brick = Brick(WHITE, 12, 3)
        brick.rect.x = 10 + i * 15
        brick.rect.y = 15
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    #row 3 of bricks
    for i in range(7):
        brick = Brick(WHITE, 12, 3)
        brick.rect.x = 10 + i * 15
        brick.rect.y = 21
        all_sprites_list.add(brick)
        all_bricks.add(brick)
    # Add the paddle & ball to the list of sprites
    all_sprites_list.add(paddle)
    all_sprites_list.add(ball)

    #clear the display
    oled.fill(0)
    oled.show()
    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True

    

    # ---------- Main Program Loop -------------
    while carryOn:       
        # For using a joystick connected via USB; initialize the joystick and exit program when a certain button is pressed
        # We used a PS4 controller for this game, but any controller should work if configured correctly

        #initialize the controller
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        exit_button = joystick.get_button(8)    
        if exit_button == 1:            
            carryOn = False                     #if user pressed SHARE button, exit game
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                carryOn = False             # If user clicked close, close the game
            elif event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(9):                 
                    while True:                        
                        event = pygame.event.wait()     #If user pressed OPTIONS, pause the game
                        if event.type == pygame.JOYBUTTONDOWN:
                            if joystick.get_button(9):                            
                                break                   #Exit infinite loop, unpause the game when pressing OPTIONS
                            if joystick.get_button(8):                             
                                carryOn = False         #Exit game when pressing SHARE button
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
        
        # Moving the paddle when we press the DPad Keys; alternative to using the stick
        hat=joystick.get_hat(0)
        if hat[0] == -1:            
            paddle.moveLeft(4)
        if hat[0] == 1:            
            paddle.moveRight(4)
        
        

        # ---------- Game logic should go here -----------
        all_sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x > 123:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x < 1:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > 60:
            ball.velocity[1] = -ball.velocity[1]
            lives -= 1
            if lives == 0:
                # Display GAME OVER Message for 3 seconds                           
                lose_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
                draw.text((20,25),"GAME OVER",font=lose_font,fill=255)
                
                oled.image(image)
                oled.show()
                pygame.time.wait(3000)
                # Stop the Game
                carryOn = False
                
        if ball.rect.y < 9:
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
                win_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
                draw.text((6,25),"LEVEL COMPLETE",font=win_font,fill=255)
                
                oled.image(image)
                oled.show()
                pygame.time.wait(3000)
                # Stop the game
                carryOn = False

                

        # ---------- Drawing code should go here --------------
        # First, create blank image for drawing.
        
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
                
        #draw a line to separate score from game
        draw.line((0,7,128,7),fill=255)
        

        # Display the score and the number of lives at the top of the screen
        score_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
        draw.text((0,0),"Score: " + str(score),font=score_font,fill=255)
        draw.text((98,0),"Lives: " + str(lives),font=score_font,fill=255)

        #draw paddle        
        draw.rectangle((paddle.rect.x,paddle.rect.y,paddle.rect.x+35,paddle.rect.y+2),outline=0,fill=255)
        
        #draw ball       
        draw.rectangle((ball.rect.x,ball.rect.y,ball.rect.x+4,ball.rect.y+4),outline=0,fill=255)
        
        #draw bricks
        for brick in all_bricks:
            draw.rectangle((brick.rect.x,brick.rect.y,brick.rect.x+12,brick.rect.y+3),outline=0,fill=255)   

        #Display the 'image' on the OLED       
        oled.image(image)
        oled.show()
     
# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
