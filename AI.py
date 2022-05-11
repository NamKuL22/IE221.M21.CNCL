import random as rd


def findRandomMove(validMoves):
    return validMoves[rd.randint(0, len(validMoves)-1)]


