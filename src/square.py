class Square:
    def __init__(self, row, col, piece=None) -> None:
        self.row = row
        self.col = col
        self.piece = piece

    def is_empty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_rival(self, color):
        return self.has_piece() and self.piece.color != color

    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_rival(color)

    def has_piece(self):
        return self.piece is not None


    @staticmethod
    def is_valid(r: int, c: int) -> bool:
        if 0 <= r <= 7 and 0 <= c <= 7:
            return True
        return False
    