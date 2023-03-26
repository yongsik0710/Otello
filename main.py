import pygame
import os
import configparser
from othello_algm import *

pygame.init()
# 설정 불러오기
config = configparser.ConfigParser()
config.read('config.ini')

#화면 설정
display_width = config.getint('display', 'width')
display_height = config.getint('display', 'height')

if display_height > display_width:
    display_max = display_height
    display_min = display_width
    gap = [0, display_max - display_min]
else:
    display_max = display_width
    display_min = display_height
    gap = [display_max - display_min, 0]

side_length = display_min / 8

screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption('오델로')

#이미지 불러오기
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

gameboard = pygame.image.load(os.path.join(image_path, "gameboard.png"))
gameboard = pygame.transform.scale(gameboard, (display_min, display_min))

black = pygame.image.load(os.path.join(image_path, "blackstone.png"))
black = pygame.transform.scale(black, (side_length, side_length))

white = pygame.image.load(os.path.join(image_path, "whitestone.png"))
white = pygame.transform.scale(white, (side_length, side_length))

font = pygame.font.SysFont('None', int(0.06*display_min))

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def game_start():
    game_start()
    phase = othello_algm.phase


def exit():
    global running
    running = 0

#버튼 설정
objects = []

button_width = int(0.28*display_min)
button_height = int(0.08*display_min)

button_x = display_width/2 - button_width/2

start_button = Button(button_x, int(0.7*display_height), button_width, button_height, 'Game Start', game_start)
exit_button = Button(button_x, int(0.8*display_height), button_width, button_height, 'Exit', exit)

phase = 0

# event handler
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if phase == 0:
        for object in objects:
            object.process()
        pygame.display.update()
        print(phase)

    elif phase == 1:
        for event in pygame.event.get():
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            select_x = int((mouse_x - (gap[0] / 2)) / side_length)
            select_y = int((mouse_y - (gap[1] / 2)) / side_length)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_reset()
            # 마우스 클릭 이벤트
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_in_board(select_x, select_y):
                        if empty_block(select_x, select_y):
                            if all_direction_test(select_x, select_y):
                                place_stones(select_x, select_y)
                                turn_change()
                            else:
                                print("그곳엔 둘 수 없습니다.")
                        else:
                            print("그곳엔 둘 수 없습니다.")
                    else:
                        print("그곳엔 둘 수 없습니다.")
        display_update()

pygame.quit()