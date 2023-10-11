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

#0 = vacio, 1 = X, 2 = O
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

squarecords = [ [2,2],[162,2],[322,2],
                [2,162],[162,162],[322,162],
                [2,322],[162,322],[322,322]]

zones = []
def changesprite(zone):
    global xturn, squarecords, game, screen

    pos = squarecords.index([zone.x, zone.y])

    if xturn and game[pos//3][pos%3] == 0:
        screen.blit(Xzonesprite,[zone.x, zone.y])
        game[pos//3][pos%3] = 1
        xturn = False

    elif not xturn and game[pos//3][pos%3] == 0:
        screen.blit(Ozonesprite,[zone.x, zone.y])
        game[pos//3][pos%3] = 2
        xturn = True


def checkwin(game):
    global drawcomplete, winX, winO, screen

    diagonalwinX = [1, 1, 1] in [[game[0][0], game[1][1], game[2][2]], [game[0][2], game[1][1], game[2][0]]]
    diagonalwinO = [2, 2, 2] in [[game[0][0], game[1][1], game[2][2]], [game[0][2], game[1][1], game[2][0]]]
    
    if diagonalwinX:
        screen.blit(winX,[0,0])
        reset()
    elif diagonalwinO:
        screen.blit(winO,[0,0])
        reset()

    for x in range(3):
        if [game[0][x], game[1][x], game[2][x]] == [1, 1, 1]:
            screen.blit(winX,[0,0])
            reset()
        if [game[0][x], game[1][x], game[2][x]] == [2, 2, 2]:
            screen.blit(winO,[0,0])
            reset()
                
    for y in game:
        if y == [1,1,1]:
            screen.blit(winX,[0,0])
            reset()
            break

        if y == [2,2,2]:
            screen.blit(winO,[0,0])
            reset()
            break

    if "0" not in "".join([str(i) for k in game for i in k]):
        reset()

def reset():
    global game, drawcomplete

    pygame.display.flip()
    pygame.time.delay(2000)

    game = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    drawcomplete = False

while running:
    pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    for cord in cords:
        line = pygame.draw.line(screen, "black", cord[0], cord[1], 5)
    
    if not drawcomplete:
        for cord in squarecords:
            zones.append(screen.blit(zonesprite,[cord[0],cord[1]]))
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