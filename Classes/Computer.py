from .Square import Square
from .Piece import Piece
from .Board import Board
from random import choice


class Computer():
    """
    A class to represent Computer.

    ...

    Attributes
    ----------
    board : Board
            board object to play on

    squares : list
            contains all squares. squares[row][column]
    
    """

    def __init__(self, board: Board):
        """
        Constructs all the necessary attributes for the Computer object.

        Parameters
        ----------
        board : Board
                board object to play on
        """

        self.board = board
        self.squares = self.board.squares

    def move(self, depth: int) -> None:
        """
        Function that initiates the hole moving sequence. Gets score for possible moves and makes one based on scores.
        
        Parameters:
                depth (int): depth of N-step look ahead algorithm
        
        """

        movesDict = {}
        for piece in self.board.blackPieces:
            if piece.posMoves(self.board): #check if it's empty
                for move in piece.posMoves(self.board): #move is a square object
                    
                    copyBoard = self.getCopy(self.board)
                    copySquare = copyBoard.squares[move.location[0]][move.location[1]]
                    copyPiece = copyBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                    
                    score = self.score_move(copyBoard,copySquare,copyPiece,depth)
                    movesDict[(piece,move)] = score
        
        max_cols = [key for key in movesDict.keys() if movesDict[key] == max(movesDict.values())]

        moveTuple = choice(max_cols)
        piece = moveTuple[0]
        targetSquare = moveTuple[1]

        for key in movesDict:
            print("Piece Location: ",key[0].location," Score: ",movesDict[key]," Move Location: ",key[1].location," Made" if key[0]==piece and key[1]==targetSquare  else "")
        print("\n")
        
        piece.move(self.board,targetSquare)

    def score_move(self, copyBoard: Board, move: Square, piece: Piece, dept: int) -> int:
        """
        Initiates the minmax function.
        
        Parameters:
                copyBoard (Board): Board object to make(more like imitate) the move

                move (Square): target square to piece to go

                piece (Piece): Piece object to move

                depth (int): depth of N-step look ahead algorithm

        Returns:
                score (int): score of the given move of the piece

        """

        copyBoard.turn = True
        piece.move(copyBoard,move)
        score = self.minmax(copyBoard,dept-1,False)
        return score

    def minmax(self, board: Board, depth: int, maximizingComputer: bool) -> int:
        """
        Min max algorithm. Calls back itself until depth is 0 or there is a winning case in the given board.
        
        Parameters:
                copyBoard (Board): Board object to make(more like imitate) the move

                depth (int): depth of N-step look ahead algorithm

                maximizingComputer (bool): MAX if True Min if False

        Returns:
                value (int): score based on MIN or MAX

                OR

                heuristicFunction() -> (int): calculates the score of the given board
        
        """

        if depth == 0:
            return self.heuristicFunction(board,depth)
        elif board.isWin() != False:
            return self.heuristicFunction(board,depth)

        nextBoard = self.getCopy(board)
        nextBoard.pieceUpdate()

        #MAX
        if maximizingComputer:
            value = -(10**8)
            
            for piece in nextBoard.blackPieces:
                if piece.posMoves(nextBoard):
                    for move in piece.posMoves(nextBoard):
                        nextnextBoard = self.getCopy(nextBoard)
                        nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                        nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                        nextnextPiece.move(nextnextBoard,nextnextSquare)
                        
                        value = max(value,self.minmax(nextnextBoard,depth-1,False))
            return value 
        
        #MIN
        else:
            value = +(10**8)
            for piece in nextBoard.whitePieces:
                if piece.posMoves(nextBoard):
                    for move in piece.posMoves(nextBoard):
                        nextnextBoard = self.getCopy(nextBoard)
                        nextnextSquare = nextnextBoard.squares[move.location[0]][move.location[1]]
                        nextnextPiece = nextnextBoard.squares[piece.location[0]][piece.location[1]].occupiedPiece
                        nextnextPiece.move(nextnextBoard,nextnextSquare)
                        
                        value = min(value,self.minmax(nextnextBoard,depth-1,True))
            return value 

    def heuristicFunction(self, board: Board, depth: int) -> int:
        """
        Calculates the score of the given board. Its the heuristic function of the game.
        
        Parameters:
                board (Board): Board object to analiyze

                depth (int): depth of N-step look ahead algorithm

        Returns:
                score (int): total score of the given board

        """

        score = 0
        board.pieceUpdate()
        depth = depth if depth>0 else 1

        #Reward
        score += len(board.blackPieces)*10

        for piece in board.blackPieces:
            if piece.location[0] == board.size-1:
                score += 10000*depth
            elif piece.location[0] == board.size-2:
                score += 100*depth
            else:
                score += piece.location[0]*10*depth

        #Punishment
        score -= len(board.whitePieces)*10

        for square in board.squares[0]:
            if square.occupiedPiece != None:
                if not square.occupiedPiece.isBlack:
                    score-= 10000*depth

        for square in board.squares[1]:
            if square.occupiedPiece != None:
                if not square.occupiedPiece.isBlack:
                    score-= 200

        return score
           
    def getCopy(self, board: Board) -> Board:
        """
        Return copy of the given board. This function creates exact coppies of Board, Square and Piece objects by creating new ones
        
        Parameters:
                board (Board): board to copy

        Returns:
                copyBoard (Board): copy of the given board
        """
        copySquares = []
        
        for row in board.squares:
            copySquares.append([])
            for square in row:
                temp = Square(square.x,square.y,square.width,square.height,square.location)
                if square.occupiedPiece != None:
                    temp.occupiedPiece = Piece(square.occupiedPiece.isBlack,square.occupiedPiece.location)
                copySquares[-1].append(temp)
        
        copyBoard = Board(board.width,board.height,board.size,genSquares=False)
        copyBoard.turn = board.turn
        copyBoard.squares = copySquares
        return copyBoard
