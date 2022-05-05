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

    """
    Đánh 1 nước cờ và thực thi (Không áp dụng cho Nhập thành, Phong tốt và Bắt tốt qua đường) 
    """


    def makeMove(self, move):
        """Cập nhật nước đi lên bàn cờ"""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Lưu nước đi vào logMove
        self.whiteToMove = not self.whiteToMove # Đổi lượt đi của người chơi

    """
    Đánh lại nước cờ cuối (undo)
    """

    def undoMove(self):
        if len(self.moveLog) !=0:    #Kiểm tra xem đúng là 1 nước cờ có thể hoàn lại không
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove #Đổi lại lượt

    """
    Các nước đi hợp lệ
    """

    def getValidMoves(self):
        return self.getAllPossibleMoves()


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
            if c+1 <= 7: #Ăn bên phải
                if self.board[r - 1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: #Tốt đen moves
            if self.board[r+1][c] == "--": #Tiến 1 bước
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #Tiến 2 bước
                    moves.append(Move((r, c), (r+2, c), self.board))
            #Ăn quân địch
            if c-1>=0: #Ăn trái
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1<=7: #Ăn phải
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))

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

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]
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