class Piece():
    """
    A class to represent Pieces.

    ...

    Attributes
    ----------
    isBlack : bool
            to determine piece color

    location : tuple
            contains row and column values
    
    """
    def __init__(self,isBlack: bool, location: tuple):
        """
        Constructs all the necessary attributes for the Piece object.

        Parameters
        ----------
        isBlack : bool
            to determine piece color

        location : tuple
            contains row and column values
        """

        self.isBlack = isBlack
        self.location = location #location(row,column)

    def posMoves(self,board) -> list:
        """
        Finds the possible moves for the Piece object. Returns list containing Square objects.
        
        Parameters:
                board (Board): board to calculate possible moves on
        
        Returns:
                output (list): contains possible moves as Square objects

        """
        output = []
        front_ax = self.location[0]+1 if self.isBlack else self.location[0]-1
        moves = [[front_ax,self.location[1]+1],[front_ax,self.location[1]],[front_ax,self.location[1]-1]]
        
        for move in moves:
            if move[1]<0 or move[1] > board.size-1 or front_ax < 0 or front_ax > board.size-1:
                continue

            square = board.squares[move[0]][move[1]]
            if square.occupiedPiece != None:
                if moves[1] != move and square.occupiedPiece.isBlack != self.isBlack:
                    output.append(square)
            else:
                output.append(square)

        return output

    def move(self,board,targetSquare) -> None:
        """
        Handels the move of the Piece.
        
        Parameters:
                board (Board): board to make move on

                targetSquare (Square): Square object to move

        """
        currentSquare = board.squares[self.location[0]][self.location[1]]
        
        targetSquare.occupiedPiece = self
        self.location = targetSquare.location
        
        currentSquare.occupiedPiece = None
        board.selectedPiece = None
        
        for row in board.squares:
            for square in row:
                if square.isHighlight:
                    square.isHighlight = False
        board.turn = not board.turn