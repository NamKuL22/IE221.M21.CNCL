class GameState():
    """
    class để lưu trữ thông tin về trạng thái hiện tại của bàn cờ, xác định xem các nước đi hợp lệ ở hiện tại và lưu trữ move Log
    """
    def __init__(self):
        # Bàn cờ 8x8 biểu diễn bằng mảng 2d, mỗi phần tử là 1 quân cờ
        # Chữ cái đầu là màu cờ b-black, w-white
        # Chữ cái sau là loại cờ R-xe (Rook), N-Ngựa (Knight - trùng tên King), B-Tượng(Bishop), Q-Hậu(Queen), K-Vua (King), p-Tốt(pawn)
        # "--" là ô cờ trống
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = () #Điều kiện ô cờ để thực hiện bắt tốt qua đường
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]


    """
    Đánh 1 nước cờ và thực thi (Không áp dụng cho Nhập thành, Phong tốt và Bắt tốt qua đường) 
    """


    def makeMove(self, move):
        """Cập nhật nước đi lên bàn cờ"""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Lưu nước đi vào logMove
        self.whiteToMove = not self.whiteToMove # Đổi lượt đi của người chơi
        #Cập nhật vị trí Vua khi thực hiện nước cờ
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #Phong tốt
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #Bắt tốt qua đường
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #Bắt tốt

        #cập nhật biến enpassantPossible:
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #Chỉ khi tốt tiến 2 bước
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #Nhập thành:
        if move.isCatsleMove:
            if move.endCol - move.startCol == 2: #Nhập thành bên vua
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] #Di chuyển xe
                self.board[move.endRow][move.endCol + 1] = '--' #Xóa xe ở vị trí cũ
            else: #Nhập thành bên hậu
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] #Di chuyển xe
                self.board[move.endRow][move.endCol - 2] = '--' #Xóa xe ở vị trí cũ


        #Cập nhật biến castlingRights - bất cứ lúc nào Xe hoặc Vua di chuyển
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))



    """
    Đánh lại nước cờ cuối (undo)
    """

    def undoMove(self):
        if len(self.moveLog) !=0:    #Kiểm tra xem đúng là 1 nước cờ có thể hoàn lại không
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Đổi lại lượt
            # Cập nhật vị trí Vua khi cần
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo bắt tốt qua đường
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #Rời ô trống đang đứng
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo tốt tiến 2 bước
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            #undo quyền nhập thành:
            self.castleRightsLog.pop() #Loại bỏ quyền nhập thành
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            #undo nhập thành
            if move.isCatsleMove:
                if move.endCol - move.startCol == 2: #Phía vua
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: #Phía hậu
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] ='--'

    """
    Update Castle Rights
    """
    def updateCastleRights(self, move):
        #Nếu đã mất xe
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False
        #Nhập thành bình thường
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #Xe trái
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #Xe phải
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #Xe trái
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #Xe phải
                    self.currentCastlingRight.bks = False
    """
    Các nước đi hợp lệ
    """

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        #Copy quyền nhập thành
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        #1. Generate tất cả các nước cờ hợp lệ
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        #2. Với tùng nước cờ, thực thi chúng
        for i in range(len(moves)-1, -1, -1): #Khi remove khỏi list, thì check lại list
            self.makeMove(moves[i])

            #3. generate tất cả các nước cờ của đối thủ

            #4. Với từng nước cờ của họ
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                moves.remove(moves[i])
            #5. Nếu họ có thể ăn vua, thì nước cờ của mình không hợp lệ
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #Chiếu tướng và chiếu bí
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves
    """
    Xác định xem có đang bị chiếu tướng không
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    """
    Xác định nếu đối thủ có thể tần công vào ô cờ nào đó
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #Đổi lượt
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Đổi lượt lại
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #Ô đang bị tấn công
                return True
        return False

    """
    Các nước có thể đi
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #Số hàng
            for c in range(len(self.board[r])): #Số cột
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #Gọi hàm move dựa trên quân cờ
        return moves
    """
    Tạo 1 list moves của Tốt
    """

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #Tốt trắng moves:
            if self.board[r - 1][c] == "--": #Tiến 1 bước
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #Tiến 2 bước
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #Ăn bên trái
                if self.board[r - 1][c-1][0] == 'b': #Ăn cờ đối thủ
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))

            if c+1 <= 7: #Ăn bên phải
                if self.board[r - 1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
        else: #Tốt đen moves
            if self.board[r+1][c] == "--": #Tiến 1 bước
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #Tiến 2 bước
                    moves.append(Move((r, c), (r+2, c), self.board))
            #Ăn quân địch
            if c-1>=0: #Ăn trái
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c+1<=7: #Ăn phải
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

        #Phong tốt
    """
    Tạo 1 list moves của Xe
    """
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #Di chuyển ên, trái, xuống, phải
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #Check ô trống
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Check quân địch
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Check quân mình
                        break
                else: #Out bàn cờ
                    break

    """
    Tạo 1 list moves của Mã
    """
    def getKnightMoves(self, r, c, moves):
        knighMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knighMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Check không phải quân mình
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    """
    Tạo 1 list moves của Tượng
    """
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #Di chuyển chéo
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #Kiểm tra ô trống
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Kiểm tra quân địch
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Check quân mình
                        break
                else:   #Out bàn cờ
                    break

    """
    Tạo 1 list moves của Hậu
    """
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    """
    Tạo 1 list moves của Tướng
    """
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Kiểm tra quân địch
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Generate tất cả các vị trí mà vua có thể nhập thành rồi add vào list moves
    """
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #Không thể nhập thành nếu đang bị chiếu
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)



    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove = True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c), (r, c-2), self.board, isCastleMove = True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    """
    class xử lý di chuyển của các quân cờ vua
    """
    # keys map chuyển đổi từ row, col sang Rank, File của bàn cờ và ngược lại
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #Phong tốt
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        #Bắt tốt qua đường
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        #Nhập thành:
        self.isCatsleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    """
    Overriding equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        """Lấy ra thông tin nước đi của quân cờ (ô ban đầu, ô di chuyển đến)"""
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """Lấy ra vị trí của ô cờ (File,Rank) từ col và row"""
        return self.colsToFiles[c] + self.rowsToRanks[r]