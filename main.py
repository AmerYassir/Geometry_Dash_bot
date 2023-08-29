import pygame


# IMPORTANT. Initializes all of Pygame's modules
pygame.init()

# Set the size, title, and fps of the game
# The display.set_mode() function creates a new Surface object that represents the actual displayed graphics
# Any drawing you do to this Surface will become visible on the monitor
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 768, 494
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash")

# Create an object to help track time
CLOCK = pygame.time.Clock()

# Each game object is displayed on a 'surface'
# The method image.load loads an image to place on a surface
# Don't worry too much about the 'convert' method. Just note that it's necessary if you want to get any kind of speed out of your blits
ground_image = pygame.image.load("./grounds/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

player = pygame.image.load("./player/player.png").convert_alpha()
player_width = player.get_width()
player_height = player.get_height()
player_ground_offset = 10
player_x_position = 10 + player_width
player_y_position = SCREEN_HEIGHT - (ground_height + player_height + player_ground_offset) + player_height
player_rect = player.get_rect(center=(player_x_position, player_y_position))

# Initialize the required variables that control the position of some objects
MOVE_SPEED = 4
scroll = 0

jumping = False
Y_GRAVITY = 3.2
JUMP_HEIGHT = 32
Y_VELOCITY = JUMP_HEIGHT

# Create multiple backgrounds that stack on top of each other to create a parallax effect
backgrounds = []
for i in range(1, 6):
    image = pygame.image.load(f"./backgrounds/plx-{i}.png").convert_alpha()
    backgrounds.append(image)

backgrounds_width = backgrounds[0].get_width()


# Draws the background and creates a parallax effect
def draw_background():
    for parallax_factor in range(50):
        speed = 1
        for i in backgrounds:
            SCREEN.blit(i, ((parallax_factor * backgrounds_width) - scroll * speed, 0))
            speed += 0.2


# Draws the ground and repeats it to stay consistent with the parallax effect
def draw_ground():
    for parallax_factor in range(120):
        SCREEN.blit(
            ground_image,
            (
                (parallax_factor * ground_width) - scroll * 2.5,
                SCREEN_HEIGHT - ground_height,
            ),
        )


# GRAVITY = 0.5
# player_speed = 5
# player_x, player_y = 200, 200

# The game loop (where all the magic happens)
run = True
while run:
    # Update the clock (Compute how many milliseconds have passed since the previous call)
    # If you pass the optional framerate argument the function will delay to keep the game running slower than the given ticks per second
    # That means: clock.tick(60) == FPS <= 60
    CLOCK.tick(FPS)

    # 'blit' stands for 'block image transfer', which is a fancy way of saying 'put one surface on another surface'
    # The most important parameters are the surface, and the position
    draw_background()
    draw_ground()

    # Check for user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        jumping = True

    # Update the required variables that control the position of some objects
    scroll += MOVE_SPEED

    # Basic jumping logic
    # Very easy to understand
    # (I don't understand it, I got it from youtube)
    if jumping:
        player_y_position -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY

        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
    
    player_rect = player.get_rect(center=(player_x_position, player_y_position))
    SCREEN.blit(player, player_rect)

    # Event handlers
    for event in pygame.event.get():
        # pygame.QUIT means any way of closing the window
        if event.type == pygame.QUIT:
            run = False

    # Update the full display Surface to the screen
    # Note: You can use pygame.display.update() to update portions of the screen by passing the desired coordinates
    pygame.display.flip()

# Deactivate all of Pygame's modules
pygame.quit()
