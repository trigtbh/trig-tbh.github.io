from pygame import *
 
player = Actor("player", (400, 550)) # Load in the player Actor image
 
def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    player.draw()
 
def update(): # Pygame Zero update function
    checkKeys()
 
def checkKeys():
    global player
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
pygame.pgzrun.go() 
