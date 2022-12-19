import pygame
from .Piece import Piece
from copy import deepcopy


class Board:

    def __init__(self,policy = [1.0,0.2,0.5]):
        self.board = []
        self.currpiece = None
        self.reds = 12
        self.blues = 12
        self.redkings = 0
        self.bluekings = 0
        self.createBoard()

    def drawBoard(self, window):
        window.fill((0, 0, 0))
        for rows in range(8):
            for cols in range(rows % 2, 8, 2):
                pygame.draw.rect(window, (225, 225, 225),(rows * 100, cols * 100, 100, 100))

    def getpiece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == (225, 0, 0):
                self.reds -= 1
            else:
                self.blues -= 1

    def winner(self):
        if len(self.getAllMoves((0,0,225))) == 0:
            return "Red Wins"
        if len(self.getAllMoves((225,0,0)))==0:
            return "Blue Wins"
        return None

    def createBoard(self):
        for rows in range(8):
            self.board.append([])
            for cols in range(8):
                if rows % 2 != cols % 2:
                    if rows < 3:
                        self.board[rows].append(Piece(rows, cols, (0, 0, 225)))
                    elif rows > 4:
                        self.board[rows].append(Piece(rows, cols, (225, 0, 0)))
                    else:
                        self.board[rows].append(0)
                else:
                    self.board[rows].append(0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if (row == 0 or row == 7) and not piece.isKing:
            piece.makeKing()
            if piece.color == (225, 0, 0):
                self.redkings += 1
            else:
                self.bluekings += 1

    def draw(self, window):
        self.drawBoard(window)
        for rows in range(8):
            for cols in range(8):
                piece = self.board[rows][cols]
                if piece != 0:
                    piece.drawPiece(window)

    def getValidMoves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == (225, 0, 0) or piece.isKing:
            moves.update(self.peekLeft(row - 1, max(row - 3, -1), -1, piece.color,left,piece.isKing))
            moves.update(self.peekRight(row - 1, max(row - 3, -1), -1, piece.color,right,piece.isKing))

        if piece.color == (0, 0, 225) or piece.isKing:
            moves.update(self.peekLeft(row + 1,min(row + 3, 8),1,piece.color,left,piece.isKing))
            moves.update(self.peekRight(row + 1,min(row + 3, 8),1,piece.color,right,piece.isKing))
        return moves

    def peekLeft(self, start, stop, step, color, left, isKing, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, 8)

                    moves.update(self.peekLeft(r + step,row,step,color,left - 1,isKing,skipped=last+skipped))
                    moves.update(self.peekRight(r + step,row,step,color,left + 1,isKing,skipped=last+skipped))
                    if isKing:
                        if step == 1:
                            row = max(r - 3, -1)
                        else:
                            row = min(r + 3, 8)

                        moves.update(self.peekLeft(r - step,row,-step,color,left - 1,isKing,skipped=last+skipped))
                        
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def peekRight(self, start, stop, step, color, right, isKing, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= 8:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, 8)

                    moves.update(self.peekLeft(r + step,row,step,color,right - 1,isKing,skipped=last+skipped))
                    moves.update(self.peekRight(r + step,row,step,color,right + 1,isKing,skipped=last+skipped))
                    if isKing:
                        if step == 1:
                            row = max(r - 3, -1)
                        else:
                            row = min(r + 3, 8)
                        
                        moves.update(self.peekRight(r - step,row,-step,color,right + 1,isKing,skipped=last+skipped))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves

    def evaluate(self):
        
        return (self.blues - self.reds) + (len(self.getAllMoves((0,0,225))) - len(self.getAllMoves((225,0,0))))*0.2 + (self.developmentScore()*0.5)

    def getAllMoves(self, color):
        allMoves = []
        for piece in self.getAllPieces(color):
            validMoves = self.getValidMoves(piece)
            for move, skip in validMoves.items():
                tempBoard = deepcopy(self)
                tempPiece = tempBoard.getpiece(piece.row, piece.col)
                tempBoard.simulateMove(tempPiece, move, skip)
                allMoves.append(tempBoard)
        return allMoves

    def simulateMove(self, piece, move, skip):
        self.move(piece, move[0], move[1])
        if skip:
            self.remove(skip)

    def developmentScore(self):
        score = 0
        for piece in self.getAllPieces((0,0,225)):
            if piece.isKing:
                score += 10
            else:
                score+=piece.row
        for piece in self.getAllPieces((225,0,0)):
            if piece.isKing:
                score -= 10
            else:
                score-=piece.row
        return score


    def getAllPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def getUniqueID(self,myTurn):
        if myTurn:
            result = "1"
        else:
            result = "0"
        for rows in range(1,9):
            for cols in range(rows % 2, 8, 2):
                piece = self.board[rows-1][cols]
                if piece == 0:
                    result += "0"
                else:
                    if piece.color == (225,0,0):
                        if piece.isKing:
                            result += "3"
                        else:
                            result += "1"
                    else:
                        if piece.isKing:
                            result += "4"
                        else:
                            result +="2"
        return result