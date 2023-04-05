import pygame
from Classes.Board import Board
from Classes.Button import Button
from Classes.Computer import Computer
import sys

pygame.init()

screenSize = 720
clock = pygame.time.Clock()
clock.tick(30)
screen = pygame.display.set_mode((screenSize, screenSize))

font = pygame.font.SysFont("arialblack", 40)

def play(turn):
    """Function that runs the game."""

    board = Board(screenSize,screenSize,size = 6)#size can be modified
    board.startPos()
    computer = Computer(board)
    if turn == "first":
        board.turn = False
    else:
        board.turn = True      
    
    while True:
        screen.fill((0))
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.click(mx,my)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                    break
        
        if board.turn == True:
            board.computerMove(computer)

        board.draw(screen)

        pygame.display.update()
        
        result =board.isWin()
        if result != False:
            print(result,"Wins!!")
            pygame.time.delay(1000)
            break

def about():
    """Function that runs about/how to play page"""
    def text_seperator(text,x,y)->list:
        """Function that seperates the text by lines and return a list"""
        lines = []
        text_font = pygame.font.SysFont("arialblack", 20)
        for line in text.splitlines():
            text = text_font.render(line, True, "#b68f40")
            rect = text.get_rect(center=(x, y))
            lines.append([text,rect])
            y+=40
        return lines

    while True:
        screen.fill((0))
        mouse_pos = pygame.mouse.get_pos()

        text = """Each player moves one piece per turn.
        A piece can be moved one space forward or diagonally
        forward, if the target position is empty. A piece 
        may be also moved to a square occupied by an enemy 
        piece, if the target position is one space diagonally forward 
        The game ends if one player reaches opponent's home row.
        \n\n Made by Mehmet Sahin Uces"""

        back_button = Button(image=None, pos=(360, 550), text_input="BACK", font=font, base_color="#d7fcd4", hovering_color="White")

        for i in text_seperator(text,330,100):
            screen.blit(i[0], i[1])

        back_button.changeColor(mouse_pos)
        back_button.update(screen)
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    main_menu()
                    break
        pygame.display.update()

def main_menu():
    """Function that runs Main Menu."""
    while True:
        screen.fill((0))


        mouse_pos = pygame.mouse.get_pos()

        menu_text = font.render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(360, 100))

        first_button = Button(image=None, pos=(360, 200), text_input="FIRST TURN", font=font, base_color="#d7fcd4", hovering_color="White")
        second_button = Button(image=None, pos=(360, 300), text_input="SECOND TURN", font=font, base_color="#d7fcd4", hovering_color="White")
        about_button = Button(image=None, pos=(360, 400), text_input="HOW TO PLAY", font=font, base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=None, pos=(360, 500), text_input="QUIT", font=font, base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [first_button,second_button,about_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if first_button.checkForInput(mouse_pos):
                    play("first")
                if second_button.checkForInput(mouse_pos):
                    play("second")
                if about_button.checkForInput(mouse_pos):
                    about()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
