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
        copyBoard.turn = True
        piece.move(copyBoard,move)
        score = self.minmax(move,copyBoard,dept-1,False)
        return score

    def minmax(self,square,board,depth,maximizingComputer) -> int:
        """Min max algorithm."""

        if depth == 0:
            return self.heuristicFunction(board,depth)
        elif board.isWin() == "White":
            return self.heuristicFunction(board,depth)
        elif board.isWin() == "Black":
            return self.heuristicFunction(board,depth)


        nextBoard = self.getCopy(board)
        nextBoard.pieceUpdate()
        if maximizingComputer:
            #we should check every piece
            value = -(10**8)
            
            for piece in nextBoard.blackPieces:
                if piece.posMoves(nextBoard):
                    for move in piece.posMoves(nextBoard):
                        nextnextBoard = self.getCopy(nextBoard)
                        nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                        nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                        nextnextPiece.move(nextnextBoard,nextnextSquare)
                        
                        value = max(value,self.minmax(nextnextSquare,nextnextBoard,depth-1,False))
            return value 
        
        else:
            #oppounent move
            value = +(10**8)
            for piece in nextBoard.whitePieces:
                if piece.posMoves(nextBoard):
                    for move in piece.posMoves(nextBoard):
                        nextnextBoard = self.getCopy(nextBoard)
                        nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                        nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                        nextnextPiece.move(nextnextBoard,nextnextSquare)
                        
                        value = min(value,self.minmax(nextnextSquare,nextnextBoard,depth-1,True))
            return value 

    def heuristicFunction(self,board,depth) -> int:
        """Calculates the score of possible move and returns as intiger. Its the heuristic function of the game."""
        #has to work for bith players asn their benefit. evaluate the current board state
        score = 0
        board.pieceUpdate()
        depth = depth if depth>0 else 1


        for piece in board.blackPieces:
            if piece.location[0] == board.size-1:
                score += 10000*depth
            elif piece.location[0] == board.size-2:
                score += 100*depth
            else:
                score += piece.location[0]*10*depth

        score += len(board.blackPieces)*10

    
        #minus
        score -= len(board.whitePieces)*10

        for square in board.squares[0]:
            if square.occupiedPiece != None:
                if not square.occupiedPiece.isBlack:
                    score-= 9000

        for square in board.squares[1]:
            if square.occupiedPiece != None:
                if not square.occupiedPiece.isBlack:
                    score-= 200

        # winpos = -1 if turn else 0
        # oneMoreStep = -2 if turn else 1
        # board.pieceUpdate()

        # #plus
        # for square in board.squares[winpos]:
        #     if square.occupiedPiece != None:
        #         if square.occupiedPiece.isBlack == turn:
        #             score+=10000

        # for square in board.squares[oneMoreStep]:
        #     if square.occupiedPiece != None:
        #         if square.occupiedPiece.isBlack == turn:
        #             score+=20


        # #minus
        # for square in board.squares[0 if winpos==-1 else -1]:
        #     if square.occupiedPiece != None:
        #         if square.occupiedPiece.isBlack != turn:
        #             score-=9000

        # for square in board.squares[1 if oneMoreStep==-2 else -2]:
        #     if square.occupiedPiece != None:
        #         if square.occupiedPiece.isBlack != turn:
        #             score-= 100

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
        copyBoard.turn = board.turn
        copyBoard.squares = copySquares
        return copyBoard

