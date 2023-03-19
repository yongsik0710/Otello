import pygame, os

pygame.init()

display_width = 1000
display_height = 800

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

# place_sound = pygame.mixer.Sound("place.wav")

block = [[0 for i in range(8)] for j in range(8)]
sub_block = [[0 for i in range(8)] for j in range(8)]

direction = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]


# 이미지 로드
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

gameboard = pygame.image.load(os.path.join(image_path, "gameboard.png"))
gameboard = pygame.transform.scale(gameboard, (display_min, display_min))

black = pygame.image.load(os.path.join(image_path, "blackstone.png"))
black = pygame.transform.scale(black, (side_length, side_length))

white = pygame.image.load(os.path.join(image_path, "whitestone.png"))
white = pygame.transform.scale(white, (side_length, side_length))


####### 함수 #######
def game_start():
    block[3][3] = 2
    block[4][4] = 2
    block[3][4] = 1
    block[4][3] = 1

    global turn
    turn = 1


def place_x(select_x):
    return int((select_x * side_length) + (gap[0]/2))


def place_y(select_y):
    return int((select_y * side_length) + (gap[1]/2))


def mouse_in_board(select_x, select_y):  # 클릭 위치가 게임보드 안인가?
    if mouse_x - (gap[0]/2) >= 0 and select_x < 8:
        if mouse_y - (gap[1]/2) >= 0 and select_y < 8:
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


def one_direction_test(select_x, select_y, dx, dy, n):  #한 방향 검사
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


def all_direction_test(select_x, select_y):  #8방향 검사
    for n in range(8):
        dx = direction[n][1]
        dy = direction[n][0]
        if one_direction_test(select_x, select_y, dx, dy, n+1):
            return True
    return False


def place_stones(select_x, select_y):
    for n in range(8):
        dx = direction[n][1]
        dy = direction[n][0]
        if one_direction_test(select_x, select_y, dx, dy, n+1):
            for i in range(8):
                for j in range(8):
                    if sub_block[i][j] == n+1 or sub_block[i][j] == -1:
                        sub_block[i][j] = -1
                    else:
                        sub_block[i][j] = 0
    sub_block[select_y][select_x] = -1
    for i in range(8):
        for j in range(8):
            if sub_block[i][j] == -1:
                block[i][j] = turn
            sub_block[i][j] = 0


def reset_sub_block():
    for i in range(8):
        for j in range(8):
            sub_block[i][j] = 0


def turn_change():
    global turn
    if turn == 1:
        turn = 2
    else:
        turn = 1


def display_update():
    screen.blit(gameboard, [gap[0]/2, gap[1]/2])
    for i in range(8):
        for r in range(8):
            if block[i][r] == 1:
                screen.blit(black, [place_x(r), place_y(i)])
            elif block[i][r] == 2:
                screen.blit(white, [place_x(r), place_y(i)])
    pygame.display.update()


####################
game_start()

running = True
while running:

    for event in pygame.event.get():
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        select_x = int((mouse_x - (gap[0]/2)) / side_length)
        select_y = int((mouse_y - (gap[1]/2)) / side_length)

        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭 이벤트
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(mouse_x, mouse_y)
            print(select_x, select_y)
            if mouse_in_board(select_x, select_y):
                if empty_block(select_x, select_y):
                    if all_direction_test(select_x, select_y):
                        reset_sub_block()
                        place_stones(select_x, select_y)
                        turn_change()
                        print("성공!!")
                    else:
                        print("그곳엔 둘 수 없습니다.")
                else:
                    print("그곳엔 둘 수 없습니다.")
            else:
                print("그곳엔 둘 수 없습니다.")
    display_update()

pygame.quit()
