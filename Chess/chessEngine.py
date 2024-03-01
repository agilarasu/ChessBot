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

    def make_move(self,move):
        self.board[move.start_row][move.start_col] = "--"  # empty the start square before moving the piece
        self.board[move.end_row][move.end_col] = move.piece_moved  # overwrite the captured piece / square with the moved piece
        self.moveLog.append(move)   # make the move logs
        self.whiteToMove = not self.whiteToMove  # switch the player after this move


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

    def get_notation(self):
        """ use this method to get the notation of the piece moved"""
        """return eg : a5a6"""
        """need to work on this method to generate fide notation"""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self,row,col):
        """use this method to convert row and column to ranks and files based of the predefined dictionary"""
        """ return eg : a5 if col == 0 and row == 3"""
        return self.cols_to_files[col] + self.rows_to_ranks[row]