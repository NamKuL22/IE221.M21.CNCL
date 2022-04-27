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
    loadImages()
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
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
