import pygame
import sys
import random


def ball_animation():
	global ball_speed_x, ball_speed_y, opponent_score, player_score, score_time
	# Moving the ball
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	# Boundaries
	if ball.top <= 0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(bounce_sound)
		ball_speed_y *= -1
	if ball.left <= 0 or ball.right >= screen_width:
		if ball.left <= 0:
			pygame.mixer.Sound.play(score_sound)
			opponent_score += 1
		else:
			pygame.mixer.Sound.play(score_sound)
			player_score += 1
		score_time = pygame.time.get_ticks()

	# Player Collisions
	if ball.colliderect(player) and ball_speed_x < 0:
		pygame.mixer.Sound.play(bounce_sound)
		if abs(ball.left - player.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and (ball_speed_y > 0):
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and (ball_speed_y < 0):
			ball_speed_y *= -1
	if ball.colliderect(opponent) and ball_speed_x > 0:
		pygame.mixer.Sound.play(bounce_sound)
		if abs(ball.right - opponent.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10 and (ball_speed_y > 0):
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and (ball_speed_y < 0):
			ball_speed_y *= -1


def ball_restart():
	global ball_speed_y, ball_speed_x, score_time
	ball_speed = 7

	current_time = pygame.time.get_ticks()
	ball.center = (screen_width / 2, screen_height / 2)

	# Loading countdown
	if current_time - score_time < 700:
		num_three = game_font.render("...", False, entity_color)
		screen.blit(num_three, (screen_width / 2 - 14, screen_height/2))
	elif 700 < current_time - score_time < 1400:
		num_two = game_font.render("..", False, entity_color)
		screen.blit(num_two, (screen_width / 2 - 14, screen_height/2))
	elif 1400 < current_time - score_time < 2100:
		num_one = game_font.render(".", False, entity_color)
		screen.blit(num_one, (screen_width / 2 - 14, screen_height/2))

	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0, 0
	else:
		ball_speed_y = ball_speed * random.choice((1, -1))
		ball_speed_x = ball_speed * random.choice((1, -1))
		score_time = None


def player_animation():
	player.y += player_speed
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height


def player_movement():
	global player_speed
	speed = 7
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_DOWN:
			player_speed += speed
		if event.key == pygame.K_UP:
			player_speed -= speed
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_DOWN:
			player_speed -= speed
		if event.key == pygame.K_UP:
			player_speed += speed


def opponent_ai():
	if opponent.centery < ball.y:
		opponent.centery += opponent_speed
	if opponent.centery > ball.y:
		opponent.centery -= opponent_speed
	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height


# SETUP
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up game window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Entities
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
opponent = pygame.Rect(screen_width-20, screen_height/2 - 100, 10, 200)
player = pygame.Rect(10, screen_height/2 - 100, 10, 200)

# Colors
bg_color = (31, 26, 56)
entity_color = (241, 240, 234)

# Movement
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
player_speed = 0
opponent_speed = 5

# Score Timer
score_time = True

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Sound
bounce_sound = pygame.mixer.Sound("sounds/jumping.ogg")
score_sound = pygame.mixer.Sound("sounds/pop-19.ogg")

# Main game loop
while True:
	# Handling input
	# Exiting the game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		player_movement()

	# Movement
	ball_animation()
	player_animation()
	opponent_ai()

	# Visuals
	screen.fill(bg_color)
	pygame.draw.rect(screen, entity_color, player)
	pygame.draw.rect(screen, entity_color, opponent)
	pygame.draw.ellipse(screen, entity_color, ball)
	pygame.draw.aaline(screen, entity_color, (screen_width/2, 0), (screen_width/2, screen_height))

	if score_time:
		ball_restart()

	# Score
	player_text = game_font.render(f"{player_score}", False, entity_color)
	screen.blit(player_text, (screen_width/2 - 40, 20))

	opponent_text = game_font.render(f"{opponent_score}", False, entity_color)
	screen.blit(opponent_text, (screen_width / 2 + 24, 20))
	# loading element
	# t = game_font.render("...", False, entity_color)
	# screen.blit(t, (screen_width / 2 - 16, screen_height/2))

	# Updating the window
	pygame.display.flip()
	clock.tick(60)
