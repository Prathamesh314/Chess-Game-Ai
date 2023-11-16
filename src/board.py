from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self) -> None:
        self.squares = [[0]*8 for _ in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        '''
        This method is going to calculate all possible (valid) moves of a piece on a specific row and column
        '''

        def knight_moves():
            possible_moves = [
                (row+1, col+2),
                (row-1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
                (row-2, col+1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.is_valid(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        # create squares of moves
                        initial = Square(row, col, piece)
                        final = Square(possible_move_row, possible_move_col)

                        # create a new move
                        move = Move(initial, final)
                        # adding valid moves to our list of moves
                        piece.add_moves(move)


        if isinstance(piece, Pawn):
            pass

        elif isinstance(piece, Rook):
            pass

        elif isinstance(piece, Bishop):
            pass

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Queen):
            pass

        elif isinstance(piece, King):
            pass


    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # These are all pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        # Time to put knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Time to put bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Time to put rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Time to put King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        # Time to put Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

