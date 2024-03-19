import pygame
import time
import random

# FONT INITIALIZATION --------------------------------------------------------------------------------
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 30)

# WINDOW SETUP ---------------------------------------------------------------------------------------
WIDTH = 900
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame 1")

BG = pygame.image.load("Background.png")
# Could use the line below this to load the background image too if it was not to scale
# BG = pygame.transform.scale(pygame.image.load("Background.jpg"), (WIDTH, HEIGHT))

# CHARACTER SETUP ------------------------------------------------------------------------------------
PLAYER_HEIGHT = 60
PLAYER_WIDTH = 40
PLAYER_VELOCITY = 5

# PROJECTILE SETUP -----------------------------------------------------------------------------------
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VELOCITY = 3

# DRAWING --------------------------------------------------------------------------------------------
def draw(player, elapsed_time, stars):
    # blit is a special command that allows you to draw on the surface of the window (x, y) down from top left.
    WIN.blit(BG, (0,0))

    # draw character onto screen (can also use RGB for colour, ex. (255, 0, 0))
    pygame.draw.rect(WIN, "red", player)

    # print the time onto the screen in the top left
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    WIN.blit(time_text, (30, 10))

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

# MAIN GAME LOOP -------------------------------------------------------------------------------------
def main():
    run = True
    
    # Player instantiation
    player = pygame.Rect(WIDTH/2, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    # Clock instantiation and timer variables
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # Set projectile launch increments and store projectiles
    star_add_increment = 2000
    star_count = 0
    stars = []

    # Monitors collisions with player
    hit = False

    while run:
        # Fix clock speed so that the loop only runs every so often (slows character movement)
        star_count += clock.tick(60)

        # Get the elapsed time to pass to draw
        elapsed_time = time.time() - start_time

        # Add projectiles to the array iteratively
        if star_count > star_add_increment:
            for _ in range(3):                                                      # _ is a placeholder
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)   # use - STAR_HEIGHT so the appearing animation happens offscreen
                stars.append(star)
            
            # Speeds up how fast projectiles are entering the game as time elapses
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():

            # On a quit command (X in top right), we exit the program
            if event.type == pygame.QUIT:
                run = False
                break
        
        # Account for user key presses, subtract/add from x axis with boundary control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        # Move projectiles and check for collisions (in this case, projectile removed)
        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        # Handles loss case, displaying a loss message and then an exit of the application
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Call our draw function to update the screen
        draw(player, elapsed_time, stars)

    pygame.quit()

# Makes sure that we are directly running python file. Prevents imports from other python files from starting the game.
if __name__ == "__main__":
    main()
