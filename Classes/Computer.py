from .Square import Square
from .Piece import Piece
from .Board import Board
from random import choice


class Computer():
    def __init__(self,board):
        """Computer init."""
        self.board = board
        self.squares = self.board.squares

    def move(self,depth):
        """Function that initiates the hole moving sequence."""

        movesDict = {}
        for piece in self.board.blackPieces:
            if piece.posMoves(self.board): #check if it's empty
                for move in piece.posMoves(self.board): #move is a square object
                    
                    copyBoard = self.getCopy(self.board)
                    copySquare = copyBoard.squares[move.location[0]][move.location[1]]
                    copyPiece = copyBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                    
                    score = self.score_move(copyBoard,copySquare,copyPiece,depth)
                    movesDict[(piece,move)] = score

        #moveslist = sorted(movesDict.items(), key=lambda item: item[1],reverse=True) #(((piece,square),score),...)
        
        max_cols = [key for key in movesDict.keys() if movesDict[key] == max(movesDict.values())]

        moveTuple = choice(max_cols)
        piece = moveTuple[0]
        targetSquare = moveTuple[1]


        for key in movesDict:
            print("Piece Location: ",key[0].location," Score: ",movesDict[key]," Move Location: ",key[1].location," Made" if key[0]==piece and key[1]==targetSquare  else "")
        print("\n")

        piece.move(self.board,targetSquare)

    def score_move(self,copyBoard,move,piece,dept) -> int:
        """Returns the final score."""
        piece.move(copyBoard,move)
        score = self.minmax(move,copyBoard,dept-1,False)
        return score

    def minmax(self,square,board,dept,maximizingComputer) -> int:
        """Min max algorithm."""
        
        #turn = not maximizingComputer
        #when turn is not maximizingComputer, AI gets points for win 
        #when turn is maximizingComputer, AI can prevent oppunent win

        if dept == 0:
            return self.heuristicFunction(board,True)
        elif board.isWin() == "White":
            print("white",dept,maximizingComputer)
            return self.heuristicFunction(board,dept%2)
        elif board.isWin() == "Black":
            print("black",dept,maximizingComputer)
            return self.heuristicFunction(board,dept%2)


        nextBoard = self.getCopy(board)
        nextBoard.pieceUpdate()
        if maximizingComputer:
            #we should check every piece
            value = -(10**8)
            
            for piece in nextBoard.blackPieces:
                for move in piece.posMoves(nextBoard):
                    nextnextBoard = self.getCopy(nextBoard)
                    nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                    nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                    nextnextPiece.move(nextnextBoard,nextnextSquare)

                    value = max(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,False))
            return value 
        
        else:
            #oppounent move
            value = +(10**8)
            for piece in nextBoard.whitePieces:
                for move in piece.posMoves(nextBoard):
                    nextnextBoard = self.getCopy(nextBoard)
                    nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                    nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                    nextnextPiece.move(nextnextBoard,nextnextSquare)

                    value = min(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,True))
            return value 

    def heuristicFunction(self,board,turn) -> int:
        """Calculates the score of possible move and returns as intiger. Its the heuristic function of the game."""
        #has to work for bith players asn their benefit. evaluate the current board state
        score = 0

        winpos = -1 if turn else 0
        oneMoreStep = -2 if turn else 1

        #plus
        for square in board.squares[winpos]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == turn:
                    score+=10000

        for square in board.squares[oneMoreStep]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == turn:
                    score+=20

        #minus
        for square in board.squares[0 if winpos==-1 else -1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack != turn:
                    score-=9000

        for square in board.squares[1 if oneMoreStep==-2 else -2]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack != turn:
                    score-= 100
        
        return score
           
    def getCopy(self,board) -> Board:
        """Return copy of the given board."""
        copySquares = []
        
        for row in board.squares:
            copySquares.append([])
            for square in row:
                temp = Square(square.x,square.y,square.width,square.height,square.location)
                if square.occupiedPiece != None:
                    temp.occupiedPiece = Piece(square.occupiedPiece.isBlack,square.occupiedPiece.location)
                copySquares[-1].append(temp)
        
        copyBoard = Board(board.width,board.height,board.size,board.gap,genSquares=False)
        copyBoard.squares = copySquares
        return copyBoard


        


