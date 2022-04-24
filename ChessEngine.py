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