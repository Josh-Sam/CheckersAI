from copy import deepcopy
import pickle

with open('Data.pickle', 'rb') as handle:
        print("retriving Transpositon table...")
        transTable = (pickle.load(handle))
        print("Done.")
         
def miniMax(board, depth, myTurn, alpha, beta):
    
    if depth <= 0 or board.winner() != None:
        return board.evaluate(), board
    if transTable.get(board.getUniqueID(myTurn),[0,0,0,0])[2] >= depth:
        
        toReturn = transTable.get(board.getUniqueID(myTurn))
        print("depth added was:", transTable.get(board.getUniqueID(myTurn),[0,0,0,0])[2] - depth)
        return toReturn[1],deepcopy(toReturn[0])
    if myTurn:
        maxVal = float('-inf')
        bestMove = None
        for move in board.getAllMoves((0, 0, 225)):
            evaluation = miniMax(move, depth - 1, False,alpha,beta)[0]
            maxVal = max(maxVal, evaluation)
            
            if maxVal == evaluation:
                bestMove = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
              break
        if transTable.get(board.getUniqueID(myTurn),[0,0,0])[2] < depth:
            transTable.update({board.getUniqueID(myTurn): [deepcopy(bestMove),maxVal, depth, bestMove.getUniqueID(not myTurn)]})
        return maxVal, bestMove
    else:
        minVal = float('inf')
        worstMove = None
        for move in board.getAllMoves((225, 0, 0)):
            evaluation = miniMax(move, depth - 1, True,alpha,beta)[0]
            minVal = min(minVal, evaluation)
            beta = min(beta, evaluation)
            if minVal == evaluation:
                worstMove = move
            beta = min(beta, evaluation)
            if beta <= alpha:
              break
        if transTable.get(board.getUniqueID(myTurn),[0,0,0])[2] < depth:
            transTable.update({board.getUniqueID(myTurn): [deepcopy(worstMove),minVal, depth, worstMove.getUniqueID(not myTurn)]})
        return minVal, worstMove
