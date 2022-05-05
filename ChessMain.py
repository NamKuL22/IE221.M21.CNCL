import pygame
import pygame as pg
from Chess import ChessEngine

WIDTH = HEIGHT = 512 # set size bàn cờ
DIMENTION = 8 # bàn cờ 8x8
SQ_SIZE = HEIGHT // DIMENTION # set size mỗi ô cờ
MAX_FPS = 30
IMAGES = {}


def loadImages():
    """Load ảnh các quân cờ vào game"""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # scale ảnh để vừa với size mỗi ô cờ

def main():
    """Hàm main xử lý input của người dùng và cập nhật lại graphics cho bàn cờ"""
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = () # lưu trữ ô cờ cuối mà người dùng chọn
    playerClicks = [] # lưu trữ 2 ô cờ người dùng chọn
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            #Thao tác bằng chuột
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos() #(x, y) vị trị của con trỏ chuột
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #người dùng click vào 1 ô 2 lần
                    sqSelected = ()
                    playerClicks = [] # reset click của người dùng
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: # khi chọn 2 ô khác nhau
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # reset click của người dùng
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            #Thao tác bằng phím
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z: #Undo khi bấm Z
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()

def drawGameState(screen, gs):
    """Xử lý graphics trong trạng thái hiện tại của bàn cờ"""
    drawBoard(screen)
    drawPieces(screen, gs.board) # vẽ các quân cờ lên trên ô bàn cờ

def drawBoard(screen):
    """Vẽ các ô của bàn cờ"""
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c)%2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """Vẽ các quân cờ lên bàn trong trạng thái hiện tại của GameState.board"""
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
