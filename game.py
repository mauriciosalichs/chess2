from piece import *
import numpy as np
from random import choice
from copy import deepcopy

class GameState:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.board = board
            cls._instance.white_pieces = white_pieces
            cls._instance.black_pieces = black_pieces
            cls._instance.white_king_pos = white_king_pos
            cls._instance.black_king_pos = black_king_pos
            cls._instance.current_player = 'w'
            cls._instance.ok_moves = []
            cls._instance.last_moved = None
            cls._instance.white_in_check = False
            cls._instance.black_in_check = False
            cls._instance.white_castling_left = True
            cls._instance.white_castling_right = True
            cls._instance.black_castling_left = True
            cls._instance.black_castling_right = True
            cls._instance.ending = None
        return cls._instance


white_pieces = []
white_pieces.append(Piece('w',PieceType.PAWN,(0,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(1,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(2,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(3,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(4,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(5,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(6,6)))
white_pieces.append(Piece('w',PieceType.PAWN,(7,6)))
white_pieces.append(Piece('w',PieceType.ROOK,(0,7)))
white_pieces.append(Piece('w',PieceType.KNIGHT,(1,7)))
white_pieces.append(Piece('w',PieceType.BISHOP,(2,7)))
white_pieces.append(Piece('w',PieceType.QUEEN,(3,7)))
white_pieces.append(Piece('w',PieceType.KING,(4,7)))
white_pieces.append(Piece('w',PieceType.BISHOP,(5,7)))
white_pieces.append(Piece('w',PieceType.KNIGHT,(6,7)))
white_pieces.append(Piece('w',PieceType.ROOK,(7,7)))

black_pieces = []
black_pieces.append(Piece('b',PieceType.PAWN,(0,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(1,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(2,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(3,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(4,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(5,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(6,1)))
black_pieces.append(Piece('b',PieceType.PAWN,(7,1)))
black_pieces.append(Piece('b',PieceType.ROOK,(0,0)))
black_pieces.append(Piece('b',PieceType.KNIGHT,(1,0)))
black_pieces.append(Piece('b',PieceType.BISHOP,(2,0)))
black_pieces.append(Piece('b',PieceType.QUEEN,(3,0)))
black_pieces.append(Piece('b',PieceType.KING,(4,0)))
black_pieces.append(Piece('b',PieceType.BISHOP,(5,0)))
black_pieces.append(Piece('b',PieceType.KNIGHT,(6,0)))
black_pieces.append(Piece('b',PieceType.ROOK,(7,0)))

board = np.full((8,8), None)
for piece in white_pieces+black_pieces:
    (i,j) = piece.position
    board[i][j] = piece
    if piece.piece_type == PieceType.KING:
        if piece.color == 'w': white_king_pos = piece.position
        elif piece.color == 'b': black_king_pos = piece.position

# Allowed movements related functions

def check_cell(board, x, y, c):
    if x > 7 or x < 0 or y > 7 or y < 0:
        return 'forb'
    if board[x][y] == None:
        return 'cont'
    else:
        return 'forb' if board[x][y].color == c else 'stop'
            
def explore(board, player_color, rangeX=None,rangeY=None,v=None):
    ans = []
    rangeX = [v]*len(rangeY) if rangeX == None else rangeX
    rangeY = [v]*len(rangeX) if rangeY == None else rangeY
    for (i,j) in zip(rangeX,rangeY):
        action = check_cell(board, i, j, player_color)
        if action == 'cont':
            ans.append((i,j))
        elif action == 'stop':
            ans.append((i,j))
            break
        else:
            break
    return ans

def pawn_moves(board, x, y, player_color):
    ans = []
    adv = -1 if player_color == 'w' else 1
    if check_cell(board, x  ,y+adv,player_color) == 'cont': ans.append((x  ,y+adv))
    if check_cell(board, x-1,y+adv,player_color) == 'stop': ans.append((x-1,y+adv))
    if check_cell(board, x+1,y+adv,player_color) == 'stop': ans.append((x+1,y+adv))
    
    if player_color == 'w' and y == 6 and board[x][4]==None and board[x][5]==None: ans.append((x,4))
    if player_color == 'b' and y == 1 and board[x][2]==None and board[x][3]==None: ans.append((x,3))
    
    return ans

def king_moves(board, x, y, player_color):
    ans = []
    for (i,j) in [(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)]:
        if check_cell(board, i, j, player_color) != 'forb': ans.append((i,j))
    # Agregar Enroques
    return ans

def knight_moves(board, x, y, player_color):
    ans = []
    for (i,j) in [(x-2,y-1), (x-2,y+1), (x-1,y-2), (x-1,y+2), (x+1,y-2), (x+1,y+2), (x+2,y-1), (x+2,y+1)]:
        if check_cell(board, i, j, player_color) != 'forb': ans.append((i,j))
    return ans
    
def cross_moves(board, x, y, player_color):
    ans = []
    ans += explore(board, player_color,rangeX=range(x-1,-1,-1),v=y)
    ans += explore(board, player_color,rangeX=range(x+1,8),v=y)
    ans += explore(board, player_color,rangeY=range(y-1,-1,-1),v=x)
    ans += explore(board, player_color,rangeY=range(y+1,8),v=x)
    return ans
    
def diag_moves(board, x, y, player_color):
    ans = []
    ans += explore(board, player_color,rangeX=range(x-1,-1,-1),rangeY=range(y-1,-1,-1))
    ans += explore(board, player_color,rangeX=range(x+1,8),rangeY=range(y+1,8))
    ans += explore(board, player_color,rangeX=range(x-1,-1,-1),rangeY=range(y+1,8))
    ans += explore(board, player_color,rangeX=range(x+1,8),rangeY=range(y-1,-1,-1))
    return ans
    
def allowed_movements(board, piece, discard_mates=True):
    ans = []
    (x, y) = piece.position
    player_color = piece.color
    if piece.piece_type == PieceType.PAWN:
        ans += pawn_moves(board, x, y, player_color)
    elif piece.piece_type == PieceType.ROOK:
        ans += cross_moves(board, x, y, player_color)
    elif piece.piece_type == PieceType.KNIGHT:
        ans += knight_moves(board, x, y, player_color)
    elif piece.piece_type == PieceType.BISHOP:
        ans += diag_moves(board, x, y, player_color)
    elif piece.piece_type == PieceType.QUEEN:
        ans += cross_moves(board, x, y, player_color)
        ans += diag_moves(board, x, y, player_color)
    elif piece.piece_type == PieceType.KING:
        ans += king_moves(board, x, y, player_color)
        
    if discard_mates:
        def_ans= []
        for (x2,y2) in ans:
            safe_move = True
            board_ = np.copy(board)
            board_[x][y] = None
            eaten_piece = board[x2][y2]
            board_[x2][y2] = piece
            wkp = (x2,y2) if piece.piece_type == PieceType.KING and piece.color == 'w' else white_king_pos
            bkp = (x2,y2) if piece.piece_type == PieceType.KING and piece.color == 'b' else black_king_pos
            for piece_ in (black_pieces if player_color == 'w' else white_pieces):
                if piece_ == eaten_piece:
                    continue
                if (wkp if player_color == 'w' else bkp) in allowed_movements(board_, piece_, False):
                    safe_move = False
                    break
            if safe_move:
                def_ans.append((x2,y2))
        return def_ans
    else:
        return ans


# Calculating opponent movements

def predict_best_movement(board, piece, move, gen):
    if gen == 0:
        return 0
    if gen % 2 == 1:
        opp, plus, opt = 'w',  1, min
    else:
        opp, plus, opt = 'b', -1, max
        
    board_ = np.copy(board)
    (i,j) = piece.position
    (k,l) = move
    eaten_piece = board_[k][l]
    if eaten_piece:
        value = plus*eaten_piece.value
    else:
        value = 0
    board_[i][j] = None
    board_[k][l] = piece
    
    next_moves = []
    for i in range(8):
        for j in range(8):
            piece_ = board_[i][j]
            if piece_ and piece_.color == opp:
                for move_ in allowed_movements(board_, piece_, False):
                    prediction = predict_best_movement(board_, piece_, move_, gen - 1)
                    next_moves.append(prediction)
    return opt(next_moves) + value


def auto_play(pieces, just_calculate): # Trying to pick the best movement
    val = -99999
    ans = []
    acc = 0
    for piece in pieces:
        for move in allowed_movements(board, piece):
            acc+=1
            val_ = predict_best_movement(board, piece, move, 3)
            if val_ > val:
                ans = [(piece, move)]
                val = val_
            elif val_ == val:
                ans.append((piece, move))
            if just_calculate:
                print(f"Playing {piece} to {move} gives {val_} points.")
    
    if not just_calculate:
        (sel_piece, (x2,y2)) = choice(ans)
        team = 'black' if sel_piece.color == 'b' else 'white'
        print(f"\nFrom {acc} possibilites, {team} plays {sel_piece} to ({x2},{y2})")
        accept_movement(sel_piece,x2,y2)
        
def black_auto_play():
    auto_play(black_pieces, False)
    
def white_calc_play():
    auto_play(white_pieces, True)
    
def calc_moves_piece(piece):
    info = []
    for move in allowed_movements(board, piece):
        val = predict_best_movement(board, piece, move, 3)
        info.append(f"Moving {piece} to {move} gives {val} points.")
    return info

def black_plays_random(): # Just plays a Random movement
    possible_moves = []
    for piece in black_pieces:
        for move in allowed_movements(board, piece):
            possible_moves.append((piece,move))
    (sel_piece, (x2,y2)) = choice(possible_moves)
    print(f"\nFrom {len(possible_moves)} possibilites, black randomly plays {sel_piece} to ({x2},{y2})")   
    accept_movement(sel_piece,x2,y2)

def accept_movement(piece,x2,y2):
    (x1,y1) = piece.position
    piece.position = (x2,y2)
    board[x1][y1] = None
    eaten_piece = board[x2][y2]
    if eaten_piece:
        damaged = white_pieces if piece.color == 'b' else black_pieces
        damaged.remove(eaten_piece)
    board[x2][y2] = piece
    GameState().last_moved = (piece,x1,y1,x2,y2)
    
    if piece.color == 'w':
        if piece.piece_type == PieceType.PAWN and y2 == 0:
            piece.piece_type = PieceType.QUEEN
        if piece.piece_type == PieceType.KING:
            GameState().white_king_pos = (x2,y2)
        # ...
        for piece_ in white_pieces:
            if GameState().black_king_pos in allowed_movements(board, piece_):
                GameState().black_in_check = True
                break
        GameState().white_in_check = False
    else:
        if piece.piece_type == PieceType.PAWN and y2 == 7:
            piece.piece_type = PieceType.QUEEN
        if piece.piece_type == PieceType.KING:
            GameState().black_king_pos = (x2,y2)
        # ...
        for piece_ in black_pieces:
            if GameState().white_king_pos in allowed_movements(board, piece_):
                GameState().white_in_check = True
                break
        GameState().black_in_check = False

