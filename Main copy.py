import pygame
from Board import Board
from Button import Button

pygame.init()

screenSize = 720
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((screenSize, screenSize))
layer1 = pygame.Surface((screenSize,screenSize))
layer2 = pygame.Surface((screenSize,screenSize))



def draw(display):
    screen.fill((0))
    board.draw(display)
    pygame.display.update()

def update():
    screen.fill((0))
    screen.blit(layer1,(0,0))
    screen.blit(layer2,(0,0))
    pygame.display.update()
        
board = Board(720,720,0)
board.startPos()        
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.click(mx,my)
    
    draw(screen)

    result =board.isWin()
    if result != False:
        print(result,"Wins!!")
        running = False


    # update()
    # pygame.draw.rect(layer2,"black",pygame.Rect(300,300,100,100))

    clock.tick(30)  # limits FPS

pygame.quit()