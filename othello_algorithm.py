import pygame
import copy

def variable_init(d_w, d_h, s_l, g_p, g_s_l):
    global display_width
    global display_height
    global side_length
    global gameboard_pos
    global gameboard_side_length

    display_width = d_w
    display_height = d_h
    side_length =s_l
    gameboard_pos = g_p
    gameboard_side_length = g_s_l


block = [[0 for i in range(8)] for j in range(8)]
sub_block = [[0 for i in range(8)] for j in range(8)]
pre_block = [[0 for i in range(8)] for j in range(8)]
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
    return int((select_x * gameboard_side_length / 8) + gameboard_pos[0])


def place_y(select_y):
    return int((select_y * gameboard_side_length / 8) + gameboard_pos[1])


def get_mouse(m_x, m_y):
    global mouse_x
    global mouse_y

    mouse_x = m_x
    mouse_y = m_y


def mouse_in_board(select_x, select_y):  # 클릭 위치가 게임보드 안인가?
    if mouse_x - gameboard_pos[0] >= 0 and 0 <= select_x <= 7:
        if mouse_y - gameboard_pos[1] >= 0 and 0 <= select_y <= 7:
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


def placeable_here(select_x, select_y):
    if mouse_in_board(select_x, select_y):
        if empty_block(select_x, select_y):
            if all_direction_test(select_x, select_y):
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


def placeable_turn():  # 이 차례에 둘 수 있는 곳이 있는가?
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
        if not placeable_turn():
            turn = 1
            if not placeable_turn():
                game_end()
            else:
                print("패스")
    else:
        turn = 1
        if not placeable_turn():
            turn = 2
            if not placeable_turn():
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


def preview(select_x, select_y):
    if placeable_here(select_x, select_y):
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
                    pre_block[i][j] = turn
                sub_block[i][j] = 0
    else:
        if mouse_in_board(select_x, select_y):
            if empty_block(select_x, select_y):
                pre_block[select_y][select_x] = 3


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


def display_update(screen, gameboard, black, white, pre_black, pre_white, pre_unplaceable):
    screen.blit(gameboard, [gameboard_pos[0], gameboard_pos[1]])

    for i in range(8):
        for r in range(8):
            if pre_block[i][r] != 1 and pre_block[i][r] != 2:
                if block[i][r] == 1:
                    screen.blit(black, [place_x(r), place_y(i)])
                elif block[i][r] == 2:
                    screen.blit(white, [place_x(r), place_y(i)])

            if pre_block[i][r] == 1:
                screen.blit(pre_black, [place_x(r), place_y(i)])
            elif pre_block[i][r] == 2:
                screen.blit(pre_white, [place_x(r), place_y(i)])
            elif pre_block[i][r] == 3:
                screen.blit(pre_unplaceable, [place_x(r), place_y(i)])

            if pre_block[i][r] != 0:
                pre_block[i][r] = 0

    pygame.display.update()