import pygame
import time
from pygame.locals import *
import random

SIZE = 40
bg_color =(0,0,0)

class Apple:
   def __init__(self,parent_screen):
      self.parent_screen = parent_screen
      self.image= pygame.image.load("apple.jpg").convert()
      self.x = SIZE*3
      self.y = SIZE*3

   def drow(self):
      self.parent_screen.blit(self.image, (self.x, self.y))
      pygame.display.flip()

   def move(self):
      self.x = random.randint(1,25)*SIZE
      self.x = random.randint(1,19)*SIZE    
    


class Snake:
   def __init__(self, parent_screen, length):
      self.parent_screen = parent_screen 
      self.block = pygame.image.load("block.jpg").convert()
      self.lenght = length
      self.x = [SIZE]*length
      self.y = [SIZE]*length
      self.direction = 'down'

   
   def increase_length(self):
      self.lenght +=1
      self.x.append (-1)
      self.y.append (-1)

   def move_up(self):
      self.direction = 'up'

   def move_down(self):
      self.direction = 'down'   

   def move_left(self):
      self.direction = 'left'

   def move_right(self):
      self.direction = 'right'

   def drow(self):
      # self.parent_screen.fill(bg_color)

      for i in range(self.lenght):
          self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
          pygame.display.flip() 


   def walk(self):
      for i in range(self.lenght-1, 0, -1):
         self.x[i] = self.x[i-1]
         self.y[i] = self.y[i-1]
      
      if self.direction == 'left':
         self.x[0] -= SIZE

      elif self.direction == 'right':
         self.x[0] += SIZE

      elif self.direction == 'up':
         self.y[0] -= SIZE

      elif self.direction == 'down':
         self.y[0] += SIZE   

      self.drow()   


class Game:
   def __init__(self):
      pygame.init()
      pygame.mixer.init()
      self.play_bf_music()
      self.surface = pygame.display.set_mode((1000,800))
      self.surface.fill((52, 235, 195))
      self.snake = Snake(self.surface, 2)
      self.snake.drow()
      self.apple =Apple(self.surface)
      self.apple.drow()

   def render_background(self):
      bg = pygame.image.load("background.jpg")
      self.surface.blit(bg,(0,0))
 

   def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.drow()
        self.display_score()
        pygame.display.flip()

        # for i in range(self.snake.lenght): 
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
              sound = pygame.mixer.Sound("ding.mp3")
              pygame.mixer.Sound.play(sound)
              self.snake.increase_length()
              self.apple.move()


        for i in range (2, self.snake.lenght):
           if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
              sound = pygame.mixer.Sound("crash.mp3")
              pygame.mixer.Sound.play(sound)
              raise "Game Over"
           
        

   def display_score(self):
      font = pygame.font.SysFont('arial', 30)
      score = font.render(f"Score: {self.snake.lenght}", True, (255,255,255)) 
      self.surface.blit(score,(850,10))  

   def play_bf_music(self):
     pygame.mixer.music.load("bg_music_1.mp3")       
     pygame.mixer.music.play(-1,0)
   
   def show_game_over(self):
      self.surface.fill(bg_color)
      font = pygame.font.SysFont('arial', 35)
      line1 = font.render(f"😢 Game Is Over 😢 Your Score Is : {self.snake.lenght}", True, (255,255,255)) 
      self.surface.blit(line1, (200, 300))

      line2 = font.render("To Play Again Press Enter. 🪱 To Exit Press Escape..", True, (255,255,255)) 
      self.surface.blit(line2, (200, 350))
      pygame.display.flip()
      pygame.mixer.music.pause()

   def is_collision(self, x1,y1,x2,y2):
      if x1 >= x2 and x1 < x2 + SIZE:
         if y1 >= y2 and y1 <y2 + SIZE:
            return True
      return False   
          
   def reset(self):
      self.snake = Snake(self.surface, 1)   
      self.apple =Apple(self.surface) 
              
   

   def run(self):
     running = True
     pause = False

     while running:
        for event in pygame.event.get():
          if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              running = False

            if event.key == K_RETURN:
               pygame.mixer.music.unpause()
               pause = False 

            if not pause:         
              if event.key == K_UP:
                  self.snake.move_up()
                
              if event.key == K_DOWN:
                  self.snake.move_down()

              if event.key == K_LEFT:
                  self.snake.move_left()

              if event.key == K_RIGHT:
                  self.snake.move_right()

          elif event.type == QUIT:
            running = False
        
        try:
          if not pause:
              self.play()

        except Exception as e:
            self.show_game_over()
            pause = True
            self.reset()


        
        time.sleep(0.2) 
 

if __name__ == "__main__":
  game = Game()
  game.run()
 

  
 
