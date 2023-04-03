from .Square import Square
from .Piece import Piece
from .Board import Board

class Computer():
    def __init__(self,board):
        """Computer init."""
        self.board = board
        self.squares = self.board.squares
        
    def heuristicFunction(self,move)->int:
        """Calculates the score of possible move and returns as intiger. Its the heuristic function of the game."""
        score = 0
        loc = move.location #move is a square object
        
        if loc[0] == self.board.size-2:
            score+=50
        elif loc[0] ==  self.board.size-1:
            score+=1000

        if loc[0] != self.board.size-1:
            for i in [1,-1]:
                if loc[1]+i < 0 or loc[1]+i > self.board.size-1: 
                    continue

                diagPiece = self.squares[loc[0]+1][loc[1]+i].occupiedPiece
                if diagPiece !=None:
                    if not diagPiece.isBlack:
                        score -= 10
                        break 
        
        for square in self.squares[1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == False and loc != square.location:
                    score -= 900
        
        for square in self.squares[2]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == False and loc != square.location:
                    score -= 30
        
        return score

    def move(self):
        movesDict = {}
        copyboard = self.getCopy()
        #piece = copyboard.squares[realPiece.location[0]][realPiece.location[1]].occupiedPiece
        for piece in self.board.blackPieces:
            if piece.posMoves(self): #check if it's empty
                for move in piece.posMoves(self): #move is a square object
                    score = self.heuristicFunction(move)
                    movesDict[(piece,move)] = score
        moveslist = sorted(movesDict.items(), key=lambda item: item[1],reverse=True) #(((piece,square),score),...)

        moveTuple = moveslist[0][0]
        piece = moveTuple[0]
        targetSquare = moveTuple[1]

        piece.move(self.board,targetSquare)

    def minmax(self,square,dept,maximizingComputer):
        # if depth = 0 or node is a terminal node then
        #     return the heuristic value of node

        # if maximizingPlayer then
        #     value := −∞
        #     for each child of node do
        #         value := max(value, minimax(child, depth − 1, FALSE))
        #     return value
        # else (* minimizing player *)
        #     value := +∞
        #     for each child of node do
        #         value := min(value, minimax(child, depth − 1, TRUE))
        #     return value
        if dept == 0:
            return self.heuristicFunction(square)
        elif maximizingComputer and square.location[0] == self.board.size-1:
            return self.heuristicFunction(square)
        elif not maximizingComputer and square.location[0] == 0:
            return self.heuristicFunction(square)
        

        if maximizingComputer:
            value = -10**10

    def posMoves(self,square,isBlack):#scrap for now
        #scrap for now
        output = []
        location = square.location
        front_ax = location[0]+1 if isBlack else location[0]-1
        moveList = [[front_ax,location[1]+1],[front_ax,location[1]],[front_ax,location[1]-1]]
        
        for move in moveList:
            try:
                if move[1]<0:continue

                nextSquare = self.board.squares[move[0]][move[1]]

                if nextSquare.occupiedPiece != None:
                    if moveList[1] != move:
                        if nextSquare.occupiedPiece.isBlack != self.isBlack:
                            output.append(nextSquare)
                else:
                    output.append(nextSquare)
            except:
                continue

        return output

    def getCopy(self):
        """Return copy of the current board"""
        copySquares = []
        
        for row in self.board.squares:
            square.append([])
            for square in row:
                temp = Square(square.x,square.y,square.width,square.height,square.location)
                if square.occupiedPiece != None:
                    temp.occupiedPiece = Piece(square.occupiedPiece.isBlack,square.occupiedPiece.location)
                copySquares.append(temp)
        
        copyBoard = Board(self.board.width,self.board.height,genSquares=False)
        copyBoard.squares = copySquares
        return copyBoard

    def score_move(self,copyBoard,move,piece,dept):
        piece.move(copyBoard,move)
        score = self.minmax(move,dept-1)

        


    
