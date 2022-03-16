import pygame
import random
import math
from pygame import mixer

#initialize a game

pygame.init()

#creating the screen

screen = pygame.display.set_mode((800,600))
#background

background = pygame.image.load('background.png')

#background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#Title and fevicon 
     
pygame.display.set_caption("Space Bomber")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

#Player

playership = pygame.image.load("spaceship.png")
enemyX = random.randint(0,735)
enemyY = random.randint(50,150) 
enemyX_change = 3
enemyY_change = 40

#enemy
enemyimg = []
enemyX =[]
enemyY =[]
enemyX_change =[]
enemyY_change =[]
no_of_enemy = 6
for i in range(no_of_enemy):
	enemyimg.append(pygame.image.load("alien.png"))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(3)
	enemyY_change.append(40)

enemyimg = pygame.image.load("alien.png") 
playerX = 370
playerY = 480
playerX_change = 0

#bullet
#fire : in motion 
#ready : not visible

bulletimg = pygame.image.load("missile.png") 
bulletX = 0
bulletY = 480 
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",19)

textX = 10
textY = 10

#game over
over_font = pygame.font.Font("freesansbold.ttf",64)


def game_over_text():
	over_text = over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(over_text,(200,250))



def score(x,y):
	score = font.render("Score:"+str(score_value),True,(255,255,255))
	screen.blit(score,(x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletimg,(x+16,y+10))
def collision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
	if distance <27:
		return True
	else:
		return False



def player(x,y):
	screen.blit(playership,(x,y))#blit means draw

def enemy(x,y,i):
	screen.blit(enemyimg,(x,y))#blit means draw






#Game loop
   
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#if keystroke is pressed check whteher its left or right

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -4
			if event.key == pygame.K_RIGHT:
				playerX_change = 4 
			if event.key == pygame.K_SPACE:
				bullet_sound = mixer.Sound("laser.wav")
				bullet_sound.play()
				if bullet_state is "ready":
					bulletX = playerX
					fire_bullet(playerX,bulletY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					playerX_change =0

	# RGB = red , green , blue

	screen.fill((0,0,0))

	#background img
	screen.blit(background,(0,0))

	#updating our player position

	playerX+=playerX_change
	if playerX<=0:
		playerX=0
	elif playerX>=736:
		playerX=736
#enemy movements
	for i in range(no_of_enemy):
		#Game over 
		if enemyY[i]>440:
			for j in range(no_of_enemy):
				enemyY[j] = 2000
			game_over_text()
			break
		enemyX[i]+=enemyX_change[i]
		if enemyX[i]<=0:
			enemyX_change[i]=3
			enemyY[i]+=enemyY_change[i]
		elif enemyX[i]>=736:
			enemyX_change[i]=-3
			enemyY[i]+=enemyY_change[i]
		#collision
		collision_occur = collision(enemyX[i],enemyY[i],bulletX,bulletY) 
		if collision_occur:
			explosion_sound = mixer.Sound("explosion.wav")
			explosion_sound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value+=1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)
		enemy(enemyX[i],enemyY[i],i)



	#bullet movement
	if bulletY<=0: 
		bulletY=480
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bulletX,bulletY)
		bulletY-=bulletY_change

	

	#infront of screen would be drawn

	player(playerX,playerY)
	score(textX,textY)

	pygame.display.update()
