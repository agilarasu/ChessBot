"""
Main file for the ChessBot game
"""
import pygame as p
from Chess import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8  # Dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animation

IMAGES = {}

'''
Initialise a global dictionary of all Images
'''


def loadImages():
    pieces = ['wp', 'wR', 'wB', 'wN', 'wK', 'wQ', 'bp', 'bN', 'bR', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # now we can access the images with IMAGES['wp']


'''
The main driver for our program'''


def main():
    p.init()  # initialize the pygame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.Gamestate()  # calls the GameState of the Engine
    print(gs.board)
    loadImages()  # call only once before while
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Draws the game board and responsible for any game graphic'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on board
    # we can also add move highlighter or suggestions here
    drawPieces(screen, gs.board)  # draw pieces  on board


'''
Draws the squares of the board (Top left square is always white from both perspective)'''


def drawBoard(screen):
    colors = [p.Color("white"),
              p.Color("gray")]  # we can customize the board color here CHESS.COM : LIGHT GRAY,DARK GREEN
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # sum of x,y of light color is always even
            color = colors[(row + col) % 2]  # 0 for white 1 for gray
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


''' Places the pieces on board based on the given position'''


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':  # if not an empty square , draw the piece
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE,SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
