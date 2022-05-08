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
    animate = False
    loadImages()
    running = True
    sqSelected = () # lưu trữ ô cờ cuối mà người dùng chọn
    playerClicks = [] # lưu trữ 2 ô cờ người dùng chọn
    gameOver = False
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            #Thao tác bằng chuột
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # reset click của người dùng
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #Thao tác bằng phím
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z: #Undo khi bấm Z
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == pg.K_r: #Reset bàn cờ khi bấm R
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            print(move.getChessNotation())
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'CheckMate! Quân đen thắng')
            else:
                drawText(screen, 'CheckMate! Quân trắng thắng')

        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Hết nước đi! Hòa')

        clock.tick(MAX_FPS)
        pg.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    """Highlight quân cờ đã chọn và các nước có thể di chuyển được của nó"""
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #đảm bảo sqSelected là quân cờ có thể di chuyển được
            #highlight ô đã chọn
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #set độ trong suốt, đục dần từ 0->255
            s.fill(pg.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight các nước có thể đi
            s.fill(pg.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected):
    """Xử lý graphics trong trạng thái hiện tại của bàn cờ"""
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # vẽ các quân cờ lên trên ô bàn cờ

def drawBoard(screen):
    """Vẽ các ô của bàn cờ"""
    global colors
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

def animateMove(move, screen, board, clock):
    """Animation khi di chuyển quân cờ"""
    global colors
    coords = [] #list tọa độ mà animation sẽ đi qua
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #số frame để di chuyển qua 1 ô
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #xóa quân cờ tại nơi nó di chuyển đến
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, endSquare)
        #
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #vẽ quân cờ di chuyển
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = pg.font.SysFont('Times New Roman', 32, True, False)
    textObject = font.render(text, 0, pg.Color('Pink'))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color('Red'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()
