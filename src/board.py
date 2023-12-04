from typing import List

from const import *
from square import Square
from piece import *
from move import Move
import copy


class Board:
    def __init__(self) -> None:
        self.squares = [[0] * 8 for _ in range(COLS)]
        self._create()
        self.lastmove = None
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if diff < 0 else piece.right_rook
                self.move(rook, rook.moves[-1])

        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        piece.moved = True
        piece.clear_moves()
        self.lastmove = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def check_check(self, piece, row, col) -> bool:
        temp_row, temp_col = row, col
        # check horizontally left
        temp_col -= 1
        while temp_col >= 0:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Bishop, Knight, Pawn))):
                return True
            temp_col -= 1

        temp_row, temp_col = row, col
        # check horizontally right
        temp_col += 1
        while temp_col < COLS:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Bishop, Knight, Pawn))):
                return True
            temp_col += 1

        temp_row, temp_col = row, col
        # check vertically up
        temp_row -= 1
        while temp_row >= 0:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Bishop, Knight, Pawn))):
                return True
            temp_row -= 1

        temp_row, temp_col = row, col
        temp_row += 1
        # check vertically down
        while temp_row < ROWS:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Bishop, Knight, Pawn))):
                return True
            temp_row += 1

        temp_row, temp_col = row, col
        temp_row -= 1
        temp_col -= 1
        # checking diagonally up left
        while temp_row >= 0 and temp_col >= 0:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Rook, Knight, Pawn))):
                return True
            temp_row -= 1
            temp_col -= 1

        temp_row, temp_col = row, col
        temp_row -= 1
        temp_col += 1
        # checking diagonally up right
        while temp_row >= 0 and temp_col < COLS:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Rook, Knight, Pawn))):
                return True
            temp_row -= 1
            temp_col += 1

        temp_row, temp_col = row, col
        temp_row += 1
        temp_col -= 1
        # checking diagonally down left
        while temp_row < ROWS and temp_col >= 0:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Rook, Knight, Pawn))):
                return True
            temp_row += 1
            temp_col -= 1

        temp_row, temp_col = row, col
        temp_row += 1
        temp_col += 1
        # diagonally down right
        while temp_row < ROWS and temp_col < COLS:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color):
                break
            elif self.squares[temp_row][temp_col].has_rival(piece.color) and not (isinstance(self.squares[temp_row][temp_col].piece, (Rook, Knight, Pawn))):
                return True
            temp_row += 1
            temp_col += 1

        return False


    def is_check(self, piece, move):
        initial_row, initial_col = move.initial.row, move.initial.col
        king_row, king_col = None, None

        # I just need to find f king
        # Checking horizontally
        temp_row, temp_col = initial_row, initial_col
        for i in range(COLS):
            if i != initial_col and self.squares[temp_row][i].has_team_piece(piece.color) and isinstance(self.squares[temp_row][i].piece, King):
                king_row, king_col = temp_row, i
                break

        if king_row is not None and king_col is not None:
            if self.check_check(piece, king_row, king_col):
                return True
            return False

        # Checking vertically
        temp_row, temp_col = initial_row, initial_col
        for j in range(ROWS):
            if j != initial_row and self.squares[j][temp_col].has_team_piece(piece.color) and isinstance(self.squares[j][temp_col].piece, King):
                king_row, king_col = j, temp_col
                break

        if king_row is not None and king_col is not None:
            if self.check_check(piece, king_row, king_col):
                return True
            return False

        # check diagonally left up
        temp_row, temp_col = initial_row, initial_col
        temp_row -= 1
        temp_row -= 1
        while temp_row >= 0 and temp_col >= 0:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color) and isinstance(self.squares[temp_row][temp_col].piece, King):
                king_row, king_col = temp_row, temp_col
                break
            temp_row -= 1
            temp_row -= 1

        if king_row is not None and king_col is not None:
            if self.check_check(piece, king_row, king_col):
                return True
            return False

        # check diagonally right up
        temp_row, temp_col = initial_row, initial_col
        temp_row -= 1
        temp_col += 1
        while temp_row >= 0 and temp_col < COLS:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color) and isinstance(self.squares[temp_row][temp_col].piece, King):
                king_row, king_col = temp_row, temp_col
                break
            temp_row -= 1
            temp_col += 1

        if king_row is not None and king_col is not None:
            if self.check_check(piece, king_row, king_col):
                return True
            return False

        # check diagonally right down
        temp_row, temp_col = initial_row, initial_col
        temp_row += 1
        temp_col += 1
        while temp_row < ROWS and temp_col < COLS:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color) and isinstance(self.squares[temp_row][temp_col].piece, King):
                king_row, king_col = temp_row, temp_col
                break
            temp_row += 1
            temp_col += 1

        if king_row is not None and king_col is not None:
            if self.check_check(piece, king_row, king_col):
                return True
            return False

        # check diagonally left down
        temp_row, temp_col = initial_row, initial_col
        temp_row += 1
        temp_col -= 1
        while temp_row < ROWS and temp_col >= 0:
            if self.squares[temp_row][temp_col].has_team_piece(piece.color) and isinstance(self.squares[temp_row][temp_col].piece, King):
                king_row, king_col = temp_row, temp_col
                break
            temp_row += 1
            temp_col -= 1

        if king_row is not None and king_col is not None:
            if self.check_check(piece, king_row, king_col):
                return True
            return False

        return False

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
            if not piece.moved:
                # Queen side castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        if self.squares[row][1].is_empty() and self.squares[row][2].is_empty() and self.squares[row][3].is_empty():
                            # rook move
                            piece.left_rook = left_rook
                            initial = Square(row, 0)
                            final = Square(row, 3)
                            move = Move(initial, final)
                            left_rook.add_moves(move)

                            # king move
                            initial = Square(row, col)
                            final = Square(row, 2)
                            move = Move(initial, final)
                            piece.add_moves(move)

                # King side castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        if self.squares[row][6].is_empty() and self.squares[row][5].is_empty():

                            # rook
                            piece.right_rook = right_rook
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            move = Move(initial, final)
                            right_rook.add_moves(move)

                            # king move
                            initial = Square(row, col)
                            final = Square(row, 6)
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
                        final_piece = self.squares[possible_moved_row][possible_moved_col].piece
                        final = Square(possible_moved_rows, possible_moved_col, final_piece)
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

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

        # Time to put Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)