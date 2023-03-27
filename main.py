import pygame
import os
import configparser
import othello_algorithm as othello

pygame.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path + "/images", relative_path)

def config_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 설정 불러오기
config = configparser.ConfigParser()
config.read(config_path('config.ini'))

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

othello.variable_init(display_width, display_height, gap, side_length)

screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption('오델로')


# 이미지 로드
gameboard = pygame.image.load(resource_path("gameboard.png"))
gameboard = pygame.transform.scale(gameboard, (display_min, display_min))

black = pygame.image.load(resource_path("blackstone.png"))
black = pygame.transform.scale(black, (side_length, side_length))

white = pygame.image.load(resource_path("whitestone.png"))
white = pygame.transform.scale(white, (side_length, side_length))

title = pygame.image.load(resource_path("title.png"))
title = pygame.transform.scale(title, (int(0.4*display_min), int(0.4*display_min)))

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

    #def __del__(self):
        #print("삭제")

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


class TextBox():
    def __init__(self, x, y, width, height, Text='Box'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fillColors = {'normal': '#ffffff'}

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(Text, True, (20, 20, 20))

        objects.append(self)

    #def __del__(self):
        #print("삭제")

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

#함수 선언
def game_start():
    global phase
    global objects

    othello.game_start()
    phase = 1

    objects = []


def exit():
    global running
    running = 0


def menu():
    if objects == []:
        resume_button = Button(button_x, int(0.2 * display_height), button_width, button_height, 'Resume', resume)
        undo_button = Button(button_x, int(0.3*display_height), button_width, button_height, 'Undo', undo)
        reset_button = Button(button_x, int(0.4 * display_height), button_width, button_height, 'Reset', reset)
        options_button = Button(button_x, int(0.5 * display_height), button_width, button_height, 'Options', options)
        exit_button = Button(button_x, int(0.6 * display_height), button_width, button_height, 'Exit', exit)


def resume():
    global objects
    global phase

    objects = []
    phase = 1


def reset():
    resume()
    othello.game_reset()


def undo():
    resume()
    othello.undo()


def options():
    global objects
    global phase

    phase = 3
    objects = []

    if objects == []:
        preview_text = TextBox(button_x-int(0.5*button_width), int(0.2 * display_height), button_width, button_height, 'Preview')
        time_limit_text = TextBox(button_x-int(0.5*button_width), int(0.3*display_height), button_width, button_height, 'Time Limit')
        resolution_text = TextBox(button_x-int(0.5*button_width), int(0.4 * display_height), button_width, button_height, 'Resolution')
        colon_text = TextBox(int(display_width / 2) + int(0.2 * button_width) / 2, int(0.2 * display_height),int(0.2 * button_width), button_height, ':')
        colon_text = TextBox(int(display_width / 2) + int(0.2 * button_width) / 2, int(0.3 * display_height),int(0.2 * button_width), button_height, ':')
        colon_text = TextBox(int(display_width / 2) + int(0.2 * button_width) / 2, int(0.4 * display_height),int(0.2 * button_width), button_height, ':')
        back_button = Button(button_x, int(0.6 * display_height), button_width, button_height, 'Back to Menu', back_to_menu)


def back_to_menu():
    global phase
    global objects

    phase = 2
    objects = []
    menu()

#버튼 설정
objects = []

button_width = int(0.28*display_min)
button_height = int(0.08*display_min)

button_x = int(display_width/2 - button_width/2)

start_button = Button(button_x, int(0.6*display_height), button_width, button_height, 'Game Start', game_start)
exit_button = Button(button_x, int(0.7*display_height), button_width, button_height, 'Exit', exit)

phase = 0

# event handler
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if phase == 0:
            screen.fill((50, 50, 50))
            screen.blit(title, [display_width/2 - int(0.4*display_min)/2, int(0.1*display_height)])
            for object in objects:
                object.process()
            pygame.display.update()

        elif phase == 1:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            select_x = int((mouse_x - (gap[0] / 2)) / side_length)
            select_y = int((mouse_y - (gap[1] / 2)) / side_length)
            othello.get_mouse(mouse_x, mouse_y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 메뉴 오픈
                    phase = 2
                    menu()
            # 마우스 클릭 이벤트
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if othello.mouse_in_board(select_x, select_y):
                        if othello.empty_block(select_x, select_y):
                            if othello.all_direction_test(select_x, select_y):
                                othello.place_stones(select_x, select_y)
                                othello.turn_change()
                            else:
                                print("그곳엔 둘 수 없습니다.")
                        else:
                            print("그곳엔 둘 수 없습니다.")
                    else:
                        print("그곳엔 둘 수 없습니다.")
            othello.display_update(screen, gameboard, black, white)

        elif phase == 2:
            screen.fill((50, 50, 50))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 메뉴 닫기
                    resume()
            for object in objects:
                object.process()
            pygame.display.update()

        elif phase == 3:
            screen.fill((50, 50, 50))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 옵션 닫기
                    back_to_menu()
            for object in objects:
                object.process()
            pygame.display.update()

pygame.quit()