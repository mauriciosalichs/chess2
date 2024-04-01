from enum import Enum

class PieceType(Enum):
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5

class Piece:
    def __init__(self, color, piece_type, position):
        self.color = color
        self.piece_type = piece_type
        self.position = position
        self.value = self.value()

    def __str__(self):
        color_str = "White" if self.color == 'w' else "Black"
        piece_type_str = {
            PieceType.PAWN: "Pawn",
            PieceType.ROOK: "Rook",
            PieceType.KNIGHT: "Knight",
            PieceType.BISHOP: "Bishop",
            PieceType.QUEEN: "Queen",
            PieceType.KING: "King"
        }[self.piece_type]
        return f"{color_str} {piece_type_str} {self.position}"
        
    def value(self):
        return {
            PieceType.PAWN: 1,
            PieceType.ROOK: 5,
            PieceType.KNIGHT: 3,
            PieceType.BISHOP: 3,
            PieceType.QUEEN: 9,
            PieceType.KING: 9999
        }[self.piece_type]

    def redef_value(self):
        self.value = [1, 5, 3, 3, 9, 9999][self.piece_type]

