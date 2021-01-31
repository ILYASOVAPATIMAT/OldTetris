import pygame
from copy import deepcopy
from random import choice, randrange
import pygame.mixer

# количество клеток по горизонтали
W = 11
# количество клеток по вертикали
H = 22
# размер клетки игрового поля
TILE = 30
# размер игрового поля
GAME_RES = W * TILE, H * TILE
# размер всего экрана
RES = 800, 700
# частота смены кадров
FPS = 60
# ожидание нажатия  запуска игры
start_game = False
vol = 1
grid = []
pygame.init()

sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

# прорисовка игрового поля
for x in range(W):
    for y in range(H):
        grid.append(pygame.Rect(x * TILE, y * TILE, TILE, TILE))

# фигуры
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

# появление и прорисовка фиуры
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
#заполняем поле нулевыми значенями
field = [[0 for i in range(W)] for j in range(H)]

anim_count = 0
anim_speed = 60 #скорость анимации
anim_limit = 2000 # максимальная скорость анимации

newrecord = False # новый рекорд в игре

start_bg = pygame.image.load('tet.jpg').convert()
bg = pygame.image.load('bf.jpg').convert()
game_bg = pygame.image.load('game.jpg').convert()

main_font = pygame.font.SysFont('comicsansms', 65)
font = pygame.font.SysFont('comicsansms', 45)

title_tetris = main_font.render('OLD TETRIS', True, pygame.Color('white'))
title_score = font.render('очки:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('gold'))

get_color = lambda: (randrange(30, 240), randrange(30, 240), randrange(30, 240))
figure = deepcopy(choice(figures))
next_figure = deepcopy(choice(figures))
color = get_color()
next_color = get_color()

score = 0
lines = 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

# игровая пауза
def paused(pauza):
    pygame.mixer.music.pause()
    font = pygame.font.SysFont('comicsansms', 42)
    follow = font.render('Paused', 1, GREEN, RED)
    screen.blit(follow, (300, 300))
    pygame.display.update()

    while pauza:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pauza = False
                    pygame.mixer.music.play(-1)

        clock.tick(15)

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    while not start_game:
        pygame.mixer.music.stop()
        screen = pygame.display.set_mode(RES)
        screen.blit(start_bg, (0, 0))
        pygame.display.set_caption("Старый тетрис...")
        img = pygame.image.load('Tetris.jpg')
        pygame.display.set_icon(img)
        font = pygame.font.SysFont('comicsansms', 45)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        follow = font.render('ИГРА ТЕТРИС', 1, RED, GREEN)
        screen.blit(follow, (280, 50))
        font = pygame.font.SysFont('comicsansms', 42)
        follow = font.render('START', 1, GREEN, RED)
        screen.blit(follow, (360, 550))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            key = pygame.key.get_pressed()
            if key[pygame.K_KP_ENTER] and start_game == False:
                s = pygame.mixer.Sound('1.mp3')
                s.play(0)
                follow = font.render('START', 1, RED, GREEN)
                font = pygame.font.SysFont('comicsansms', 45)
                screen.blit(follow, (360, 550))
                start_game = True

                for i in range(10):
                    for j in range(9):
                        pygame.draw.rect(screen, get_color(), (i * 80, j * 80, 76, 76))
                        pygame.display.flip()
                        clock.tick(150)

            elif event.type == pygame.MOUSEBUTTONDOWN and start_game == False:
                if event.pos[0] > 370 and event.pos[0] < 520 and event.pos[1] < 610 and event.pos[1] > 550:
                    s = pygame.mixer.Sound('1.mp3')
                    s.play(0)
                    follow = font.render('START', 1, RED, GREEN)
                    font = pygame.font.SysFont('comicsansms', 45)
                    screen.blit(follow, (360, 550))
                    start_game = True
                else:
                    start_game = False
        pygame.display.flip()
        clock.tick(FPS)

    # заставка переход к игре
    for i in range(10):
        for j in range(9):
            pygame.draw.rect(screen, get_color(), (i * 80, j * 80, 76, 76))
            pygame.display.flip()
            clock.tick(150)
    pygame.display.flip()
    clock.tick(2)

    # проигрывание фоновой мелодии
    pygame.mixer.music.load('3.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(vol)

    # начало игры
    while start_game:
        record = get_record()
        dx, rotate = 0, False
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))

        # delay for full lines
        for i in range(lines):
            pygame.time.wait(200)

        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                    s = pygame.mixer.Sound('4.mp3')
                    s.play(0)
                elif event.key == pygame.K_UP:
                    rotate = True
                elif event.key == pygame.K_s:
                    vol = abs(vol - 1)
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_SPACE:
                    pause = True
                    paused(pause)

        # смещение фигуры по Х
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        # смещение фигуры по у
        # увеличение скорости
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure = next_figure
                    color = next_color
                    next_figure = deepcopy(choice(figures))
                    next_color = get_color()
                    anim_limit = 2000
                    break

        # вращение фигуры
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        # проверка линий
        line = H - 1
        lines = 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1

        # подсчет очков
        score += scores[lines]

        if score > int(record) and not newrecord:
            s = pygame.mixer.Sound('6.mp3')
            s.play(0)
            newrecord = True

        # прорисовка решетки игры
        for i_rect in grid:
            pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1)

        # прорисовка элементов (кубиков) фигуры
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)

        #
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)

        # прорисовка следующей фигуры
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 340
            figure_rect.y = next_figure[i].y * TILE + 515
            pygame.draw.rect(sc, next_color, figure_rect)

        # прорисовка надписей
        sc.blit(title_tetris, (370, 50))
        sc.blit(title_score, (440, 175))
        sc.blit(font.render(str(score), True, pygame.Color('green')), (560, 180))
        sc.blit(title_record, (430, 230))
        sc.blit(font.render(record, True, pygame.Color('gold')), (590, 232))

        # завершение игры, обнуление значений игрового поля, заполнение поля цветными квадратиками
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count = 0
                anim_speed = 60
                anim_limit = 2000
                score = 0
                start_game = False

                # заставка заверщения игры
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)

        pygame.display.flip()
        clock.tick(FPS)
