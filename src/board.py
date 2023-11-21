from typing import List

from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self) -> None:
        self.squares = [[0] * 8 for _ in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        '''
        This method is going to calculate all possible (valid) moves of a piece on a specific row and column
        '''

        def king_moves():
            moves_list = [
                (1, 0),
                (-1, 0),
                (0, -1),
                (0, 1),
                (1, 1),
                (1, -1),
                (-1, -1),
                (-1, 1),
            ]
            for moves in moves_list:
                row_incr, col_incr = moves
                new_row, new_col = row + row_incr, col + col_incr
                if Square.is_valid(new_row, new_col):
                    if self.squares[new_row][new_col].is_empty_or_rival(piece.color) and not isinstance(self.squares[new_row][new_col].piece, King):
                        initial = Square(row, col)
                        final = Square(new_row, new_col)
                        move = Move(initial, final)
                        piece.add_moves(move)

        def all_in_one_moves(inc: List[tuple]):
            for incr in inc:
                row_incr, col_incr = incr
                temp_row, temp_col = row, col
                while 0 <= temp_row <= ROWS and 0 <= temp_col <= COLS:
                    temp_row += row_incr
                    temp_col += col_incr
                    if Square.is_valid(temp_row, temp_col):
                        if self.squares[temp_row][temp_col].is_empty_or_rival(piece.color) and not isinstance(self.squares[temp_row][temp_col].piece, King):
                            initial = Square(row, col)
                            final = Square(temp_row, temp_col)
                            move = Move(initial, final)
                            piece.add_moves(move)
                            if self.squares[temp_row][temp_col].has_rival(piece.color):
                                break

        def pawn_move():
            steps = 1 if piece.moved else 2
            start = row + piece.dir
            end = row + ((1 + steps) * piece.dir)
            # vertical moves
            for possible_moved_row in range(start, end, piece.dir):
                if Square.is_valid(possible_moved_row, col):
                    if self.squares[possible_moved_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(possible_moved_row, col)
                        move = Move(initial, final)
                        piece.add_moves(move)
                    else:
                        break
                else:
                    break
            # diagonal moves
            possible_moved_rows = row + piece.dir
            possible_moved_cols = [col+1, col-1]
            for possible_moved_col in possible_moved_cols:
                if Square.is_valid(possible_moved_rows, possible_moved_col):
                    if self.squares[possible_moved_rows][possible_moved_col].has_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_moved_rows, possible_moved_col)
                        move = Move(initial, final)
                        piece.add_moves(move)

        def knight_moves():
            possible_moves = [
                (row + 1, col + 2),
                (row - 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
                (row - 2, col + 1),
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
            pawn_move()

        elif isinstance(piece, Rook):
            all_in_one_moves(
                [
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                ]
            )

        elif isinstance(piece, Bishop):
            all_in_one_moves(
                [
                    (-1, -1),
                    (-1, 1),
                    (1, -1),
                    (1, 1),
                ]
            )

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Queen):
            all_in_one_moves(
                [
                    (-1, -1),
                    (-1, 1),
                    (1, -1),
                    (1, 1),
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                ]
            )

        elif isinstance(piece, King):
            king_moves()

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
        self.squares[5][4] = Square(5, 4, King(color))

        # Time to put Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
