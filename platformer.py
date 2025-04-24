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
tile_size = 200


#Load images
sun_img = pg.image.load("img/sun.png")
bg_img = pg.image.load("img/sky.png")
player_img = pg.image.load("img/sanke.png")


def draw_grid():
    for line in range(0,6):
        pg.draw.line(screen, (255,255,255), (0,line * tile_size), (screen_widht, line * tile_size))
        pg.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_height))

class World():
    def __init__(self,data):
        self.tile_list = []

        # load images
        dirt_img = pg.image.load("img/dirt.png")

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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data= [
[1,1,1,1,1],
[1,0,0,0,1],
[1,0,0,0,1],
[1,1,1,1,1],
]

world = World(world_data)

run = True
# Main loop
while run:
    
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))

    world.draw()

    draw_grid()

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