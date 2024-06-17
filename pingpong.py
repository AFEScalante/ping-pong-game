import os
import sys
import pygame

pygame.init()

screen_x, screen_y = 600, 350
screen = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption("Ping-Pong")

# Music effects
intro_sound = pygame.mixer.Sound("audio/intro.wav")
intro_sound.set_volume(0.7)
intro_sound.play()
hit_sound = pygame.mixer.Sound("audio/hit.wav")

# Initial screen
font_path = 'font/Pixeltype.ttf'
font_title = pygame.font.Font(font_path, 60)
font_intro = pygame.font.Font(font_path, 30)
title_surf = font_title.render("Ping-Pong", False, "#415a77")
title_rect = title_surf.get_rect(center = (300, 150))
intro_surf = font_intro.render("Presiona espacio tecla para empezar", True, "#e0e1dd")
intro_rect = intro_surf.get_rect(center = (300, 250))

BALL_ACCELERATION = 5
BALL_RADIUS = 10

start_time = 0

def collision_right(rect1, rect2):
    if rect1.colliderect(rect2):
        if rect1.right >= rect2.left and rect1.left < rect2.left:
            return True
    return False

# Element classes
class Player():
  def __init__(self):
    self.x = 20
    self.y = 200
    self.width = 15
    self.height = 90
    self.vel = 10
    
  def draw(self):
    pygame.draw.rect(screen, "#1b263b", (self.x, self.y, self.width, self.height))
    
  def move(self, keys):
    if keys[pygame.K_UP] and self.y > 0: 
      self.y += -self.vel

    if keys[pygame.K_DOWN] and self.y < screen_y - self.height: 
      self.y += self.vel


class Ball():
  def __init__(self):
    self.x = 400
    self.y = 200
    self.x_vel = BALL_ACCELERATION
    self.y_vel = BALL_ACCELERATION
    self.rad = BALL_RADIUS
    
  def draw(self):
    pygame.draw.circle(screen, "#e0e1dd", (self.x, self.y), 10)
  
  def move(self):
    self.x += self.x_vel
    self.y += self.y_vel

    if self.x >= screen_x - self.rad:
      self.x_vel = -self.x_vel

    if self.y >= screen_y - self.rad or self.y <= self.rad:
      self.y_vel = -self.y_vel
      
  def bounce(self):
    hit_sound.play()
    self.x_vel = -self.x_vel

clock = pygame.time.Clock()

def game():
  ball = Ball()
  player = Player()  
  game_active = False
  score = 0

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
        
      if game_active == False:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          game_active = True
          score = 0
          ball.x_vel = BALL_ACCELERATION
          ball.y_vel = BALL_ACCELERATION
          start_time = pygame.time.get_ticks() / 1000
    
    if game_active:
      screen.fill("#778da9")

      ball.move()
      keys = pygame.key.get_pressed()
      player.move(keys=keys)

      player.draw()
      ball.draw()
      
      player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
      ball_rect = pygame.Rect(ball.x, ball.y, ball.rad, ball.rad)

      if collision_right(player_rect, ball_rect):
        ball.bounce()
        score += 1
      
      if ball.x < ball.rad:
        game_active = False
        
      score_surf = font_title.render(str(score), False, "#415a77")
      score_rect = score_surf.get_rect(center = (300, 300))
      screen.blit(score_surf, score_rect)
      
      # Increase ball speed each 5 seconds
      if int((pygame.time.get_ticks()) / 1000 - start_time) % 5 == 0:
        ball.x_vel = ball.x_vel * 1.001
        ball.y_vel = ball.y_vel * 1.001

    else:
      # Reset positions
      ball.x = 400
      ball.y = 200
      player.x = 20
      player.y = 200
      
      # Reset score
      ball.x_vel = 5
      ball.y_vel = 5

      screen.fill("#778da9")
      screen.blit(title_surf, title_rect)
      
      if score == 0:
        screen.blit(intro_surf, intro_rect)
      else:
        intro_score_surf = font_intro.render(f"Tu puntaje: {score}", True, "#e0e1dd")
        intro_score_rect = intro_score_surf.get_rect(center = (300, 250))
        intro_text_surf = font_intro.render(f"Oprime cualquier tecla para continuar", True, "#e0e1dd")
        intro_text_rect = intro_text_surf.get_rect(center = (300, 280))
        screen.blit(intro_text_surf, intro_text_rect)
        screen.blit(intro_score_surf, intro_score_rect)

    pygame.display.update()
    clock.tick(60)

game()