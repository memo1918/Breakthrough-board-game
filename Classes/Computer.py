from .Square import Square
from .Piece import Piece
from .Board import Board
from random import choice

class Computer():
    def __init__(self,board):
        """Computer init."""
        self.board = board
        self.squares = self.board.squares
        self.something = []
        
    
    def move(self,depth):
        """Function that initiates the hole moving sequence."""

        movesDict = {}
        for piece in self.board.blackPieces:
            if piece.posMoves(self.board): #check if it's empty
                for move in piece.posMoves(self.board): #move is a square object
                    
                    copyBoard = self.getCopy(self.board)
                    copySquare = copyBoard.squares[move.location[0]][move.location[1]]
                    copyPiece = copyBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece#being none
                    
                    score = self.score_move(copyBoard,copySquare,copyPiece,depth)
                    movesDict[(piece,move)] = score
        
        #print(self.something)
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
        self.something.append([])
        score = self.minmax(move,copyBoard,dept-1,False)
        return score

    def minmax(self,square,board,dept,maximizingComputer) -> int:
        """Min max algorithm."""
        
        if dept == 0:
            return self.heuristicFunction(board,square,maximizingComputer)
        elif maximizingComputer and square.location[0] == self.board.size-1:
            return self.heuristicFunction(board,square,maximizingComputer)
        elif not maximizingComputer and square.location[0] == 0:
            return self.heuristicFunction(board,square,maximizingComputer)
        
        nextBoard = self.getCopy(board)
        if maximizingComputer:
            #we should check every piece
            value = -(10**8)
            nextBoard.pieceUpdate()
            for piece in nextBoard.blackPieces:
                for move in piece.posMoves(nextBoard):
                    nextnextBoard = self.getCopy(nextBoard)
                    nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                    nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece

                    nextnextPiece.move(nextnextBoard,nextnextSquare)
                    value = max(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,True))
            return value 

            # nextSquare = nextBoard.squares[square.location[0]][square.location[1]]
            # nextPiece = nextSquare.occupiedPiece
            # for move in nextPiece.posMoves(nextBoard):
            #     # move is a square, and will not be same with the copy 
            #     # so we have to find this square in the copy board

            #     nextnextBoard = self.getCopy(nextBoard)
            #     nextnextSquare = nextnextBoard.squares[nextSquare.location[0]][nextSquare.location[1]]
            #     nextnextPiece = nextnextBoard.squares[nextPiece.location[0]][nextPiece.location[1]].occupiedPiece
            #     move = nextnextBoard.squares[move.location[0]][move.location[1]]

            #     nextnextPiece.move(nextnextBoard,move)
            #     value = max(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,False))
            # return value 
        
       
        else:
            #oppounent move
            value = +(10**8)
            nextBoard.pieceUpdate()
            for piece in nextBoard.whitePieces:
                for move in piece.posMoves(nextBoard):
                    nextnextBoard = self.getCopy(nextBoard)
                    nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                    nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece

                    nextnextPiece.move(nextnextBoard,nextnextSquare)
                    value = min(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,True))
            
            return value 

    def heuristicFunction(self,board,scoreSquare,turn) -> int:
        """Calculates the score of possible move and returns as intiger. Its the heuristic function of the game."""
        #has to work for bith players asn their benefit. 
        #TODO: we shold not check the hole board.

        score = 0
        squares = board.squares
        piece = scoreSquare.occupiedPiece
        loc = piece.location

        self.something[-1].append([loc,scoreSquare.location])
        
        # #checks the pieces that 1 move away from win.
        # for square in squares[-2 if turn else 1]:
        #     if square.occupiedPiece != None:
        #         if square.occupiedPiece.isBlack == turn:
        #             score+= 50
        
        # #checks the pieces in the wining  position.
        # for square in squares[-1 if turn else 0]:
        #     if square.occupiedPiece != None:
        #         if square.occupiedPiece.isBlack == turn:
        #             score+= 10**4
        
        #cheks if the pieces are in danger.
        # for row in squares:
        #     for square in row:
        #         if square.occupiedPiece != None:
        #             if square.occupiedPiece.isBlack == turn:
        #                 piece = square.occupiedPiece
        #                 loc = piece.location
        #                 if loc[0] < board.size-1 and loc[0] > board.size-1:
        #                     for i in [1,-1]:
        #                         if loc[1]+i < 0 or loc[1]+i > self.board.size-1: 
        #                             continue

        #                         diagPiece = squares[loc[0]+1][loc[1]+i].occupiedPiece
        #                         if diagPiece !=None:
        #                             if diagPiece.isBlack != turn:
        #                                 score -= 10
        #                                 break 

        if loc[0] == (-2 if turn else 1):
            print("i am here")
            score += 50
        elif loc[0] ==  (-1 if turn else 0):
            print("i am here2")
            score += 10**4
        
        #checking tuns's side if there are any oppounent piece
        for square in squares[1 if turn else -2]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack != turn and loc != square.location:
                    score -= 40
        
        for square in squares[0 if turn else -1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack != turn and loc != square.location:
                    score -= 10**3
        
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


        


    
