import pgzrun
import random

WIDTH = 1000
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

PLAYER_IMG = "spaceship"
JUNK_IMG = "space junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"
BACKGROUND_LVL1 = "level 1"
BACKGROUND_LVL2 = "level 2"
BACKGROUND_LVL3 = "level 3"
BACKGROUND_TITLE = "Gamedev logo"
BACKGROUND_IMG = BACKGROUND_LVL1

JUNK_SPEED = 5
SATELLITE_SPEED = 3
DEBRIS_SPEED = 3
LASER_SPEED = 30

score = 0
junk_collected = 0
level = 0
level_screen = 0
lvl2_limit = 5
lvl3_limit = 20


def init():
    global player, junks, satellite, debris, lasers
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH - 15, HEIGHT/2)

    junks = []
    for i in range (5):
        junk = Actor(JUNK_IMG)
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(65, HEIGHT - junk.height)
        junk.topright = (x_pos, y_pos)
        junks.append(junk)

    satellite = Actor(SATELLITE_IMG)
    satellite.topright = (0, random.randint(65, HEIGHT - satellite.height))

    debris = Actor(DEBRIS_IMG)
    debris.topright = (0, random.randint(65, HEIGHT - satellite.height))

    lasers = []
    player.laserActive = 1  # add laserActive status to the player

    music.play("spacelife") #
    
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

init()
def update():
    global score, level, level_screen, BACKGROUND_IMG, junk_collected
    if junk_collected == lvl2_limit:
        level = 2
    if junk_collected == lvl3_limit:
        level = 3
        
    if level == -1: #instructions screen
        BACKGROUND_IMG = BACKGROUND_LVL1
        
    if score >= 0 and level >= 1:
        if level_screen == 1:
            BACKGROUND_IMG = BACKGROUND_LVL1
            if keyboard.RETURN == 1:
                level_screen = 2
           
        if level_screen == 2:
            playerUpdate()
            junkUpdate()

        if level == 2 and level_screen <= 3:
            BACKGROUND_IMG = BACKGROUND_LVL2
            level_screen = 3
            if keyboard.RETURN == 1:
                level_screen = 4
                #
                
        if level_screen == 4:
            satelliteUpdate()
            playerUpdate()
            junkUpdate()
            
        if level == 3 and level_screen <= 5:
            level_screen = 5
            BACKGROUND_IMG = BACKGROUND_LVL3
            if keyboard.RETURN == 1:
                level_screen = 6
                #

        if level_screen == 6:
            junkUpdate()
            playerUpdate()
            satelliteUpdate()
            debrisUpdate()
            laserUpdate()

    if score < 0 or level == -2:
        music.stop()
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = "level 1"
            score = 0
            junk_collected = 0
            level = 0
            init()
            music.play("spacelife")
            
def debrisUpdate():
    global score
    debris.x += DEBRIS_SPEED
    collision = player.colliderect(debris)

    if debris.left > WIDTH or collision == 1:
        debris.pos = (random.randint(-500, -50), random.randint(65, HEIGHT - debris.height))
    
    if collision == 1:
        score -= 10

def satelliteUpdate():
    global score
    satellite.x += SATELLITE_SPEED
    
    collision = player.colliderect(satellite)
    if satellite.left > WIDTH or collision == 1:
        satellite.left = random.randint(-500, -50)
        satellite.top = random.randint(65, HEIGHT - satellite.height)

    if collision == 1:
        score -= 5

def junkUpdate():
    global score, junk_collected
    for junk in junks:
        junk.x += JUNK_SPEED
        collision = player.colliderect(junk)
    
        if junk.left > WIDTH or collision == 1:
            junk.right = -10
            junk.top = random.randint(65, HEIGHT - junk.height)

        if collision == 1:
            score += 1
            junk_collected += 1
            sounds.collect_pep.play()

def playerUpdate():
    if keyboard.up == 1:
        player.y -= 5

    elif keyboard.down == 1:
        player.y += 5

    if player.top < 65:
        player.top = 65

    if player.bottom >= 590:
        player.bottom = 590

    if keyboard.space == 1 and level >= 2:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)
        
def draw():
    global BACKGROUND_IMG
    screen.clear()
    screen.blit(BACKGROUND_IMG,(0,0))
    if level == -1:
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\nPress SPACEBAR to fire lasers\n\nThe goal is to destroy bad satellites with lasers before\nthey reach the end of the screen while collecting debris\n\nMake sure not to hurt the good satellites!\n\nGOOD LUCK! :)"
        screen.draw.text(show_instructions, midtop = (WIDTH/2, 70), fontsize = 35, color = WHITE)
    if level == 0:
        start_button.draw()
        instructions_button.draw()

    if level >= 1:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topright = (365, 15), fontsize = 35, color = WHITE)
        player.draw()
        for junk in junks:
            junk.draw()
        satellite.draw()
        debris.draw()
        for laser in lasers:
            laser.draw()
            
    if score < 0:
        game_over = "GAME OVER\nPress ENTER to play again"
        screen.draw.text(game_over,center = (WIDTH/2, HEIGHT/2), fontsize = 70, color = WHITE)

    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_level_title = "LEVEL" + str(level) + "\n Press ENTER to continue."
        screen.draw.text(show_level_title, center = (WIDTH/2, HEIGHT/2), fontsize = 70, color = WHITE)

    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft = (750, 25), fontsize = 35, color = WHITE)

    show_collect_value = "Junk : " + str(junk_collected)
    screen.draw.text(show_collect_value, topleft = (435, 25), fontsize = 35, color = WHITE)                                             

def laserUpdate():
    global score
    for laser in lasers:
        laser.x -= LASER_SPEED
        if laser.right < 0:
            lasers.remove(laser)
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            satellite.left = random.randint(-500, -50)
            satellite.top = random.randint(65, HEIGHT - satellite.height)
            score -= 5
            sounds.explosion.play()
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            debris.pos = (0, random.randint(65, HEIGHT - debris.height))
            score += 5
            sounds.explosion.play()

def on_mouse_down(pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1

    if instructions_button.collidepoint(pos):
        level = -1
        
def makeLaserActive():
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)
        sounds.laserfire02.play()
        lasers.append(laser)

pgzrun.go()
