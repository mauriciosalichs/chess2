import pygame
import threading
import numpy as np
from game import *
from time import sleep

# Initialize constant variables
pygame.init()
size = 100
extra_space = 300
large_font = pygame.font.Font(None, 36)
medium_font = pygame.font.Font(None, 26)
small_font = pygame.font.Font(None, 16)
screen_width, screen_height = size*8 + extra_space, size*8
screen = pygame.display.set_mode((screen_width, screen_height))

white_imgs = [pygame.image.load(f"img/w{piece_name}.png").convert_alpha() for piece_name in ["PAWN","ROOK","KNIGHT","BISHOP","QUEEN","KING"]]
black_imgs = [pygame.image.load(f"img/b{piece_name}.png").convert_alpha() for piece_name in ["PAWN","ROOK","KNIGHT","BISHOP","QUEEN","KING"]]

def draw_board(mx = -100, my = -100):
    white_cell = True
    for i in range(8):
        for j in range(8):
            if white_cell:
                color = (200,200,200)
            else:
                color = (100,100,100)
            pygame.draw.rect(screen, color, (i*size, j*size, size, size))
            white_cell = not white_cell
        white_cell = not white_cell
    # Last used cell: pygame.draw.rect(screen, assets.blue, (lx*size, ly*size, size, size), 3)
    # Draw pieces:
    for piece in white_pieces:
        if piece != selected_piece:
            (i,j) = piece.position
            screen.blit(white_imgs[piece.piece_type.value], (i*size, j*size))
    for piece in black_pieces:
        if piece != selected_piece:
            (i,j) = piece.position
            screen.blit(black_imgs[piece.piece_type.value], (i*size, j*size))
    if selected_piece:
        piece_image = white_imgs[selected_piece.piece_type.value] if selected_piece.color == 'w' else black_imgs[selected_piece.piece_type.value]
        screen.blit(piece_image, (mx, my))
    pygame.display.flip()

def draw_animation(length):
    global selected_piece
    last_moved = GameState().last_moved
    if last_moved:
        (selected_piece,x1,y1,x2,y2) = last_moved
        x1*=100
        x2*=100
        y1*=100
        y2*=100
        x_step = (x2 - x1) / (length - 1)
        y_step = (y2 - y1) / (length - 1)
        x_values = [int(x1 + i * x_step) for i in range(length)]
        y_values = [int(y1 + i * y_step) for i in range(length)]
        ranges = list(zip(x_values, y_values))
        for (i,j) in ranges:
            draw_board(i,j)
            sleep(0.1/length)
        selected_piece = None
    
def reset_variables():
    global action_started, selected_piece, x, y
    action_started = False
    x, y = -100, -100
    selected_piece = None

running = True
waiting_opponent = False
reset_variables()
draw_board()

board = GameState().board
white_pieces = GameState().white_pieces
black_pieces = GameState().black_pieces
waiting_opp = None

while running:
    if action_started:
        draw_board(x-50, y-50)
    if waiting_opponent and not (waiting_opp and waiting_opp.is_alive()):
        waiting_opponent = False
        draw_animation(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not waiting_opponent:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if not action_started and event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                x1 = int(x1/size)
                y1 = int(y1/size)
                selected_piece = board[x1][y1]
                if selected_piece and selected_piece.color == 'w':
                   action_started = True
                   #print('\n',selected_piece,allowed_movements(selected_piece))
            elif action_started and event.type == pygame.MOUSEBUTTONUP:
                x2, y2 = event.pos
                x2 = int(x2/size)
                y2 = int(y2/size)
                if (x2,y2) in allowed_movements(board, selected_piece):
                    # White plays the chosen movement
                    accept_movement(selected_piece,x2,y2)
                    # Now black plays
                    waiting_opp = threading.Thread(target=black_plays)
                    waiting_opp.start()
                    waiting_opponent = True
                else:
                    print("Not allowed")
                reset_variables()
                draw_board()       
pygame.quit()
