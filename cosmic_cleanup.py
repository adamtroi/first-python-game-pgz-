# Intro to GameDev - main game file
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
BACKGROUND_LVL1 = "level 1"

player = Actor(PLAYER_IMG)
player.midright = (WIDTH - 15, HEIGHT/2)

junk = Actor(JUNK_IMG)
junk.pos = (0, random.randint(65, HEIGHT - junk.height))
JUNK_SPEED = 5

satellite = Actor(SATELLITE_IMG)
satellite.topright = (0, random.randint(65, HEIGHT - satellite.height))
SATELLITE_SPEED = 3

debris = Actor(DEBRIS_IMG)
debris.topright = (0, random.randint(65, HEIGHT - satellite.height))
DEBRIS_SPEED = 3

score = 0

junks = []
for i in range (5):
    junk = Actor(JUNK_IMG)
    x_pos = random.randint(-500, -50)
    y_pos = random.randint(65, HEIGHT - junk.height)
    junk.topright = (x_pos, y_pos)
    junks.append(junk)

def update():
    junkUpdate()
    playerUpdate()
    satelliteUpdate()
    debrisUpdate()
    laserUpdate()

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
    global score
    for junk in junks:
        junk.x += JUNK_SPEED
        collision = player.colliderect(junk)
    
        if junk.left > WIDTH or collision == 1:
            junk.right = -10
            junk.top = random.randint(65, HEIGHT - junk.height)

        if collision == 1:
            score += 1

def playerUpdate():
    if keyboard.up == 1:
        player.y -= 5

    elif keyboard.down == 1:
        player.y += 5

    if player.top < 65:
        player.top = 65

    if player.bottom >= 590:
        player.bottom = 590

    if keyboard.space == 1:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)
        
def draw():
    screen.clear()
    screen.blit(BACKGROUND_LVL1,(0,0))
    player.draw()
    for junk in junks:
        junk.draw()
    satellite.draw()
    debris.draw()
    for laser in lasers:
        laser.draw()

    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft = (750, 25), fontsize = 35, color = WHITE)

lasers = []
player.laserActive = 1  # add laserActive status to the player
LASER_SPEED = 30

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
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            debris.pos = (0, random.randint(65, HEIGHT - debris.height))
            score += 5
        if junk.colliderect(laser) == 1:
            lasers.remove(laser)
            junk.pos = (random.randint(-500, -50), random.randint(65, HEIGHT - junk.height))
            score += 1
            
def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list

pgzrun.go()
