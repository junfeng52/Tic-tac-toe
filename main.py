import pygame

pygame.init()
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()
running = True
drawcomplete = False
xturn = True
pygame.display.set_caption("TITATOU")

zonesprite = pygame.image.load("img/zone.png")
Xzonesprite = pygame.image.load("img/xzone.png")
Ozonesprite = pygame.image.load("img/Ozone.png")
winX = pygame.image.load("img/xwin.png")
winO = pygame.image.load("img/Owin.png")

#0 = None, 1 = X, 2 = O
game = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

cords = [[(0, 0), (0, 480)],
        [(0, 480), (480, 480)],
        [(480, 480), (480, 0)],
        [(480,0), (0, 0)],
        #in line
        [(160, 0), (160, 480)],
        [(160*2, 0), (160*2, 480)],
        [(0, 160), (480, 160)],
        [(0, 160*2),(480, 160*2)]]

squarecords = [[[160*y+2, 160*x+2] for y in range(3)] for x in range(3)]

zones = []
def changesprite(zone):
    global xturn, squarecords, game, screen
    pos = []

    for x in range(3):
        for y in range(3):
            if [zone.x, zone.y] == squarecords[x][y]:
                pos = [x, y]

    if xturn and game[pos[0]][pos[1]] == 0:
        screen.blit(Xzonesprite, [zone.x, zone.y])
        game[pos[0]][pos[1]] = 1
        xturn = False
    elif not xturn and game[pos[0]][pos[1]] == 0:
        screen.blit(Ozonesprite, [zone.x, zone.y])
        game[pos[0]][pos[1]] = 2
        xturn = True

def checkwin(game):
    global drawcomplete, winX, winO
    winstate = [[game[0][0], game[1][1], game[2][2]], [game[0][2], game[1][1], game[2][0]]]
    for x in range(3):
        winstate.append([game[0][x], game[1][x], game[2][x]])
        winstate.append([game[x][0], game[x][1], game[x][2]])

    if [1, 1, 1] in winstate:
        screen.blit(winX,[0,0])
        reset()
    elif [2, 2, 2] in winstate:
        screen.blit(winO,[0,0])
        reset()

    if "0" not in "".join([str(i) for k in game for i in k]):
        reset()

def reset():
    global game, drawcomplete, xturn
    pygame.display.flip()
    pygame.time.delay(2000)
    game = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    xturn = True
    drawcomplete = False

while running:
    pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    for cord in cords:
        line = pygame.draw.line(screen, "black", cord[0], cord[1], 5)

    if not drawcomplete:
        for x in range(3):
            for y in range(3):
                zones.append(screen.blit(zonesprite, squarecords[x][y]))
        drawcomplete = True

    for event in pygame.event.get():
        #Quit event
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for zone in zones:
                if zone.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                    changesprite(zone)

    checkwin(game)
    pygame.display.flip()
    clock.tick(60)