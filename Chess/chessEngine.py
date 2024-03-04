"""storing and determining valid moves, it will also store move logs"""


class Gamestate():
    def __init__(self):
        # try improving this with numpy in future
        # 8x8 2d list
        # this board variable stores the current state of the game
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        ]

        self.whiteToMove = True  # false if black to move
        self.moveLog = []  # keep track of the moves

    def make_move(self, move):
        """Takes a move as parameter and executes it (It will not work for en-passant ,promotion and castling)"""
        if move.is_pawn_promotion():
            move.piece_moved = move.piece_moved[0] + "Q"
            self.board[move.start_row][move.start_col] = "--"  # empty the start square before moving the piece
            self.board[move.end_row][
                move.end_col] = move.piece_moved

        else:
            self.board[move.start_row][move.start_col] = "--"  # empty the start square before moving the piece
            self.board[move.end_row][
                move.end_col] = move.piece_moved  # overwrite the captured piece / square with the moved piece
        self.moveLog.append(move)  # make the move logs
        self.whiteToMove = not self.whiteToMove  # switch the player after this move

    def undo_move(self):
        """Undo the last move"""
        if len(self.moveLog) != 0:  # Check if any moves are made
            move = self.moveLog.pop()  # Pops out the last move from moveLog
            self.board[move.start_row][
                move.start_col] = move.piece_moved  # we are placing the moved piece to the start square
            self.board[move.end_row][move.end_col] = move.piece_captured  # put the captured piece back to the board
            self.whiteToMove = not self.whiteToMove  # Switch the turn back

    def get_valid_moves(self):
        """Get valid moves with considering checks"""
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """Get all Moves without considering checks"""
        moves = []
        for row in range(len(self.board)):  # Number of rows
            for col in range(len(self.board[row])):  # Number of Columns
                piece_color = self.board[row][col][0]
                if (piece_color == 'w' and self.whiteToMove) or (
                        piece_color == 'b' and not self.whiteToMove):  # check if piece can be moved by current player
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.get_pawn_moves(row, col, moves)
                    elif piece == 'R':
                        self.get_rook_moves(row, col, moves)
                    elif piece == 'N':
                        self.get_knight_moves(row, col, moves)
                    elif piece == 'B':
                        self.get_bishop_moves(row, col, moves)
                    elif piece == 'Q':
                        self.get_queen_moves(row, col, moves)
                    elif piece == 'K':
                        self.get_king_moves(row, col, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        """Get all possible moves of a pawn , given its current position"""
        """White pawns start on row 6 (rank 2) and black pawn starts on row 1 (rank 7) """
        """Need to add promotions as valid move to move list"""
        if self.whiteToMove:
            # For white pawn
            if self.board[r - 1][c] == "--":  # 1 square pawn advance If the square in front of pawn is empty
                moves.append(Move((r, c), (r - 1, c), self.board))
                # We check two square pawn advance only if the square in front is empty
                if r == 6 and self.board[r - 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # To capture an enemy piece on left
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # To capture an enemy piece on right
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            # For black pawn
            if self.board[r + 1][c] == "--":  # 1 square pawn advance If the square in front of pawn is empty
                moves.append(Move((r, c), (r + 1, c), self.board))
                # We check two square pawn advance only if the square in front is empty
                if r == 1 and self.board[r + 2][c] == '--':  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # To capture an enemy piece on left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # To capture an enemy piece on right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_rook_moves(self, r, c, moves):
        """
        Get all possible moves of a Rook, given its current position.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for d in directions:
            new_row, new_col = r, c
            while True:
                new_row += d[0]
                new_col += d[1]
                if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                    piece_color = self.board[r][c][0]
                    if self.board[new_row][new_col][0] != piece_color:  # Check for any piece
                        moves.append(Move((r, c), (new_row, new_col), self.board))
                        if self.board[new_row][new_col] != '--':  # Stop if a piece is encountered
                            break
                    else:
                        break  # Stop if own piece is encountered
                else:
                    break  # Stop if outside board

    def get_knight_moves(self, r, c, moves):
        """
        Get all possible moves of a Knight, given its current position.
        """
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for move in knight_moves:
            new_row = r + move[0]
            new_col = c + move[1]
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                piece_color = self.board[r][c][0]
                if (piece_color == 'w' and self.whiteToMove) or (piece_color == 'b' and not self.whiteToMove):
                    if self.board[new_row][new_col][0] != piece_color:
                        moves.append(Move((r, c), (new_row, new_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        """
        Get all possible moves of a Bishop, given its current position.
        """
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in directions:
            new_row, new_col = r, c
            while True:
                new_row += d[0]
                new_col += d[1]
                if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                    piece_color = self.board[r][c][0]
                    if self.board[new_row][new_col][0] != piece_color:
                        moves.append(Move((r, c), (new_row, new_col), self.board))
                        if self.board[new_row][new_col] != '--':
                            break  # Stop if a piece is encountered
                    else:
                        break  # Stop if own piece is encountered
                else:
                    break  # Stop if outside board

    def get_queen_moves(self, r, c, moves):
        """
        Get all possible moves of a Queen, given its current position.
        """
        self.get_rook_moves(r, c, moves)  # Queen moves like a rook
        self.get_bishop_moves(r, c, moves)  # Queen moves like a bishop

    def get_king_moves(self, r, c, moves):
        """
        Get all possible moves of a King, given its current position.
        (Considering only basic king moves, not castling)
        """
        king_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for move in king_moves:
            new_row = r + move[0]
            new_col = c + move[1]
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                piece_color = self.board[r][c][0]
                if (piece_color == 'w' and self.whiteToMove) or (piece_color == 'b' and not self.whiteToMove):
                    if self.board[new_row][new_col][0] != piece_color:
                        moves.append(Move((r, c), (new_row, new_col), self.board))



class Move():
    rank_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # ranks mapped to the rows
    rows_to_ranks = {v: k for k, v in rank_to_rows.items()}  # rows mapped to the ranks
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}  # files mapped to the Columns
    cols_to_files = {v: k for k, v in files_to_cols.items()}  # Columns mapped to the Files

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]  # get the piece that moved
        self.piece_captured = board[self.end_row][self.end_col]  # get the piece / square that was captured
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col  # Generates a unique id to the move

    def __eq__(self, other):
        """Overrides the default __eq__ method to check if the move id of the user move is on of the valid move"""
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_notation(self):
        """ use this method to get the notation of the piece moved"""
        """return eg : a5a6"""
        """need to work on this method to generate fide notation"""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        """use this method to convert row and column to ranks and files based of the predefined dictionary"""
        """ return eg : a5 if col == 0 and row == 3"""
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def is_pawn_promotion(self):
        """this method checks if the pawn is in promotion square"""
        if self.piece_moved == 'bp' and self.end_row == 7:  # for black piece
            return True
        elif self.piece_moved == 'wp' and self.end_row == 0:
            return True
        else:
            return False



