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
            cls._instance.current_player = 'w'
            cls._instance.white_in_check = False
            cls._instance.black_in_check = False
            cls._instance.white_castling_left = True
            cls._instance.white_castling_right = True
            cls._instance.black_castling_left = True
            cls._instance.black_castling_right = True
            cls._instance.ending = None
        return cls._instance
        
    def check_cell(self, x, y, c):
        if x > 7 or x < 0 or y > 7 or y < 0:
            return 'forb'
        if self.board[x][y] == None:
            return 'cont'
        else:
            return 'forb' if self.board[x][y].color == c else 'stop'


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

# Allowed movements related functions

def explore(player_color, rangeX=None,rangeY=None,v=None):
    ans = []
    rangeX = [v]*len(rangeY) if rangeX == None else rangeX
    rangeY = [v]*len(rangeX) if rangeY == None else rangeY
    for (i,j) in zip(rangeX,rangeY):
        action = GameState().check_cell(i, j, player_color)
        if action == 'cont':
            ans.append((i,j))
        elif action == 'stop':
            ans.append((i,j))
            break
        else:
            break
    return ans

def pawn_moves(x, y, player_color):
    ans = []
    adv = -1 if player_color == 'w' else 1
    if GameState().check_cell(x  ,y+adv,player_color) == 'cont': ans.append((x  ,y+adv))
    if GameState().check_cell(x-1,y+adv,player_color) == 'stop': ans.append((x-1,y+adv))
    if GameState().check_cell(x+1,y+adv,player_color) == 'stop': ans.append((x+1,y+adv))
    
    if player_color == 'w' and y == 6 and board[x][4]==None and board[x][5]==None: ans.append((x,4))
    if player_color == 'b' and y == 1 and board[x][2]==None and board[x][3]==None: ans.append((x,3))
    
    return ans

def king_moves(x, y, player_color):
    ans = []
    for (i,j) in [(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)]:
        if GameState().check_cell(i, j, player_color) != 'forb': ans.append((i,j))
    # Agregar Enroques
    return ans

def knight_moves(x, y, player_color):
    ans = []
    for (i,j) in [(x-2,y-1), (x-2,y+1), (x-1,y-2), (x-1,y+2), (x+1,y-2), (x+1,y+2), (x+2,y-1), (x+2,y+1)]:
        if GameState().check_cell(i, j, player_color) != 'forb': ans.append((i,j))
    return ans
    
def cross_moves(x, y, player_color):
    ans = []
    ans += explore(player_color,rangeX=range(x-1,-1,-1),v=y)
    ans += explore(player_color,rangeX=range(x+1,8),v=y)
    ans += explore(player_color,rangeY=range(y-1,-1,-1),v=x)
    ans += explore(player_color,rangeY=range(y+1,8),v=x)
    return ans
    
def diag_moves(x, y, player_color):
    ans = []
    ans += explore(player_color,rangeX=range(x-1,-1,-1),rangeY=range(y-1,-1,-1))
    ans += explore(player_color,rangeX=range(x+1,8),rangeY=range(y+1,8))
    ans += explore(player_color,rangeX=range(x-1,-1,-1),rangeY=range(y+1,8))
    ans += explore(player_color,rangeX=range(x+1,8),rangeY=range(y-1,-1,-1))
    return ans
    
def allowed_movements(piece):
    ans = []
    (x, y) = piece.position
    player_color = piece.color
    if piece.piece_type == PieceType.PAWN:
        ans += pawn_moves(x, y, player_color)
    elif piece.piece_type == PieceType.ROOK:
        ans += cross_moves(x, y, player_color)
    elif piece.piece_type == PieceType.KNIGHT:
        ans += knight_moves(x, y, player_color)
    elif piece.piece_type == PieceType.BISHOP:
        ans += diag_moves(x, y, player_color)
    elif piece.piece_type == PieceType.QUEEN:
        ans += cross_moves(x, y, player_color)
        ans += diag_moves(x, y, player_color)
    elif piece.piece_type == PieceType.KING:
        ans += king_moves(x, y, player_color)
    return ans


# Calculating opponent movements

def calculate_black_play(piece, move, board, wpieces, bpieces, gen):
    if gen == 0:
        return 0
    if gen % 2 == 0:
        player_pieces, opp_pieces, plus = bpieces, wpieces, 1
    else:
        player_pieces, opp_pieces, plus = wpieces, bpieces, -1
    
    (i,j) = piece.position
    (k,l) = move
    eaten_piece = board[k][l]
    if eaten_piece:
        value = plus*eaten_piece.value
        for p in opp_pieces:
            if p.position == (k,l): opp_pieces.remove(p)
        
    else:
        value = 0
    board[i][j] = None
    board[k][l] = piece
    for p in player_pieces:
        if p.position == (i,j): p.position = (k,l)
    vals = []
    for piece_ in opp_pieces:
        for move_ in allowed_movements(piece_):
            vals.append(calculate_black_play(piece_, move_, board, wpieces, bpieces, gen - 1) + value)
    if vals:
        return max(vals) if gen % 2 == 0 else min(vals)
    else:
        return 0


def black_plays(): # Trying to pick the best movement (doesnt work)
    val = -99999
    ans = None
    acc = 0
    for piece in black_pieces:
        for move in allowed_movements(piece):
            acc+=1
            val_ = calculate_black_play(piece, move, np.copy(board), deepcopy(white_pieces), deepcopy(black_pieces), 2)
            #print(f"Move {piece} to {move}...gets {val_} points")
            if val_ > val:
                ans = (piece, move)
                val = val_
    
    (sel_piece, (x2,y2)) = ans
    print(f"\nFrom {acc} possibilites, black plays {sel_piece} to ({x2},{y2})")
    accept_movement(sel_piece,x2,y2)

def black_plays_random(): # Just plays a Random movement
    possible_moves = []
    for piece in black_pieces:
        for move in allowed_movements(piece):
            possible_moves.append((piece,move))
    (sel_piece, (x2,y2)) = choice(possible_moves)
    print(f"\nFrom {len(possible_moves)} possibilites, black plays {sel_piece} to ({x2},{y2})")   
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
