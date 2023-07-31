import pygame
import random
import asyncio
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()

# Fonts
game_font = pygame.font.Font(None,25)

# Graphics 
apple = pygame.image.load('Graphics/apple.png')
trophy = pygame.image.load('Graphics/trophy.png')

head_up = pygame.image.load('Graphics/head_up.png')
head_down = pygame.image.load('Graphics/head_down.png')
head_right = pygame.image.load('Graphics/head_right.png')
head_left = pygame.image.load('Graphics/head_left.png')

tail_up = pygame.image.load('Graphics/tail_up.png')
tail_down = pygame.image.load('Graphics/tail_down.png')
tail_right = pygame.image.load('Graphics/tail_right.png')
tail_left = pygame.image.load('Graphics/tail_left.png')

body_vertical = pygame.image.load('Graphics/body_vertical.png')
body_horizontal = pygame.image.load('Graphics/body_horizontal.png')

body_tr = pygame.image.load('Graphics/body_topright.png')
body_tl = pygame.image.load('Graphics/body_topleft.png')
body_br = pygame.image.load('Graphics/body_bottomright.png')
body_bl = pygame.image.load('Graphics/body_bottomleft.png')

# Sounds
crunch_sound = pygame.mixer.Sound('Sounds/Short_Bones.ogg')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 30
SPEED = 50
cell_number = 20 
cell_size = 30

class SnakeGameAI:

    def __init__(self, w=600, h=600):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        icon = pygame.image.load('Graphics/apple.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(1, ((self.w-BLOCK_SIZE )//BLOCK_SIZE)-1 )*BLOCK_SIZE
        y = random.randint(3, ((self.h-BLOCK_SIZE )//BLOCK_SIZE)-1 )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            crunch_sound.play()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > (self.w - BLOCK_SIZE)-30 or pt.x < 30 or pt.y > (self.h - BLOCK_SIZE)-30 or pt.y < 90:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill((175,215,70))

        game_outline_color = (76,153,0)
        for row in range (2,3):
            for col in range (cell_number):
                top_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.display, game_outline_color, top_outline_bar_rect)
        for row in range (cell_number-1, cell_number): 
            for col in range (cell_number):
                bot_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.display, game_outline_color, bot_outline_bar_rect)
        for row in range (3, cell_number-1): 
            for col in range(0,1): 
                left_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.display, game_outline_color, left_outline_bar_rect)
        for row in range (3, cell_number-1):
            for col in range (cell_number-1, cell_number):
                right_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.display, game_outline_color, right_outline_bar_rect)

        top_bar_color = (0, 102, 0)
        for row in range (0,2):
            for col in range(cell_number):
                top_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.display, top_bar_color, top_bar_rect)

        grass_color = (167, 209, 61)
        for row in range (3, cell_number-1):
            if row % 2 == 0: 
                for col in range (1, cell_number-1):
                    if col % 2 == 0: 
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(self.display, grass_color, grass_rect)
            else: 
                for col in range (1,cell_number-1):
                    if col % 2 != 0: 
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(self.display, grass_color, grass_rect
                        )

        #self.update_head_graphics()
        #self.update_tail_graphics()

        pt = self.head
        if self.direction == Direction.UP:
            snake_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            self.display.blit(head_up, snake_rect)
        elif self.direction == Direction.DOWN:
            snake_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            self.display.blit(head_down, snake_rect)
        elif self.direction == Direction.RIGHT: 
            snake_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            self.display.blit(head_right, snake_rect)
        else: 
            snake_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            self.display.blit(head_left, snake_rect)
        
        if self.previous_direction == Direction.UP and self.direction == Direction.UP:
                snake_body_rect = pygame.Rect((pt.x), (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_vertical, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x), (pt.y)+(2*BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_down, snake_tail_rect)
        elif self.previous_direction == Direction.UP and self.direction == Direction.LEFT: 
                snake_body_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_bl, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_down, snake_tail_rect)
        elif self.previous_direction == Direction.UP and self.direction == Direction.RIGHT: 
                snake_body_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_br, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_down, snake_tail_rect)

        if self.previous_direction == Direction.DOWN and self.direction == Direction.DOWN: 
                snake_body_rect = pygame.Rect((pt.x), (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_vertical, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x), (pt.y)-(2*BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_up, snake_tail_rect)
        elif self.previous_direction == Direction.DOWN and self.direction == Direction.LEFT: 
                snake_body_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_tl, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_up, snake_tail_rect)
        elif self.previous_direction == Direction.DOWN and self.direction == Direction.RIGHT: 
                snake_body_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_tr, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_up, snake_tail_rect)

        if self.previous_direction == Direction.RIGHT and self.direction == Direction.RIGHT: 
                snake_body_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_horizontal, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)-(2*BLOCK_SIZE), (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_left, snake_tail_rect)
        elif self.previous_direction == Direction.RIGHT and self.direction == Direction.UP: 
                snake_body_rect = pygame.Rect((pt.x), (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_tl, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_left, snake_tail_rect)
        elif self.previous_direction == Direction.RIGHT and self.direction == Direction.DOWN: 
                snake_body_rect = pygame.Rect((pt.x), (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_bl, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)-BLOCK_SIZE, (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_left, snake_tail_rect)
        
        if self.previous_direction == Direction.LEFT and self.direction == Direction.LEFT: 
                snake_body_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_horizontal, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)+(2*BLOCK_SIZE), (pt.y), BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_right, snake_tail_rect)
        elif self.previous_direction == Direction.LEFT and self.direction == Direction.UP: 
                snake_body_rect = pygame.Rect((pt.x), (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_tr, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y)+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_right, snake_tail_rect)
        elif self.previous_direction == Direction.LEFT and self.direction == Direction.DOWN: 
                snake_body_rect = pygame.Rect((pt.x), (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_br, snake_body_rect)
                #snake_tail_rect = pygame.Rect((pt.x)+BLOCK_SIZE, (pt.y)-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                #self.display.blit(tail_right, snake_tail_rect)


        for pt in self.snake[2:]:
            if self.previous_direction == Direction.UP or self.previous_direction == Direction.DOWN:
                snake_new_body_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_vertical, snake_new_body_rect)
            else: 
                snake_new_body_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
                self.display.blit(body_horizontal, snake_new_body_rect)

            #snake_rect = pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            #self.display.blit(body_horizontal, snake_rect)

            #pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            #pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        fruit_rect = pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE)
        self.display.blit(apple, fruit_rect)
        #pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        score_text = str(self.score)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size*cell_number-105)
        score_y = int(cell_size*cell_number-570)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 8, apple_rect.height)     

        pygame.draw.rect(self.display, (167,209,61), bg_rect)
        self.display.blit(score_surface, score_rect)
        self.display.blit(apple, apple_rect)
        pygame.draw.rect(self.display, (56,74,12), bg_rect, 2)   

        #text = font.render("Score: " + str(self.score), True, WHITE)
        #self.display.blit(text, [0, 0])

        if self.score > self.high_score:
            self.high_score = self.score
        high_score_text = str(self.high_score)
        high_score_surface = game_font.render(high_score_text, True, (56,74,12))
        high_score_x = int(cell_size*cell_number-30)
        high_score_y = int(cell_size*cell_number-570)
        high_score_rect = high_score_surface.get_rect(center = (high_score_x, high_score_y))
        trophy_rect = trophy.get_rect(midright = (high_score_rect.left, high_score_rect.centery))
        hs_rect = pygame.Rect(trophy_rect.left, trophy_rect.top, trophy_rect.width + high_score_rect.width + 8, trophy_rect.height)

        pygame.draw.rect(self.display, (167,209,61), hs_rect)
        self.display.blit(high_score_surface, high_score_rect)
        self.display.blit(trophy, trophy_rect)
        pygame.draw.rect(self.display, (56,74,12), hs_rect, 2) 

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.previous_direction = self.direction
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)