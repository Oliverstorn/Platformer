import pygame as pg

# Setup
pg.init()

clock = pg.time.Clock()
fps = 60

# Setting the screen up
screen_widht = 1000
screen_height = 775
screen = pg.display.set_mode((screen_widht, screen_height))
pg.display.set_caption("Sankeformer")

# define game variables
tile_size = 50
game_over = 0


#Load images
sun_img = pg.image.load("img/sun.png")
bg_img = pg.image.load("img/sky.png")
restart_img = pg.image.load("img/restart_btn.png")


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
    

            #check for collision with Lava
            if pg.sprite.spritecollide(self, lava_group, False):
                game_over = -1

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
        pg.draw.rect(screen, (255,255,255), self.rect,2)

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

        # load images
        dirt_img = pg.image.load("img/dirt.png")
        grass_img = pg.image.load("img/grass.png")

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
                    #draw dirt
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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pg.draw.rect(screen, (255,255,255), tile[1],2)

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

world_data= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,0,0,0,3,0,0,0,0,2,0,0,0,0,0,0,0,0,1],
[1,0,0,2,2,2,2,0,0,2,1,0,0,2,2,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1],
[1,0,0,0,0,0,0,3,0,0,2,0,2,0,2,2,2,1,1,1],
[1,0,0,0,0,2,2,2,2,6,6,6,6,6,1,1,1,1,1,1],
[1,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


player = Player(100, screen_height - 107)

slot_group = pg.sprite.Group()
lava_group = pg.sprite.Group()

world = World(world_data)

#Create buttons
restart_button = Button(screen_widht // 2 - 50, screen_height // 2 + 100, restart_img)

run = True
# Main loop
while run:
    
    clock.tick(fps)

    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))

    world.draw()

    if game_over == 0:
        slot_group.update()

    slot_group.draw(screen)
    lava_group.draw(screen)

    game_over = player.update(game_over)

    #If player is dead
    if game_over == -1:
        if restart_button.draw():
            player.reset(100, screen_height - 107)
            game_over = 0

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