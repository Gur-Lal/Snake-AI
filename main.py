import pygame,sys,random,time, gradio as gr
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics/body_topright.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_topleft.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_bottomright.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bottomleft.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sounds/Short_Bones.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index+1]-block
                next_block = self.body[index-1]-block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down 

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down 

    def move_snake(self):
        if self.new_block == True: 
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    def add_block(self):
        self.new_block = True
 
    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.x = random.randint(1, cell_number - 2)
        self.y = random.randint(3, cell_number - 2)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
    
    def randomize(self):
        self.x = random.randint(1, cell_number - 2)
        self.y = random.randint(3, cell_number - 2)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.high_score = 0 
        self.score = 0
        self.reset_block = False

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_top_bar()
        self.draw_game_outline()
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_high_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 1 <= self.snake.body[0].x < cell_number-1 or not 3 <= self.snake.body[0].y < cell_number-1:
            self.game_over()
            self.fruit.randomize()  

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()   
                if self.reset_block == False: 
                    self.fruit.randomize() 
                    self.reset_block = True
    
    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range (3,cell_number-1):
            if row % 2 == 0:
                for col in range (1,cell_number-1):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range (1,cell_number-1):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_top_bar(self):
        top_bar_color = (0, 102, 0)
        for row in range (0,2): 
            for col in range (cell_number):
                top_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, top_bar_color, top_bar_rect)

    def draw_game_outline(self):
        game_outline_color = (76,153,0)
        for row in range (2,3):
            for col in range (cell_number):
                top_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, game_outline_color, top_outline_bar_rect)
        for row in range (cell_number-1,cell_number):
            for col in range (cell_number):
                bot_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, game_outline_color, bot_outline_bar_rect)
        for row in range (3, cell_number-1):
            for col in range(0,1): 
                left_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, game_outline_color, left_outline_bar_rect)
        for row in range (3, cell_number-1):
            for col in range(cell_number-1,cell_number): 
                right_outline_bar_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, game_outline_color, right_outline_bar_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size*cell_number - 105)
        score_y = int(cell_size*cell_number - 570)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 8, apple_rect.height)

        pygame.draw.rect(screen, (167,209,61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)  

    def draw_high_score(self):
        if len(self.snake.body)-3 > self.high_score:
            self.high_score = len(self.snake.body)-3
        high_score_text = str(self.high_score)
        high_score_surface = game_font.render(high_score_text,True,(56,74,12))
        high_score_x = int(cell_size*cell_number - 30)
        high_score_y = int(cell_size*cell_number - 570)
        high_score_rect = high_score_surface.get_rect(center = (high_score_x, high_score_y))
        trophy_rect = trophy.get_rect(midright = (high_score_rect.left,high_score_rect.centery))
        hs_rect = pygame.Rect(trophy_rect.left, trophy_rect.top, trophy_rect.width + high_score_rect.width + 8, trophy_rect.height)

        pygame.draw.rect(screen, (167,209,61), hs_rect)
        screen.blit(high_score_surface, high_score_rect)
        screen.blit(trophy, trophy_rect)
        pygame.draw.rect(screen, (56,74,12), hs_rect, 2)  

pygame.display.set_caption("Snake")
icon = pygame.image.load('Graphics/apple.png')  
pygame.display.set_icon(icon)
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 30
cell_number =20
t0=time.time()
delay_time = 0.05
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
trophy = pygame.image.load('Graphics/trophy.png').convert_alpha()
game_font = pygame.font.Font(None,25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)

main_game = MAIN()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    if time.time()-t0 >= delay_time:
                        main_game.snake.direction = Vector2(0, -1)
                        t0=time.time()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    if time.time()-t0 >= delay_time:
                        main_game.snake.direction = Vector2(0, 1)
                        t0=time.time()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    if time.time()-t0 >= delay_time:
                        main_game.snake.direction =  Vector2(1, 0)
                        t0=time.time()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    if time.time()-t0 >= delay_time:
                        main_game.snake.direction = Vector2(-1, 0)
                        t0=time.time()

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(100)