import copy
import pygame as pg

pg.init()

FPS = 30

# FILE_PATH = "user_maps/user_map6.txt"
# FILE_PATH = "game_map/map1.txt"
TEXT = open("map_name.txt", 'r').read()
FILE_PATH = f"user_maps/{TEXT}.txt"

BLOCK_SIZE = 23
PREF = 25

WIDTH = 800
HEIGHT = 600
CAPTION = "viruses"

# WIDTH = 32 * 23
# HEIGHT = 32 * 23


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

imgs = {0: "air",
        1: "wall",
        11: "player_1",
        12: "player_12",
        21: "player_2",
        22: "player_22", }
ammo_imgs = {0: "red_ammo_0",
             1: "ammo_1",
             2: "ammo_2",
             3: "ammo_3"}

clock = pg.time.Clock()


def draw_image(screen, image_path, position, sizex, sizey):
    image = pg.image.load(image_path)
    image = pg.transform.scale(image, (sizex, sizey))
    screen.blit(image, position)


def load_image(screen, image_path):
    image = pg.image.load(image_path)
    return image


# 0 - air
# 1 - wall
# 2 - spawn first
# 3 - spawn second
class Base_palate:
    def __init__(self, plate):
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        self.size = len(plate[0])
        self.plate = plate

        for i in range(self.size):
            for j in range(self.size):
                if (plate[i][j] == 2):
                    self.x1 = i
                    self.y1 = j
                if (plate[i][j] == 3):
                    self.x2 = i
                    self.y2 = j

    def pos(self, x, y):
        return (self.plate[x][y])


# 0 - air
# 11 - 1st player
# 12 - 1st player base
# 21 - 2nd player
# 22 - 2nd player base
class Second_plate:
    def __init__(self, base_plate):
        self.size = base_plate.size
        self.plate = base_plate.plate
        self.plate[base_plate.x1][base_plate.y1] = 11
        self.plate[base_plate.x2][base_plate.y2] = 21

    def pos(self, x, y):
        return self.plate[x][y]


class Main_plate:
    def __init__(self, plate):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        pg.display.set_icon(load_image(self.screen, "textures/icons/icon.png"))

        self.base_plate = Base_palate(plate)
        self.size = self.base_plate.size
        self.x1 = self.base_plate.x1
        self.x2 = self.base_plate.x2
        self.y1 = self.base_plate.y1
        self.y2 = self.base_plate.y2
        self.live_1 = self.live_2 = 1
        self.used = [[0] * self.size for _ in range(self.size)]
        self.turn = 1
        self.ammo = 0

        self.h_info = PREF
        self.w_info = PREF + BLOCK_SIZE * self.size + 37

        self.second_plate = Second_plate(self.base_plate)
        self.last_second_plate = copy.deepcopy(self.second_plate.plate)


    def check(self, x, y):
        if (x < 0 or y < 0):
            return 0
        if (x >= self.size or y >= self.size):
            return 0
        return 1

    def new_turn(self, x, y):
        if (x > self.h_info + 83 * 2 or y >= self.w_info + 125): return
        if (x < self.h_info or y < self.w_info): return

        if (self.ammo <= 0):
            return

        self.ammo = 0
        self.turn += 1

        if (self.turn > 2):
            self.turn = 1

        self.last_second_plate = copy.deepcopy(self.second_plate.plate)

    def new_used(self):
        self.used = [[0] * self.size for _ in range(self.size)]

    def dfs(self, x, y):
        self.used[x][y] = 1

        cur = 0

        b = (self.turn) % 2 + 1
        if (self.second_plate.pos(x, y) in [int(f"{b}1"), int(f"{b}2")]):
            cur += 1

        for nx in [x - 1, x, x + 1]:
            for ny in [y - 1, y, y + 1]:
                if (self.check(nx, ny)):
                    if (self.used[nx][ny] == 0):
                        k = self.second_plate.pos(nx, ny)

                        if (k != 1 and k != int(f"{self.turn}2")):
                            cur += self.dfs(nx, ny)

        return cur

    def is_finish(self):
        ans = 0

        self.new_used()
        for i in range(self.size):
            for j in range(self.size):
                if (self.used[i][j] == 0):
                    if (self.second_plate.pos(i, j) == int(f"{self.turn}1")):
                        h = self.dfs(i, j)

                        # print(h, i, j)
                        if (h <= 0):
                            ans = self.turn

        if (self.live_1 == 0):
            ans = 2
        if (self.live_2 == 0):
            ans = 1

        return ans

    def check_undo(self, y, x):
        if (x < self.w_info or y < self.h_info + 83 * 4): return
        if (x > self.w_info + 125 or y > self.h_info + 83 * 4 + 83): return

        self.ammo = 0
        self.second_plate.plate = copy.deepcopy(self.last_second_plate)


    def moves(self, x, y):
        if (self.ammo >= 3):
            return

        if (self.check(x, y)):
            element = self.second_plate.pos(x, y)
            if (self.turn == 1):
                if (element == 0 or element == 21):
                    flag = 0
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            new_element = self.second_plate.plate[x + i][y + j]
                            if (new_element == 11 or new_element == 12):
                                flag = 1
                    if (flag == 1):
                        if (element == 0):
                            self.live_1 += 1
                            self.second_plate.plate[x][y] = 11
                        else:
                            self.live_2 -= 1
                            self.second_plate.plate[x][y] = 12

                        self.ammo += 1
            else:
                if (element == 0 or element == 11):
                    flag = 0
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            new_element = self.second_plate.plate[x + i][y + j]
                            if (new_element == 21 or new_element == 22):
                                flag = 1
                    if (flag == 1):
                        if (element == 0):
                            self.live_2 += 1
                            self.second_plate.plate[x][y] = 21
                        else:
                            self.live_1 -= 1
                            self.second_plate.plate[x][y] = 22

                        self.ammo += 1

    def event_check(self, end):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if (end == 0):
                if (event.type == pg.MOUSEBUTTONDOWN):
                    if (event.button == 1):
                        pos_x = event.pos[1]
                        pos_y = event.pos[0]

                        x = (event.pos[1] - PREF) // BLOCK_SIZE
                        y = (event.pos[0] - PREF) // BLOCK_SIZE
                        self.moves(x, y)
                        self.new_turn(pos_x, pos_y)
                        self.check_undo(pos_x, pos_y)

                        # print(pos_x, pos_y)

    def draw_finish(self):
        x = 1
        if (self.ammo == 0):
            x = 2

        rect = pg.Rect(self.w_info, self.h_info + 83, 125, 83)
        draw_image(self.screen, f"textures/icons/finish_{x}.png", rect, 125, 83)

    def draw(self):
        self.screen.fill(WHITE)

        end = self.is_finish()


        if (end != 0):
            color = "blue"
            if (end == 1):
                color = "red"

            rect = pg.Rect(self.w_info, self.h_info + 83 * 2, 125, 83)
            draw_image(self.screen, f"textures/icons/{color}_win.png", rect, 125, 83)
        else:
            rect = pg.Rect(self.w_info, self.h_info + 83 * 2 + 17, 48, 48)
            draw_image(self.screen, f"textures/icons/player_{self.turn}2.png", rect, 48, 48)

        self.event_check(end)

        for i in range(self.size):
            for j in range(self.size):
                x = PREF + j * BLOCK_SIZE
                y = PREF + i * BLOCK_SIZE
                rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                img = self.second_plate.plate[i][j]

                draw_image(self.screen, f"textures/icons/{imgs[img]}.png", rect, BLOCK_SIZE, BLOCK_SIZE)

        rect = pg.Rect(self.w_info, self.h_info, 125, 83)
        draw_image(self.screen, f"textures/icons/{ammo_imgs[self.ammo]}.png", rect, 125, 83)

        rect = pg.Rect(self.w_info, self.h_info + 83 * 4, 125, 83)
        draw_image(self.screen, f"textures/icons/undo.png", rect, 125, 83)

        self.draw_finish()

        clock.tick(FPS)
        pg.display.update()


def main():
    file = open(f'maps/{FILE_PATH}', 'r')
    text = file.read().split('\n')

    map = []
    for i in range(len(text)):
        lst = list(text[i].split())
        for j in range(len(lst)):
            lst[j] = int(lst[j])

        map.append(lst)

    main_plate = Main_plate(map)

    run = 1
    while (run):
        main_plate.draw()


main()
