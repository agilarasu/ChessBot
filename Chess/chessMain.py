"""
Main file for the ChessBot game

"""
import pygame as p
import chessEngine
import os

WIDTH = HEIGHT = 512
DIMENSION = 8  # Dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60  # For animation

IMAGES = {}
# add images here
'''
Initialise a global dictionary of all Images
'''
"""Import the audio files for the game"""
p.mixer.init()
move_self = p.mixer.Sound(os.path.join('audio', 'move-self.mp3'))
capture = p.mixer.Sound(os.path.join('audio', 'capture.mp3'))


def load_images():
    pieces = ['wp', 'wR', 'wB', 'wN', 'wK', 'wQ', 'bp', 'bN', 'bR', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # now we can access the images with IMAGES['wp']


def main():
    """The main driver for our program"""
    """Initialise the game graphics"""
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    """Initialise the game state"""
    gs = chessEngine.Gamestate()  # calls the GameState of the Engine
    print(gs.board)
    valid_moves = gs.get_valid_moves()  # get all valid moves from this position
    move_made = False  # Flag variable when a move is made
    load_images()  # call only once before while
    running = True
    sq_selected = ()  # stores the last click of the user
    player_clicks = []  # stores the player clicks as a list of two tuples eg: [(6,1),(5,1)] a6
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            # Mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x,y of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # check if the same square was selected twice
                    sq_selected = ()  # deselect the square
                    player_clicks = []  # delete the clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                # move the piece if they do a second click
                if len(player_clicks) == 2:
                    move = chessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_notation())
                    if gs.whiteToMove and move.piece_moved[
                        0] == 'w' and move in valid_moves:  # check piece color and valid move
                        gs.make_move(move)
                        move_made = True
                        make_sound(move)
                    elif not gs.whiteToMove and move.piece_moved[0] == 'b' and move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        make_sound(move)
                    else:
                        # handle invalid move
                        print("Invalid move!")

                    # reset the move to let them do next move
                    sq_selected = ()
                    player_clicks = []
            # Key handler
            elif event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                    # undo for left arrow
                    gs.undo_move()
                    move_made = True

        if move_made:  # Get a new set of valid moves after the current mave is made
            print("movemade")
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs):
    """Draws the game board and responsible for any game graphic"""
    draw_board(screen)  # draw squares on board
    # we can also add move highlighter or suggestions here
    draw_pieces(screen, gs.board)  # draw pieces  on board


def draw_board(screen):
    """Draws the squares of the board (Top left square is always white from both perspective)"""
    colors = [p.Color("white"),
              p.Color("gray")]  # we can customize the board color here CHESS.COM : LIGHT GRAY,DARK GREEN
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # sum of x,y of light color is always even
            color = colors[(row + col) % 2]  # 0 for white 1 for gray
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """Places the pieces on board based on the given position"""
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':  # if not an empty square , draw the piece
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def make_sound(move):
    """This method classifies the moves as captures , moves, check , checkmate and promotion"""

    if move.piece_captured != '--':
        p.mixer.Sound.play(capture)
    elif move.piece_captured == '--':
        p.mixer.Sound.play(move_self)


if __name__ == "__main__":
    main()
