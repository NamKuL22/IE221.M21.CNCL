import pygame as pg
from Chess import ChessEngine, AI

BOARD_WIDTH = BOARD_HEIGHT = 512 # set size bàn cờ
MOVE_LOG_PANEL_WIDTH = 100
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENTION = 8 # bàn cờ 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENTION # set size mỗi ô cờ
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
    screen = pg.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    pg.display.set_caption('Cờ Vua (Bấm 1 để đánh với máy | Bấm 2 để chơi với người)')
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    moveLogFont = pg.font.SysFont('Arial', 16, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = () # lưu trữ ô cờ cuối mà người dùng chọn
    playerClicks = [] # lưu trữ 2 ô cờ người dùng chọn
    gameOver = False
    playerOne = True  # Nếu là người dùng chơi quân trắng thì là True, nếu là AI thì là False
    playerTwo = True  # Tương tự cho quân đen
    selectGameMode = False #Chọn đánh với người hay với máy (True: đã chọn, False: chưa chọn)

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            #Thao tác bằng chuột
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver and selectGameMode:
                    location = pg.mouse.get_pos() #(x, y) vị trị của con trỏ chuột
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: #người dùng click vào 1 ô 2 lần hoặc click vào movelog
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
                    selectGameMode = False
                    pg.display.set_caption('Cờ Vua (Bấm 1 để đánh với máy | Bấm 2 để chơi với người)')
                    if e.key == pg.K_1 and not selectGameMode:  # Chơi với máy
                        playerTwo = False
                        selectGameMode = True
                        pg.display.set_caption('Cờ Vua (chơi với máy)')
                    if e.key == pg.K_2 and not selectGameMode:  # Chơi với người
                        playerTwo = True
                        selectGameMode = True
                        pg.display.set_caption('Cờ Vua (chơi 2 người)')
                if e.key == pg.K_1 and not selectGameMode: #Chơi với máy
                    playerTwo = False
                    selectGameMode = True
                    pg.display.set_caption('Cờ Vua (chơi với máy)')
                if e.key == pg.K_2 and not selectGameMode: #Chơi với người
                    playerTwo = True
                    selectGameMode = True
                    pg.display.set_caption('Cờ Vua (chơi 2 người)')
        # Tìm ra nước đi cho AI
        if not gameOver and not humanTurn:
            AIMove = AI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            print(move.getChessNotation())
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkmate or gs. stalemate:
            gameOver = True
            text = 'Hết nước đi! Hòa' if gs. stalemate else 'CheckMate! Quân đen thắng' if gs.whiteToMove else 'CheckMate! Quân trắng thắng'
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)
        pg.display.flip()


def drawBoard(screen):
    """Vẽ các ô của bàn cờ"""
    global colors
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c)%2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


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


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    """Xử lý graphics trong trạng thái hiện tại của bàn cờ"""
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # vẽ các quân cờ lên trên ô bàn cờ
    drawMoveLog(screen, gs, moveLogFont)

def drawPieces(screen, board):
    """Vẽ các quân cờ lên bàn trong trạng thái hiện tại của GameState.board"""
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    """Vẽ MoveLog"""
    moveLogRect = pg.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
    pg.draw.rect(screen, pg.Color("black"), moveLogRect)
    moveLog =gs.moveLog
    moveTexts = []
    moveTexts.append('   Moves log')
    moveTexts.append('    W       B')
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation() + "  "
        if i + 1 < len(moveLog): #đảm bảo quân đen đã đi
            moveString += moveLog[i+1].getChessNotation()
        moveTexts.append(moveString)
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(len(moveTexts)):
        text = moveTexts[i]
        textObject = font.render(text, True, pg.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


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
        #vẽ quân cờ bị ăn
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow -1
                endSquare = pg.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #vẽ quân cờ di chuyển
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    font = pg.font.SysFont('Times New Roman', 32, True, False)
    textObject = font.render(text, 0, pg.Color('Pink'))
    textLocation = pg.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color('Red'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()