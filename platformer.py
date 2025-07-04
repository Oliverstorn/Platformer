import pygame as pg
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

# Setup
pg.mixer.pre_init(44100, -16, 2, 512)

pg.init()

clock = pg.time.Clock()
fps = 60

# Setting the screen up
screen_widht = 1000
screen_height = 775
screen = pg.display.set_mode((screen_widht, screen_height))
pg.display.set_caption("Sankeformer")

#define 
font = pg.font.SysFont("Bauhaus 93", 55)
font_score = pg.font.SysFont("Bauhaus 93", 30)

# define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 5
score = 0

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)

#Load images
dirt_img = pg.image.load("img/dirt.png")
grass_img = pg.image.load("img/grass.png")
sun_img = pg.image.load("img/sun.png")
bg_img = pg.image.load("img/sky.png")
restart_img = pg.image.load("img/restart_btn.png")
start_img = pg.image.load("img/start_btn.png")
exit_img = pg.image.load("img/exit_btn.png")

#load sounds
pg.mixer.music.load("img/music.wav")
pg.mixer.music.play(-1, 0.0,5000)
coin_fx = pg.mixer.Sound("img/coin.wav")
coin_fx.set_volume(0.5)
jump_fx = pg.mixer.Sound("img/jumping.wav")
jump_fx.set_volume(0.5)
game_over_fx = pg.mixer.Sound("img/dead_sound.wav")
game_over_fx.set_volume(100)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function to reset level
def reset_level(level):
    player.reset(100, screen_height - 107)
    slot_group.empty()
    lava_group.empty()
    exit_group.empty()

    #load in level data and create world
    if path.exists(f"level{level}_data"):
        pickle_in = open(f"level{level}_data", "rb")
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pg.mouse.get_pos()

        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                
        
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
                
    
        #Draw button
        screen.blit(self.image, (self.rect))

        return action
    
class Player():
    def __init__(self,x,y):
        self.reset(x,y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 10

        if game_over == 0:

            #get key presses
            key = pg.key.get_pressed()
            if key[pg.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pg.K_SPACE] == False:
                self.jumped = False
            if key[pg.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pg.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pg.K_LEFT] == False and key[pg.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #Check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x +dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e falling
                    elif self.vel_y >= 0:
                        dy =tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collision with enemies
            if pg.sprite.spritecollide(self, slot_group, False):
                game_over = -1
                game_over_fx.play()
    
            #check for collision with Lava
            if pg.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            #check for collision with exit
            if pg.sprite.spritecollide(self, exit_group, False):
                game_over = 1


            #Update player position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

#Calculate new player posision
#Check collision at new position
#Adjust player position

        #draw player onto screen
        screen.blit(self.image, self.rect)
        #Draw rectangle around player for debugging
        #pg.draw.rect(screen, (255,255,255), self.rect,2)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,3):
            img_right =pg.image.load(f"img/sanke{num}.png")
            img_right = pg.transform.scale(img_right, (40,80))
            img_left = pg.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pg.image.load("img/ghost.png")
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self,data):
        self.tile_list = []

        # making variable for row, so it keeps track of the row
        row_count = 0
        for row in data:
            # making variable for column, so it keeps track of the column
            col_count = 0
            for tile in row:
                if tile == 1:
                    #draw dirt
                    img = pg.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    #draw grass
                    img = pg.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    #draw Enemy
                    slot = Enemy(col_count * tile_size, row_count * tile_size + 7)
                    slot_group.add(slot)
                if tile == 6:
                    #draw lava
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    #draw coin
                    coin = Coin(col_count* tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    #draw exit
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #Draw rectangle around tile for debugging
            #pg.draw.rect(screen, (255,255,255), tile[1],2)

class Enemy(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img/slut.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load("img/lava.png")
        self.image = pg.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load("img/polet.png")
        self.image = pg.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Exit(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        img = pg.image.load("img/exit.png")
        self.image = pg.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player(100, screen_height - 107)

slot_group = pg.sprite.Group()
lava_group = pg.sprite.Group()
coin_group = pg.sprite.Group()
exit_group = pg.sprite.Group()

#create dummy coin for showing score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)


#load in level data and create world
if path.exists(f"level{level}_data"):
    pickle_in = open(f"level{level}_data", "rb")
    world_data = pickle.load(pickle_in)
world = World(world_data)

#Create buttons
restart_button = Button(screen_widht // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_widht // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_widht // 2 + 150, screen_height // 2, exit_img)

run = True
# Main loop
while run:
    
    clock.tick(fps)

    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))

    if main_menu == True:
        if exit_button.draw() == True:
            run = False
        if start_button.draw() == True:
            main_menu = False
    else: 
        world.draw()

        # Game is running, enemies update and coins are collected
        if game_over == 0:
            slot_group.update()
            #update score
            #check if a coin has been collected
            if pg.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text("Score: " + str(score), font_score, white, tile_size + 10, 10)


        slot_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        #If player is dead
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
            
        #If player has completed the level    
        if game_over == 1:
            #reset game and go to next level
            level += 1
            score = 0
            if level <= max_levels:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text("YOU HAVE COMPLETED SANKEFORMER", font, blue, (screen_widht // 6) - 140, screen_height // 2 - 50)
                #restart game
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # Check for key presses
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    pg.display.update()

pg.quit()