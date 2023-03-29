import pygame
class GameBoard():
    def __init__(self, gameboard_pos, width, height):
        self.board_x = gameboard_pos[0]
        self.board_y = gameboard_pos[1]
        self.board_image = pygame.image.load(resource_path("images/gameboard.png"))
        self.board_image  = pygame.transform.scale(board_image, (gameboard_side_length, gameboard_side_length))