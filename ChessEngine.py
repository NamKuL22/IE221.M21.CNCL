class GameState():
    """
    class để lưu trữ thông tin về trạng thái hiện tại của bàn cờ, xác định xem các nước đi hợp lệ ở hiện tại và lưu trữ move Log
    """
    def __init__(self):
        # Bàn cờ 8x8 biểu diễn bằng mảng 2d, mỗi phần tử là 1 quân cờ
        # Chữ cái đầu là màu cờ b-black, w-white
        # Chữ cái sau là loại cờ R-xe, N-Ngựa, B-Tượng, Q-Hậu, K-Vua, p-Tốt
        # "--" là ô cờ trống
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
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        """Cập nhật nước đi lên bàn cờ"""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Lưu nước đi vào logMove
        self.whiteToMove = not self.whiteToMove # Đổi lượt đi của người chơi

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

    def getChessNotation(self):
        """Lấy ra thông tin nước đi của quân cờ (ô ban đầu, ô di chuyển đến)"""
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """Lấy ra vị trí của ô cờ (File,Rank) từ col và row"""
        return self.colsToFiles[c] + self.rowsToRanks[r]