import pygame
from game import *

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

def draw_board():
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
        screen.blit(piece_image, (x-50, y-50))
    pygame.display.flip()


def reset_variables():
    global action_started, selected_piece, x, y
    action_started = False
    x, y = -10, -10
    selected_piece = None

running = True
reset_variables()
draw_board()

board = GameState().board
white_pieces = GameState().white_pieces
black_pieces = GameState().black_pieces

while running:

    if action_started:
        draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            if (x2,y2) in allowed_movements(selected_piece):
                # White plays the chosen movement
                selected_piece.position = (x2,y2)
                calculate_damage(x2,y2)
                board[x2][y2] = selected_piece
                board[x1][y1] = None
                # Now black plays
                black_plays_random()
            else:
                print("Not allowed" )
            reset_variables()
            draw_board()
            
pygame.quit()
