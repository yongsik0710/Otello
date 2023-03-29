import pygame
import os
import configparser
import othello_algorithm as othello
import sys

pygame.init()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 설정 불러오기
config = configparser.ConfigParser()
config.read(resource_path('config.ini'))

#화면 설정
display_width = config.getint('display', 'width')
display_height = config.getint('display', 'height')
gameboard_side_length = int(0.9 * display_height)
side_length = int(gameboard_side_length / 8)
gameboard_pos = [int(0.15 * display_width), int(0.05 * display_height)]

othello.variable_init(display_width, display_height, side_length, gameboard_pos)

screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption('오델로')

# 이미지 로드
gameboard = pygame.image.load(resource_path("images/gameboard.png"))
gameboard = pygame.transform.scale(gameboard, (gameboard_side_length, gameboard_side_length))

black = pygame.image.load(resource_path("images/blackstone.png"))
black = pygame.transform.scale(black, (side_length, side_length))

white = pygame.image.load(resource_path("images/whitestone.png"))
white = pygame.transform.scale(white, (side_length, side_length))

pre_black = pygame.image.load(resource_path("images/pre_blackstone.png"))
pre_black = pygame.transform.scale(pre_black, (side_length, side_length))

pre_white = pygame.image.load(resource_path("images/pre_whitestone.png"))
pre_white = pygame.transform.scale(pre_white, (side_length, side_length))

pre_unplaceable = pygame.image.load(resource_path("images/pre_unplaceable.png"))
pre_unplaceable = pygame.transform.scale(pre_unplaceable, (side_length, side_length))

title = pygame.image.load(resource_path("images/title.png"))
title = pygame.transform.scale(title, (int(0.4 * display_height), int(0.4 * display_height)))

font = pygame.font.SysFont('None', int(0.06 * display_height))


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x - int(width / 2)
        self.y = y - int(height / 2)
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
        self.x = x - int(width / 2)
        self.y = y - int(height / 2)
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
        resume_button = Button(x_center, y_center - int(0.2 * display_height), button_width, button_height, 'Resume', resume)
        undo_button = Button(x_center, y_center - int(0.1 * display_height), button_width, button_height, 'Undo', undo)
        reset_button = Button(x_center, y_center, button_width, button_height, 'Reset', reset)
        options_button = Button(x_center, y_center + int(0.1 * display_height), button_width, button_height, 'Options', options)
        exit_button = Button(x_center, y_center + int(0.2 * display_height), button_width, button_height, 'Exit', exit)


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
    global preview_value_text
    global time_limit_value_text

    phase = 3
    objects = []

    preview_text_pos = y_center - int(0.2 * display_height)
    preview_text = TextBox(x_center - int(0.18 * display_height), preview_text_pos, button_width, button_height, 'Preview')
    colon_text = TextBox(x_center, preview_text_pos, int(0.6 * button_height), button_height, ':')
    preview_up_button = Button(x_center + int(0.12 * display_height), preview_text_pos, int(0.8 * button_height), int(0.8 * button_height), '<', change_preview)
    preview_value_text = TextBox(x_center + int(0.25 * display_height), preview_text_pos, int(0.6 * button_width), button_height, config.get('interface', 'preview'))
    preview_down_button = Button(x_center + int(0.38 * display_height), preview_text_pos, int(0.8 * button_height), int(0.8 * button_height), '>', change_preview)

    time_limit_text_pos = y_center - int(0.1 * display_height)
    time_limit_text = TextBox(x_center - int(0.18 * display_height), time_limit_text_pos, button_width, button_height, 'Time Limit')
    time_limit_up_button = Button(x_center + int(0.09 * display_height), time_limit_text_pos, int(0.8 * button_height), int(0.8 * button_height), '<', down_time_limit)
    time_limit_value_text = TextBox(x_center + int(0.25 * display_height), time_limit_text_pos, int(0.8 * button_width), button_height, config.get('gameplay', 'time limit'))
    time_limit_down_button = Button(x_center + int(0.41 * display_height), time_limit_text_pos, int(0.8 * button_height), int(0.8 * button_height), '>', up_time_limit)
    colon_text = TextBox(x_center, time_limit_text_pos, int(0.6 * button_height), button_height, ':')

    resolution_text_pos = y_center
    resolution_text = TextBox(x_center - int(0.18 * display_height), resolution_text_pos, button_width, button_height, 'Resolution')
    colon_text = TextBox(x_center, resolution_text_pos, int(0.6 * button_height), button_height, ':')

    back_button = Button(x_center, y_center + int(0.2 * display_height), button_width, button_height, 'Back to Menu', back_to_menu)

def change_preview():
    global preview_value_text

    if config.getboolean('interface', 'preview'):
        config['interface']['preview'] = 'False'
    else:
        config['interface']['preview'] = 'True'

    Text = config['interface']['preview']
    preview_value_text.buttonSurf = font.render(Text, True, (20, 20, 20))

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def up_time_limit():
    global time_limit_value_text

    time_limit = config.get('gameplay', 'time limit')
    time_limit_max = 30
    time_limit_min = 5

    if time_limit != 'unlimited':
        time_limit = int(time_limit)
        if int(time_limit) < time_limit_max:
            time_limit += 5
            time_limit = str(time_limit)
            config['gameplay']['time limit'] = time_limit
        else:
            config['gameplay']['time limit'] = 'unlimited'
    else:
        time_limit_min = str(time_limit_min)
        config['gameplay']['time limit'] = time_limit_min

    Text = config['gameplay']['time limit']
    time_limit_value_text.buttonSurf = font.render(Text, True, (20, 20, 20))

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def down_time_limit():
    global time_limit_value_text

    time_limit = config.get('gameplay', 'time limit')
    time_limit_max = 30
    time_limit_min = 5

    if time_limit != 'unlimited':
        time_limit = int(time_limit)
        if int(time_limit) > time_limit_min:
            time_limit -= 5
            time_limit = str(time_limit)
            config['gameplay']['time limit'] = time_limit
        else:
            config['gameplay']['time limit'] = 'unlimited'
    else:
        time_limit_max = str(time_limit_max)
        config['gameplay']['time limit'] = time_limit_max

    Text = config['gameplay']['time limit']
    time_limit_value_text.buttonSurf = font.render(Text, True, (20, 20, 20))

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def back_to_menu():
    global phase
    global objects

    phase = 2
    objects = []
    menu()


# 시작 화면
objects = []

button_width = int(0.28*display_height)
button_height = int(0.08*display_height)

x_center = int(display_width/2)
y_center = int(display_height/2)

panel_pos = [int(0.8 * display_width), y_center]

panel = TextBox(panel_pos[0], panel_pos[1], int(0.5 * gameboard_side_length), gameboard_side_length)

start_button = Button(x_center, y_center + int(0.15 * display_height), button_width, button_height, 'Game Start', game_start)
exit_button = Button(x_center, y_center + int(0.25 * display_height), button_width, button_height, 'Exit', exit)

phase = 0

# event handler
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if phase == 0:
            screen.fill((50, 50, 50))
            screen.blit(title, [x_center - int(0.4 * display_height) / 2, y_center - int(0.4 * display_height)])
            for object in objects:
                object.process()
            pygame.display.update()

        elif phase == 1:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            select_x = int((mouse_x - gameboard_pos[0]) / side_length)
            select_y = int((mouse_y - gameboard_pos[1]) / side_length)
            othello.get_mouse(mouse_x, mouse_y)

            if config.getboolean('interface', 'preview'):
                othello.preview(select_x, select_y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 메뉴 오픈
                    phase = 2
                    menu()
            # 마우스 클릭 이벤트
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if othello.placeable_here(select_x, select_y):
                        othello.place_stones(select_x, select_y)
                        othello.turn_change()
                    else:
                        print("그곳에는 둘 수 없습니다.")

            othello.display_update(screen, gameboard, black, white, pre_black, pre_white, pre_unplaceable)

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