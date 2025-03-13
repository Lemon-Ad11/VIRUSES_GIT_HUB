import pygame
import sys
import time

def draw_image(screen, image_path, position):
    image = pygame.image.load(image_path)
    screen.blit(image, position)


pygame.init()
pygame.display.set_caption("Map Maker")
screen = pygame.display.set_mode((1000, 800))
screen.fill((255, 255, 255))
f1 = pygame.font.Font(None, 24)
text1 = f1.render('Copyright © 2025 Nosov Vsevolod & Ueldanov Danis', 1, (0, 0, 0))

screen.blit(text1, (500, 750))


pygame.display.update()

plate = [[0] * 23 for i in range(23)]

for i in range(23):
    for j in range(23):
        r = pygame.Rect(i * 32, j * 32, 32, 32)
        draw_image(screen, "air.jpg", r)

r = pygame.Rect(800, 50, 83, 125)
draw_image(screen, "save.jpg", r)

flag = 0

while True:
    if flag:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = event.pos[0] // 32
                y = event.pos[1] // 32
                if x < 23 and y < 23:
                    r = pygame.Rect(x * 32, y * 32, 32, 32)
                    plate[y][x] += 1
                    plate[y][x] %= 4
                    cur = plate[y][x]
                    pygame.mixer.music.load('tap.mp3')
                    pygame.mixer.music.play()
                    if cur == 0:
                        draw_image(screen, "air.jpg", r)
                    if cur == 1:
                        draw_image(screen, "wall.jpg", r)
                    if cur == 2:
                        draw_image(screen, "player 1.jpg", r)
                    if cur == 3:
                        draw_image(screen, "player 2.jpg", r)
                else:
                    x = event.pos[0]
                    y = event.pos[1]
                    if x > 800 and y > 50 and x < 800 + 83 and y < 50 + 125:
                        count = 0
                        count1 = 0
                        for i in range(23):
                            for j in range(23):
                                if plate[i][j] == 2:
                                    count += 1
                                if plate[i][j] == 3:
                                    count1 += 1
                        if count != 1 or count1 != 1:
                            pygame.mixer.music.load('WA.mp3')
                            pygame.mixer.music.play()
                        else:
                            file = open("count.txt", 'r')
                            cnt = int(str(file.read()))
                            for q in range(100):
                                file = open("count.txt", 'w')
                                file.write(str(cnt + 1))
                                filec = open("user_maps/user_map" + str(cnt + 1) + ".txt", 'w')
                                for i in range(23):
                                    for j in range(23):
                                        filec.write(str(plate[i][j]) + " ")
                                    filec.write('\n')
                            flag = 1
                            break

    pygame.display.flip()
pygame.mixer.music.load('OK.mp3')
pygame.mixer.music.play()
time.sleep(1)
pygame.quit()
sys.exit()
