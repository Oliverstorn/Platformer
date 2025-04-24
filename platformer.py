import pygame as pg

# Setup
pg.init()
clock = pg.time.Clock()

# Setting the screen up
screen_widht = 1000
screen_height = 775
screen = pg.display.set_mode((screen_widht, screen_height))
pg.display.set_caption("Platformer")

# define game variables
tile_size = 50


#Load images
sun_img = pg.image.load("img/sun.png")
bg_img = pg.image.load("img/sky.png")
player_img = pg.image.load("img/sanke.png")


class Player():
    def __init__(self,x,y):
        img =pg.image.load("img/sanke.png")
        self.img = pg.transform.scale(img, (80,80))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def update(self):

        dx = 0
        dy = 0
        #get key presses
        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pg.K_SPACE] == False:
            self.jumped = False
        if key[pg.K_LEFT]:
            dx -= 5
        if key[pg.K_RIGHT]:
            dx += 5

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #Check for collision

        #Update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

#Calculate new player posision
#Check collision at new position
#Adjust player position

        #draw player onto screen
        screen.blit(self.img, self.rect)

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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,2,0,2,0,2,2,2,2,2,1],
[1,0,0,0,0,2,2,2,2,0,0,0,0,0,1,1,1,1,1,1],
[1,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

player = Player(100, screen_height - 107)
world = World(world_data)

run = True
# Main loop
while run:
    
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))

    world.draw()
    player.update()


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