from .Square import Square
from .Piece import Piece
from .Board import Board

class Computer():
    def __init__(self,board):
        """Computer init."""
        self.board = board
        self.squares = self.board.squares
        
    def heuristicFunction(self,board,turn) -> int:
        """Calculates the score of possible move and returns as intiger. Its the heuristic function of the game."""
        #has to work for bith players asn their benefit.

        score = 0
        squares = board.squares
        
        """ # if loc[0] == self.board.size-2:
        #     score+=50
        # elif loc[0] ==  self.board.size-1:
        #     score+= 10**4
           # if loc[0] != self.board.size-1:
        #     for i in [1,-1]:
        #         if loc[1]+i < 0 or loc[1]+i > self.board.size-1: 
        #             continue

        #         diagPiece = self.squares[loc[0]+1][loc[1]+i].occupiedPiece
        #         if diagPiece !=None:
        #             if not diagPiece.isBlack:
        #                 score -= 10
        #                 break """

        #checks the pieces that 1 move away from win.
        for square in squares[1 if turn else -2]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == turn:
                    score+= 50
        
        #checks the pieces in the wining  position.
        for square in squares[-1 if turn else 0]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack == turn:
                    score+= 10**4
        
        #cheks if the pieces are in danger.
        for row in squares:
            for square in row:
                if square.occupiedPiece != None:
                    if square.occupiedPiece.isBlack == turn:
                        piece = square.occupiedPiece
                        loc = piece.location
                        if loc[0] < board.size-1 and loc[0] > board.size-1:
                            for i in [1,-1]:
                                if loc[1]+i < 0 or loc[1]+i > self.board.size-1: 
                                    continue

                                diagPiece = squares[loc[0]+1][loc[1]+i].occupiedPiece
                                if diagPiece !=None:
                                    if diagPiece.isBlack != turn:
                                        score -= 10
                                        break 
        
        #checking tuns's side if there are any oppounent piece
        for square in self.squares[0 if turn else -1]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack != turn :
                    score -= 900 
        for square in self.squares[1 if turn else -2]:
            if square.occupiedPiece != None:
                if square.occupiedPiece.isBlack != turn:
                    score -= 30
        
        return score

    def move(self,depth):
        """Function that initiates the hole moving sequence."""

        movesDict = {}
        copyBoard = self.getCopy()
        #piece = copyboard.squares[realPiece.location[0]][realPiece.location[1]].occupiedPiece
        for piece in self.board.blackPieces:
            if piece.posMoves(self.board): #check if it's empty
                for move in piece.posMoves(self.board): #move is a square object

                    copySquare = copyBoard.squares[move.location[0]][move.location[1]]
                    copyPiece = copySquare.occupiedPiece
                    
                    score = self.score_move(copyBoard,copySquare,copyPiece,depth)
                    movesDict[(piece,move)] = score
        
        
        moveslist = sorted(movesDict.items(), key=lambda item: item[1],reverse=True) #(((piece,square),score),...)

        moveTuple = moveslist[0][0]
        piece = moveTuple[0]
        targetSquare = moveTuple[1]

        piece.move(self.board,targetSquare)

    def minmax(self,square,board,dept,maximizingComputer) -> int:
        """Min max algorithm."""
        
        if dept == 0:
            return self.heuristicFunction(board,maximizingComputer)
        elif maximizingComputer and square.location[0] == self.board.size-1:
            return self.heuristicFunction(board,maximizingComputer)
        elif not maximizingComputer and square.location[0] == 0:
            return self.heuristicFunction(board,maximizingComputer)
        
        nextBoard = self.getCopy(board)
        if maximizingComputer:
            value = -(10**10)
            
            nextSquare = nextBoard.squares[square.location[0]][square.location[1]]
            nextPiece = nextSquare.occupiedPiece
            for move in nextPiece.posMoves():
                # move is a square, and will not be same with the copy 
                # so we have to find this square in the copy board

                nextnextBoard = self.getCopy(nextBoard)
                nextnextSquare = nextnextBoard.squares[nextSquare.location[0]][nextSquare.location[1]]
                nextnextPiece = nextnextSquare.occupiedPiece  
                move = nextnextBoard.squares[move.location[0]][move.location[1]]

                nextnextPiece.move(nextnextBoard,move)
                value = max(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,False))
            return value 
       
        else:
            #opponuent move
            value = +(10**10)
            nextBoard.pieceUpdate()
            for piece in nextBoard.whitePieces:
                for move in piece.posMoves():
                    nextnextBoard = self.getCopy(nextBoard)
                    nextnextSquare = nextnextBoard.squares[nextSquare.location[0]][nextSquare.location[1]]
                    nextnextPiece = nextnextSquare.occupiedPiece  
                    move = nextnextBoard.squares[move.location[0]][move.location[1]]

                    nextnextPiece.move(nextnextBoard,move)
                    value = min(value,self.minmax(nextnextSquare,nextnextBoard,dept-1,True))
            
            return value 
           
    def getCopy(self,board) -> Board:
        """Return copy of the current board"""
        copySquares = []
        
        for row in board.squares:
            square.append([])
            for square in row:
                temp = Square(square.x,square.y,square.width,square.height,square.location)
                if square.occupiedPiece != None:
                    temp.occupiedPiece = Piece(square.occupiedPiece.isBlack,square.occupiedPiece.location)
                copySquares.append(temp)
        
        copyBoard = Board(board.width,board.height,board.size,board.gap,genSquares=False)
        copyBoard.squares = copySquares
        return copyBoard

    def score_move(self,copyBoard,move,piece,dept) -> int:
        """Returns the final score."""
        piece.move(copyBoard,move)
        score = self.minmax(move,dept-1,copyBoard)
        return score

        


    
