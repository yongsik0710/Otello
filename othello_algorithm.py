import pygame
import configparser
import os
import copy

config = configparser.ConfigParser()
config.read('config.ini')

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

# 이미지 로드
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

gameboard = pygame.image.load(os.path.join(image_path, "gameboard.png"))
gameboard = pygame.transform.scale(gameboard, (display_min, display_min))

black = pygame.image.load(os.path.join(image_path, "blackstone.png"))
black = pygame.transform.scale(black, (side_length, side_length))

white = pygame.image.load(os.path.join(image_path, "whitestone.png"))
white = pygame.transform.scale(white, (side_length, side_length))


block = [[0 for i in range(8)] for j in range(8)]
sub_block = [[0 for i in range(8)] for j in range(8)]
direction = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]
turn = 1
turn_num = 0
history = []


# 함수
def game_start():

    block[3][3] = 2
    block[4][4] = 2
    block[3][4] = 1
    block[4][3] = 1

    history.append(copy.deepcopy(block))


def place_x(select_x):
    return int((select_x * side_length) + (gap[0] / 2))


def place_y(select_y):
    return int((select_y * side_length) + (gap[1] / 2))


def get_mouse(m_x, m_y):
    global mouse_x
    global mouse_y

    mouse_x = m_x
    mouse_y = m_y


def mouse_in_board(select_x, select_y):  # 클릭 위치가 게임보드 안인가?
    if mouse_x - (gap[0] / 2) >= 0 and select_x < 8:
        if mouse_y - (gap[1] / 2) >= 0 and select_y < 8:
            return True
        else:
            return False
    else:
        return False


def select_in_board(select_x, select_y):  # 선택 위치가 게임보드 안인가?
    if 0 <= select_x <= 7:
        if 0 <= select_y <= 7:
            return True
        else:
            return False
    else:
        return False


def empty_block(select_x, select_y):  # 선택한 곳이 비워져 있는가?
    if block[select_y][select_x] == 0:
        return True
    else:
        return False


def same_block(select_x, select_y):  # 선택한 곳이 같은 블럭인가? (검은색의 차례인 경우 검은색인 경우 참)
    if block[select_y][select_x] == turn:
        return True
    else:
        return False


def different_block(select_x, select_y):  # 선택한 곳이 다른 블럭인가? (검은색의 차례인 경우 흰색인 경우만 참)
    if block[select_y][select_x] != turn:
        if not empty_block(select_x, select_y):
            return True
        else:
            return False
    else:
        return False


def first_direction_test(select_x, select_y):  # 바로 다음 칸이 다른 색인가?
    if select_in_board(select_x, select_y):
        if different_block(select_x, select_y):
            return True
        else:
            return False
    else:
        return False


def one_direction_test(select_x, select_y, dx, dy, n):  # 한 방향 검사
    select_x += dx
    select_y += dy
    if first_direction_test(select_x, select_y):
        sub_block[select_y][select_x] = n
        while True:
            select_x += dx
            select_y += dy
            if select_in_board(select_x, select_y):
                if not empty_block(select_x, select_y):
                    if same_block(select_x, select_y):
                        return True
                    else:
                        sub_block[select_y][select_x] = n
                else:
                    return False
            else:
                return False
    else:
        return False


def all_direction_test(select_x, select_y):  # 8방향 검사
    for n in range(8):
        dx = direction[n][1]
        dy = direction[n][0]
        if one_direction_test(select_x, select_y, dx, dy, 0):
            return True
    return False


def place_stones(select_x, select_y):  # 돌 설치
    for n in range(8):
        dx = direction[n][1]
        dy = direction[n][0]
        if one_direction_test(select_x, select_y, dx, dy, n + 1):
            for i in range(8):
                for j in range(8):
                    if sub_block[i][j] == n + 1 or sub_block[i][j] == -1:
                        sub_block[i][j] = -1
                    else:
                        sub_block[i][j] = 0
    sub_block[select_y][select_x] = -1
    for i in range(8):
        for j in range(8):
            if sub_block[i][j] == -1:
                block[i][j] = turn
            sub_block[i][j] = 0


def placeable():  # 이 차례에 둘 수 있는 곳이 있는가?
    for i in range(8):
        for j in range(8):
            if empty_block(i, j):
                if all_direction_test(i, j):
                    return True
    return False


def turn_change():
    global turn
    global turn_num

    if turn == 1:
        turn = 2
        if not placeable():
            turn = 1
            if not placeable():
                game_end()
            else:
                print("패스")
    else:
        turn = 1
        if not placeable():
            turn = 2
            if not placeable():
                game_end()
            else:
                print("패스")

    turn_num += 1
    history.append(copy.deepcopy(block))


def undo():
    global turn_num
    global block
    global turn

    if turn_num >= 1:
        block = history[turn_num-1]
        turn_num -= 1
        if turn == 1:
            turn = 2
        else:
            turn = 1
    else:
        print("더 이상 되돌릴 수 없습니다.")


def game_end():  # 게임 결과 산출
    black = 0
    white = 0
    for i in range(8):
        for j in range(8):
            if block[i][j] == 1:
                black += 1
            elif block[i][j] == 2:
                white += 1
    print("검은색 :", black)
    print("흰색 : ", white)
    if black > white:
        print("검은색 승!")
    elif black == white:
        print("무승부")
    else:
        print("흰색 승!")


def game_reset():  # 게임 초기화
    global turn
    global turn_num

    turn = 1
    turn_num = 0
    history = []

    for i in range(8):
        for j in range(8):
            block[i][j] = 0
            sub_block[i][j] = 0
    game_start()
    print("게임 초기화됨")


def display_update(screen):
    screen.blit(gameboard, [gap[0] / 2, gap[1] / 2])
    for i in range(8):
        for r in range(8):
            if block[i][r] == 1:
                screen.blit(black, [place_x(r), place_y(i)])
            elif block[i][r] == 2:
                screen.blit(white, [place_x(r), place_y(i)])
    pygame.display.update()